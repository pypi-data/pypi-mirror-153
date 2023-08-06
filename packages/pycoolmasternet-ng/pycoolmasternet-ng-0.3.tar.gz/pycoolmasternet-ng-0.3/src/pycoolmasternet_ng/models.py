from decimal import Decimal
from typing import Any, Dict, List, Optional, Union

from .constants import (
    CM_FAN_MODE_FSPEED_ARG_MAP,
    CM_FAN_MODE_MAP,
    CM_LOUVER_POSITION_STATE_MAP,
    CM_MODE_MAP,
    CM_PROPS_MODE_MAP,
    FanMode,
    LineType,
    LouverPosition,
    LouverPositionState,
    Mode,
    QueryDatapoint,
)
from .data import LINE_TYPE_TO_BRAND_NAME, LINE_TYPE_TO_MODE_TEMP_RANGE
from .exceptions import CoolMasterNetNoUidError, DeviceDisappearedException
from .structures import UID, Line
from .transports import BaseTransport


class Gateway:
    """
    A CoolMasterNet gateway.
    """

    def __init__(self, transport: BaseTransport):
        self.transport = transport

    @classmethod
    async def from_transport(cls, transport: BaseTransport) -> "Gateway":
        c = cls(transport)
        await c.refresh()
        return c

    @property
    def serial_number(self):
        return self._settings.get("S/N")

    @property
    def version(self):
        return self._settings.get("Version")

    async def refresh(self):
        await self.refresh_settings()
        await self.refresh_props()
        await self.refresh_lines()
        await self.refresh_devices()

    async def refresh_devices(self):
        ls_results = await self.transport.command("ls2")

        self._devices = {}
        self._coolplug_lines = {}

        for line in ls_results:
            uid = UID.from_string(line.split()[0])

            is_coolplug = self.lines[uid.line_number].type in (LineType.PLUGBUS, LineType.PLUGBUS_WIRELESS)

            if is_coolplug:
                self._coolplug_lines[uid] = self._parse_lines_result(await self.transport.plug_command(uid, "line"))

            # according to CoolAutomation, the HVAC will always be on line 1 of a CoolPlug
            device_line = self._coolplug_lines[uid][1] if is_coolplug else self._lines[uid.line_number]

            self._devices[uid] = await Device.init_with_ls_line(
                self, line, hvac_line=device_line, properties=self.properties.get(uid, {})
            )

    async def refresh_props(self):
        props_results = await self.transport.command("props")

        heading_line = props_results[0]
        headings = list(s.strip() for s in heading_line.split("|") if s.strip())

        self._properties = {}

        for unit_line in props_results[2:]:
            props = {key: value for key, value in zip(headings, list(s.strip() for s in unit_line.split("|")))}

            self._properties[UID.from_string(props.pop("UID"))] = props

    async def refresh_lines(self):
        line_results = await self.transport.command("line")

        self._lines = self._parse_lines_result(line_results)

    async def refresh_settings(self):
        self._settings = await self.get_settings()

    async def get_settings(self) -> Dict[str, str]:
        set_results = await self.transport.command("set")

        return self._parse_key_values(set_results)

    async def get_ifconfig(self) -> Dict[str, str]:
        ifconfig_results = await self.transport.command("ifconfig")

        return self._parse_key_values(ifconfig_results)

    @staticmethod
    def _parse_key_values(lines: List[str]) -> Dict[str, str]:
        results = {}

        for line in lines:
            key, value = line.split(": ")

            results[key.strip()] = value.strip()

        return results

    @staticmethod
    def _parse_lines_result(line_results):
        lines = {}

        for heading, meta in zip(line_results[0::2], line_results[1::2]):
            line = Line.from_heading_meta(heading=heading, meta=meta)
            lines[line.number] = line

        return lines

    @property
    def properties(self) -> Dict[UID, dict]:
        return getattr(self, "_properties", {})

    @property
    def devices(self) -> Dict[UID, "Device"]:
        return getattr(self, "_devices", {})

    @property
    def lines(self) -> Dict[int, Any]:
        return getattr(self, "_lines", {})

    async def unit_command(self, uid: UID, command: str, extra_args: Optional[List[str]] = None):
        """
        Sends a command to a unit.
        """
        return await self.transport.unit_command(uid=uid, command=command, extra_args=extra_args)

    async def plug_unit_command(self, plug_uid: UID, uid: UID, command: str, extra_args: Optional[List[str]] = None):
        """
        Sends a command to a unit via a CoolPlug.
        """

        args = [command, str(uid)]

        if extra_args:
            args += extra_args

        return await self.transport.plug_command(plug_uid, " ".join(args))

    def __str__(self):
        return f"S/N: {self.serial_number} @ " + str(self.transport)


