from enum import Enum

PROMPT = b">"


class Mode(Enum):
    COOL = "Cool"
    HEAT = "Heat"
    FAN = "Fan"
    DRY = "Dry"
    AUTO = "Auto"


CM_MODE_MAP = {mode.value: mode for mode in Mode}


class FanMode(Enum):
    VERY_LOW = "VLow"
    LOW = "Low"
    MEDIUM = "Med"
    HIGH = "High"
    VERY_HIGH = "Top"
    AUTO = "Auto"


# returned by "ls" line
CM_FAN_MODE_MAP = {fan_mode.value: fan_mode for fan_mode in FanMode}

# FanMode to "fspeed" argument map
CM_FAN_MODE_FSPEED_ARG_MAP = {fan_mode: fan_mode.value[0].lower() for fan_mode in FanMode}

# "properties" fan mode identifiers to FanMode
CM_PROPS_FAN_MODE_MAP = {fan_mode.value[0].lower(): fan_mode for fan_mode in FanMode}

CM_PROPS_MODE_MAP = {mode.value[0].lower(): mode for mode in Mode}


class LineType(Enum):
    DAIKIN = "DK"
    MITSUBISHI_ELECTRIC = "ME"
    MITSUBISHI_ELECTRIC_M1M2 = "M1M2"
    SANYO = "SA"
    TOSHIBA = "TO"
    PANASONIC = "PN"
    HITACHI = "HT"
    LG = "LG"
    MITSUBISHI_HEAVY_INDUSTRIES = "MH"
    GREE = "GR"
    MIDEA = "MD"
    KENTATSU = "KT"
    TRANE = "TR"
    CHIGO = "CG"
    FUJITSU = "FJ"
    SAMSUNG = "SM"
    TADIRAN_INVERTER = "TI"
    MEITAV = "MT"
    HAIER = "HA"
    BLUESTAR = "BSM"

    KNX = "KNX"

    PLUGBUS = "CH"
    PLUGBUS_WIRELESS = "CHWi"
    PLUGBUS_WIRELESS_CLIENT = "PBWi"  # from CoolPlug's side

    HDL = "HDL"

    MODBUS = "CLMB"

    MODBUS_COOLGATE4 = "CG4"
    MODBUS_COOLGATE5 = "CG5"

    MAC = "MAC"  # seen on CoolPlug

    UNUSED = "Unused"


LINE_TYPE_MAP = {item.value: item for item in LineType}


class QueryDatapoint(Enum):
    ON_OFF = "o"
    MODE = "m"
    FAN_MODE = "f"
    TARGET_TEMPERATURE = "t"
    FAILURE_CODE = "e"
    AMBIENT_TEMPERATURE = "a"
    TARGET_TEMPERATURE_PRECISE = "h"
    LOUVER_POSITION = "s"


class ModeState(Enum):
    COOL = "Cool"
    HEAT = "Heat"
    FAN = "Fan"
    DRY = "Dry"
    AUTO = "Auto"
    AUX_HEAT = "Haux"


class QueryPowerStatus(Enum):
    OFF = 0
    ON = 1


QUERY_MODE_MAPPING = {
    0: ModeState.COOL,
    1: ModeState.HEAT,
    2: ModeState.AUTO,
    3: ModeState.DRY,
    4: ModeState.AUX_HEAT,
    5: ModeState.FAN,
}


class LouverPosition(Enum):
    SWING = "a"
    STOP_SWING = "x"

    HORIZONTAL = "h"
    VERTICAL = "v"

    THIRTY_DEGREES = "3"
    FORTY_FIVE_DEGREES = "4"
    SIXTY_DEGREES = "6"


class LouverPositionState(Enum):
    SWING = "a"
    STOP_SWING = "x"

    HORIZONTAL = "h"
    VERTICAL = "v"

    THIRTY_DEGREES = "3"
    FORTY_FIVE_DEGREES = "4"
    SIXTY_DEGREES = "6"

    NOT_SUPPORTED = "0"


CM_LOUVER_POSITION_STATE_MAP = {pos.value: pos for pos in LouverPositionState}
