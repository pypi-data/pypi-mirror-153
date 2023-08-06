import asyncio
from typing import List, Optional, Union

from .constants import PROMPT
from .exceptions import (
    RESULT_CODE_TO_EXCEPTION_MAP,
    RESULT_VERBOSE_CODE_TO_EXCEPTION_MAP,
    CoolMasterNetUnknownError,
    RequirementNotSatisfied,
)
from .structures import UID


class BaseTransport:
    """
    A mode of connection to a CoolMasterNet device.

    Subclass this to implement the various protocols that CoolMasterNet supports - serial, TCP, REST, etc.
    """

    async def command(self, command: str) -> List[str]:
        raise NotImplementedError

    async def unit_command(self, uid: UID, command: str, extra_args: Optional[List[str]] = None):
        raise NotImplementedError

    async def plug_command(self, plug_uid: UID, command: str):
        raise NotImplementedError


class CharTransportBase(BaseTransport):
    """
    A character-based transport such as for serial or TCP-based connections.
    """

    @staticmethod
    def _parse_response(lines: List[str]) -> List[str]:
        last_line = lines[-1]

        if last_line.startswith("ERROR:"):
            result_code = int(last_line.split(":")[1])

            if result_code != 0:
                raise RESULT_CODE_TO_EXCEPTION_MAP.get(
                    result_code, CoolMasterNetUnknownError(f"Unknown result code {result_code}")
                )
        else:
            if last_line != "OK":
                raise RESULT_VERBOSE_CODE_TO_EXCEPTION_MAP.get(
                    last_line, CoolMasterNetUnknownError(f"Unknown result {lines[-1]}")
                )

        return lines[:-1]

    async def unit_command(self, uid: UID, command: str, extra_args: Optional[List[str]] = None):
        """
        Sends a command to a given UID.
        """

        args = [command, str(uid)]

        if extra_args:
            args += extra_args

        return await self.command(" ".join(args))

    async def plug_command(self, plug_uid: UID, command: str):
        """
        Sends a command to a given CoolPlug unit.
        """
        return self._parse_response(await self.unit_command(plug_uid, "plug", extra_args=[command]))


class NetworkTransportMixin:
    """
    A mixin to determine which transports rely on a network connection.
    """


class TCPTransport(NetworkTransportMixin, CharTransportBase):
    """
    A TCP transport for the "Aserver" protocol.

    TODO: this currently opens & closes the connection on each command - maybe we should persist it?
    """

    def __init__(self, host: str, port: Union[int, str] = 10102):
        self.host = host
        self.port = port

    async def command(self, command: str) -> List[str]:
        reader, writer = await asyncio.open_connection(self.host, self.port)

        try:
            await reader.readuntil(PROMPT)

            writer.write((command + "\n").encode("utf-8"))
            response_bytes = await reader.readuntil(b"\r\n" + PROMPT)

            response = response_bytes.decode("utf-8")
            return self._parse_response(response.split("\r\n")[:-1])
        finally:
            writer.close()
            await writer.wait_closed()

    def __str__(self):
        return f"TCP/IP {self.host}:{self.port}"


class RESTTransport(NetworkTransportMixin, BaseTransport):
    """
    A REST transport.

    URL should be the URL to the device, not including the internal /api prefix or anything,
    so if connecting to the device directly it should just be http://host:port/.
    The URL parameter is provided (as opposed to just a host/port combo) to accomodate potential
    reverse-proxies that might map the CoolMasterNet device to a subdirectory from the root URL.

    To hit the API the device's serial number is also needed.

    # TODO: actually implement this and test what's going on with the serial number
    # as I constantly got an error saying it's wrong despite providing the correct one.
    # Maybe it wants the CoolPlug serial numbers?
    """

    def __init__(self, url: str, serial_number: str):
        # TODO: figure out how to do HTTP requests with asyncio
        raise NotImplementedError


class SerialTransport(CharTransportBase):
    """
    A pyserial-backed serial transport backend.

    TODO: this currently opens & closes the port on each command.
    We should maybe persist the connection for some time?

    Example:

        s = SerialTransport('/dev/ttyS0', 9600)

        # serial to network gateway (not currently supported by pyserial-asyncio)
        s = SerialTransport('rfc2217://192.168.0.1:12345', 9600)

        # suppress errors for non-compliant gateways
        s = SerialTransport('rfc2217://192.168.0.1:12345?ign_set_control=True', 9600)

    """

    def __init__(self, url: str, baudrate=9600, **pyserial_kwargs):
        try:
            import serial
            import serial_asyncio
        except ImportError:
            raise RequirementNotSatisfied("Please install pyserial and pyserial-asyncio.")
        else:
            self._pyserial = serial
            self._pyserial_asyncio = serial_asyncio

        self.url = url
        self._baud_rate = baudrate
        self._pyserial_kwargs = pyserial_kwargs

    async def command(self, command: str) -> List[str]:
        reader, writer = await serial_asyncio.open_serial_connection(
            url=self.url, baudrate=self._baud_rate, **self._pyserial_kwargs
        )

        try:
            writer.write((command + "\n").encode("utf-8"))

            # read our own line back; note that even if echo is disabled,
            # the device still follows up any commands with at least a blank line
            # so this works either way
            await reader.readuntil()

            response = await reader.readuntil(b"\r\n" + PROMPT)
            decoded_response = response.decode("utf-8")

            return self._parse_response(decoded_response.split("\r\n")[:-1])
        finally:
            writer.close()
            await writer.wait_closed()

    def __str__(self):
        return f"Serial {self.url} @ {self._baud_rate}"