class Device:
    """
    An HVAC device connected to a gateway.

    Most methods take a "refresh" boolean parameter. This is True by default
    meaning that the internal state will be refreshed by querying the device after the command completes.

    If you are setting multiple values in quick succession, it might be better for performance
    to set it to False and then call refresh() manually afterwards.
    """

    def __init__(self, gateway: Gateway, uid: UID, hvac_line: Line, properties: dict):
        self.gateway = gateway
        self.uid = uid
        self.properties = properties
        self.hvac_line = hvac_line

    @classmethod
    async def init_with_ls_line(cls, gateway: Gateway, ls_line: str, **kwargs):
        """
        Shortcut method to create the class from an existing "ls2" result line.

        This avoids an unnecessary command being issued if the data is already available,
        for example as a result of the gateway doing an initial "ls2" when discovering devices.
        """

        c = cls(gateway=gateway, uid=UID.from_string(ls_line.split()[0]), **kwargs)

        c._populate_from_ls_line(ls_line)
        await c._refresh_louver_position()

        return c

    def __str__(self):
        return str(self.uid)

    async def command(self, command: str, extra_args=None, refresh: bool = True):
        """
        Sends a command to the device's UID.

        :param refresh: whether to refresh the internal state after completion.
        Set this to False if issuing multiple commands in sequence and then call refresh() manually.
        """

        result = await self.gateway.unit_command(uid=self.uid, command=command, extra_args=extra_args)

        if refresh:
            await self.refresh()

        return result

    async def query(self, datapoint: QueryDatapoint) -> str:
        """
        Query a datapoint and return its value as a string.
        """
        result = await self.command("query", extra_args=[datapoint.value], refresh=False)
        return result[0]

    async def refresh(self):
        """
        Refresh the internal state by querying the gateway for the device's status.
        """

        try:
            ls_line = await self.command("ls2", refresh=False)  # ["L5.001 OFF 22.0C 22.8C Top  Heat OK   - 0"]
        except CoolMasterNetNoUidError:
            raise DeviceDisappearedException(self.uid)

        self._populate_from_ls_line(ls_line[0])
        await self._refresh_louver_position()

    def _populate_from_ls_line(self, ls_line: str):
        """
        Populate the internal state from an existing line from a "ls2" command.
        """

        _, power_state, target_temp, current_temp, fan_mode, mode, error_code, filter_sign, demand = ls_line.split()

        self._power_state = power_state == "ON"
        self._temperature_unit = target_temp[-1:]
        self._target_temp = Decimal(target_temp[:-1])
        self._current_temp = Decimal(current_temp[:-1])
        self._fan_mode = CM_FAN_MODE_MAP[fan_mode]
        self._mode = CM_MODE_MAP[mode]
        self._error_code = error_code if error_code != "OK" else None
        self._filter_sign = filter_sign == "#"
        self._demand = demand != "0"

    async def _refresh_louver_position(self):
        """
        Refreshes the louver/swing position. We skip checking if the unit previously told us
        it does not support it as we assume a unit can not gain this capability at runtime.
        """

        # the hasattr check is needed as we want to allow this to be called on class initialization
        # before the internal state attributes have been created

        if not hasattr(self, "_louver_position") or self.louver_position != LouverPositionState.NOT_SUPPORTED:
            self._louver_position = CM_LOUVER_POSITION_STATE_MAP[await self.query(QueryDatapoint.LOUVER_POSITION)]

    @property
    def power_state(self) -> bool:
        """
        Boolean state of the power status of the device. True for "on", false otherwise.
        """
        return getattr(self, "_power_state")

    @property
    def temperature_unit(self) -> str:
        """
        The temperature unit set on the device. This *MAY* depend on the configuration
        of the CoolMasterNet gateway and any intermediary (CoolPlug) gateways. It is not
        guaranteed to reflect the user-facing configuration on the device's thermostat.

        Returns "C" or "F".
        """
        return getattr(self, "_temperature_unit")

    @property
    def target_temperature(self) -> Decimal:
        """
        The target temperature the device is set at.
        """
        return getattr(self, "_target_temp")

    @property
    def current_temperature(self) -> Decimal:
        """
        The current ambient temperature.

        Note that this may reflect the temperature set via set_current_temperature()
        and cached by the CoolMasterNet device but there is still no guarantee
        that the device is actually using this temperature.
        """
        return getattr(self, "_current_temp")

    @property
    def fan_mode(self) -> FanMode:
        """
        The current fan speed mode of the device.
        """
        return getattr(self, "_fan_mode")

    @property
    def mode(self) -> Mode:
        """
        The current mode (cooling, heating, drying, etc) of the device.
        """
        return getattr(self, "_mode")

    @property
    def louver_position(self) -> LouverPositionState:
        """
        The current louver position (swing) of the device.
        """
        return getattr(self, "_louver_position")

    @property
    def error_code(self) -> Optional[str]:
        """
        The current error code as reported by the device.

        None means there is no error.
        """
        return getattr(self, "_error_code")

    @property
    def filter_sign(self) -> bool:
        """
        Boolean flag whether the device is requesting a filter change.
        """
        return getattr(self, "_filter_sign")

    @property
    def demand(self) -> bool:
        """
        Boolean flag whether the device is currently reporting "demand"
        (most likely requesting refrigerant from the condensing unit).

        Not always reliable: some units or configurations consistently report this as no demand.
        """
        return getattr(self, "_demand")

    @property
    def target_temperature_range(self):
        """
        Allowed temperature range for the current mode.
        """
        ranges = self.temperature_ranges

        if ranges:
            return ranges.get(self.mode)

    @property
    def temperature_ranges(self):
        """
        A mapping of mode to temperature ranges, if known.
        """
        return LINE_TYPE_TO_MODE_TEMP_RANGE.get(self.hvac_line.type)

    @property
    def friendly_name(self) -> Optional[str]:
        """
        Returns the friendly name if one has been set using the "props" command.
        """
        return self.properties.get("Name")

    @property
    def supported_modes(self) -> List[Mode]:
        if "Modes" not in self.properties:
            return list(Mode)

        modes = (s.strip() for s in self.properties["Modes"].split() if s.strip())
        modes = list(CM_PROPS_MODE_MAP[m] for m in modes if m in CM_PROPS_MODE_MAP)

        # TODO: auxiliary heat is not supported yet
        return modes

    @property
    def supported_fan_speeds(self) -> List[FanMode]:
        if "Fspeeds" not in self.properties:
            return list(FanMode)

        modes = (s.strip() for s in self.properties["Fspeeds"].split() if s.strip())
        modes = list(CM_FAN_MODE_FSPEED_ARG_MAP[m] for m in modes if m in CM_FAN_MODE_FSPEED_ARG_MAP)

        return modes

    @property
    def brand_name(self) -> Optional[str]:
        """
        Returns the brand name of this unit if it can be inferred.
        """
        return LINE_TYPE_TO_BRAND_NAME.get(self.hvac_line.type)

    async def set_power_state(self, power_state: bool, refresh: bool = True):
        await self.command("on" if power_state else "off", refresh=refresh)

    async def set_mode(self, mode: Mode, refresh: bool = True):
        await self.command(mode.value.lower(), refresh=refresh)

    async def set_temperature(self, temperature: Union[int, float, Decimal], refresh: bool = True):
        await self.command("temp", [f"{temperature:.1f}"], refresh=refresh)

    async def set_fan_mode(self, fan_speed: FanMode, refresh: bool = True):
        await self.command("fspeed", [CM_FAN_MODE_FSPEED_ARG_MAP[fan_speed]], refresh=refresh)

    async def set_louver_position(self, position: LouverPosition, refresh: bool = True):
        await self.command("swing", [position.value], refresh=refresh)

    async def reset_filter_sign(self, refresh: bool = True):
        await self.command("filt", refresh=refresh)

    async def set_current_temperature(self, temperature: Union[int, float, Decimal], refresh: bool = True):
        """
        Provides the value as the current ambient temperature for the device.

        This is cached by the CoolMasterNet gateway and will then be reported as the current
        temperature measured by the device even if the device itself ignores it.
        """
        await self.command("feed", [f"{temperature:.1f}"], refresh=refresh)
