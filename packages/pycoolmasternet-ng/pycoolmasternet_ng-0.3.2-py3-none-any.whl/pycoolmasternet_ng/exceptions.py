class CoolMasterNetException(Exception):
    """
    Base class for CoolMasterNet exceptions.
    """


class RequirementNotSatisfied(CoolMasterNetException):
    """
    An extra requirement (library, etc) needs to be installed.
    """


class DeviceDisappearedException(CoolMasterNetException):
    """
    The device we were looking for is no longer on the bus.
    """


class CoolMasterNetRemoteError(CoolMasterNetException):
    """
    Base class for remote device exceptions.
    """


class UIDError:
    """
    Mixin for UID-related errors.
    """


class CoolMasterNetNoUidError(UIDError, CoolMasterNetRemoteError):
    """
    UID not found
    """

    code = 1
    verbose_code = "No UID"


class CoolMasterNetNotStrictUidError(UIDError, CoolMasterNetRemoteError):
    """
    UID must be precise
    """

    code = 2
    verbose_code = "Not Strict UID"


class CoolMasterNetBadFormatError(CoolMasterNetRemoteError):
    """
    Command format is wrong
    """

    code = 3
    verbose_code = "Bad Format"


class CoolMasterNetFailedError(CoolMasterNetRemoteError):
    """
    Command execution failed
    """

    code = 4
    verbose_code = "Failed"


class LineError:
    """
    Mixin for line-related errors.
    """


class CoolMasterNetLineUnusedError(LineError, CoolMasterNetRemoteError):
    """
    Line is unused
    """

    code = 5
    verbose_code = "Line Unused"


class CoolMasterNetUnknownCommandError(CoolMasterNetRemoteError):
    """
    Command is unknown
    """

    code = 6
    verbose_code = "Unknown Command"


class CoolMasterNetBadHvacLineError(LineError, CoolMasterNetRemoteError):
    """
    Line number is wrong
    """

    code = 7
    verbose_code = "Bad HVAC Line"


class CoolMasterNetBadFunctionError(CoolMasterNetRemoteError):
    """
    Wrong function
    """

    code = 8
    verbose_code = "Bad Function"


class CoolMasterNetBadLineTypeError(LineError, CoolMasterNetRemoteError):
    """
    Wrong line type definition
    """

    code = 9
    verbose_code = "Bad Line Type"


class CoolMasterNetBadParameterError(CoolMasterNetRemoteError):
    """
    Command parameter is wrong
    """

    code = 10
    verbose_code = "Bad Parameter"


class CoolMasterNetOkBootRequiredError(CoolMasterNetRemoteError):
    """
    Command execution will be effective after reboot
    """

    code = 11
    verbose_code = "OK, Boot Required!"


class CoolMasterNetBadGpioError(CoolMasterNetRemoteError):
    """
    Wrong GPIO
    """

    code = 12
    verbose_code = "Bad GPIO"


class CoolMasterNetSddpDisabledError(CoolMasterNetRemoteError):
    """
    SDDP module is disabled, enable it to proceed
    """

    code = 13
    verbose_code = "SDDP Disabled"


class CoolMasterNetVirtualAddressInUseError(CoolMasterNetRemoteError):
    """
    Virtual address already in use
    """

    code = 14
    verbose_code = "Virtual Address In Use"


class CoolMasterNetBadPropertyError(CoolMasterNetRemoteError):
    """
    Wrong property
    """

    code = 15
    verbose_code = "Bad Property"


class CoolMasterNetNumberOfLinesExceededError(LineError, CoolMasterNetRemoteError):
    """
    Can't define more line types
    """

    code = 16
    verbose_code = "Number of lines exceeded"


class CoolMasterNetWarningDipSwitchStateIncorrectError(CoolMasterNetRemoteError):
    """
    Dip switch state is incorrect for defined line type
    """

    code = 17
    verbose_code = "Warning! Dip Switch State Incorrect"


class CoolMasterNetSddpNotInitializedError(CoolMasterNetRemoteError):
    """
    SDDP is enabled, but Ethernet link is still down
    """

    code = 18
    verbose_code = "SDDP Not Initialized"


class ModbusError:
    """
    Mixin for Modbus-related errors.
    """


class CoolMasterNetModbusError80(ModbusError, CoolMasterNetRemoteError):
    """
    No response from the addressee
    """

    code = 80
    verbose_code = "ModBus Error:80"


class CoolMasterNetModbusError81(ModbusError, CoolMasterNetRemoteError):
    """
    Big timeout between bytes in received message
    """

    code = 81
    verbose_code = "ModBus Error:81"


class CoolMasterNetModbusError82(ModbusError, CoolMasterNetRemoteError):
    """
    Small timeout between bytes in received message
    """

    code = 82
    verbose_code = "ModBus Error:82"


class CoolMasterNetModbusError83(ModbusError, CoolMasterNetRemoteError):
    """
    Received message with internal timeout
    """

    code = 83
    verbose_code = "ModBus Error:83"


class CoolMasterNetModbusError84(ModbusError, CoolMasterNetRemoteError):
    """
    Received message is too big
    """

    code = 84
    verbose_code = "ModBus Error:84"


class CoolMasterNetModbusError85(ModbusError, CoolMasterNetRemoteError):
    """
    CRC error in received message
    """

    code = 85
    verbose_code = "ModBus Error:85"


class CoolMasterNetModbusError86(ModbusError, CoolMasterNetRemoteError):
    """
    ModBus exception in response
    """

    code = 86
    verbose_code = "ModBus Error:86"


class CoolMasterNetCollisionError(LineError, CoolMasterNetRemoteError):
    """
    Collision in sent command on HVAC line
    """

    code = 100
    verbose_code = "Collision"


class CoolMasterNetUnsupportedFeatureError(CoolMasterNetRemoteError):
    """
    Unsupported command or command's parameter for this HVAC line
    """

    code = 101
    verbose_code = "Unsupported Feature"


class CoolMasterNetIncorrectIndoorTypeError(CoolMasterNetRemoteError):
    """
    Chosen Indoor Unit doesn't support this command or command's parameter
    """

    code = 102
    verbose_code = "Incorrect Indoor Type"


class CoolMasterNetNoAckFromIndoorError(LineError, CoolMasterNetRemoteError):
    """
    Indoor Unit didn't acknowledged sent command
    """

    code = 103
    verbose_code = "No ACK From Indoor"


class CoolMasterNetTimeOutOnReceiveError(LineError, CoolMasterNetRemoteError):
    """
    No response from Indoor Unit
    """

    code = 104
    verbose_code = "Time Out on Receive"


class CoolMasterNetCsErrorInReceivedMessageError(CoolMasterNetRemoteError):
    """
    Check Sum error in received message
    """

    code = 105
    verbose_code = "CS Error In Received Message"


class CoolMasterNetLineInitInProgressError(LineError, CoolMasterNetRemoteError):
    """
    Can't show lines status due to initialization process
    """

    code = 106
    verbose_code = "Line Init In Progress..."


class CoolMasterNetLineError(LineError, CoolMasterNetRemoteError):
    """
    Some error on the HVAC line
    """

    code = 107
    verbose_code = "Line Error"


class CoolMasterNetFeedDisabledError(CoolMasterNetRemoteError):
    """
    Indoor Unit can't receive measured ambient temperature due to its switch position
    """

    code = 108
    verbose_code = "Feed Disabled"


class HDLError:
    """
    Mixin for HDL-related errors.
    """


class CoolMasterNetHdlNotInitializedError(HDLError, CoolMasterNetRemoteError):
    """
    HDL line was not defined or ethernet cable is unplugged
    """

    code = 150
    verbose_code = "HDL Not Initialized"


class CoolMasterNetHdlDbOverflowError(HDLError, CoolMasterNetRemoteError):
    """
    HDL Data Base is full, can't add new configuration
    """

    code = 151
    verbose_code = "HDL DB Overflow"


class CoolMasterNetHdlEthDisabledError(HDLError, CoolMasterNetRemoteError):
    """
    HDL over ethernet disabled
    """

    code = 152
    verbose_code = "HDL Eth Disabled"


class CoolMasterNetUidNotFoundError(UIDError, CoolMasterNetRemoteError):
    """
    Specified Indoor Unit not found in Data Base
    """

    code = 200
    verbose_code = "UID Not Found"


class CoolMasterNetStrictUidNotFoundError(UIDError, CoolMasterNetRemoteError):
    """
    Specified Indoor Unit by uid strict not found in Data Base
    """

    code = 201
    verbose_code = "Strict UID Not Found"


class CoolMasterNetIndoorRemovedError(CoolMasterNetRemoteError):
    """
    Indoor Unit removed from Data Base
    """

    code = 202
    verbose_code = "Indoor Removed"


class CoolMasterNetDbOverflowError(CoolMasterNetRemoteError):
    """
    Indoor Units Data Base is full, can't add new one
    """

    code = 203
    verbose_code = "DB Overflow"


class CoolMasterNetGroupDbOverflowError(CoolMasterNetRemoteError):
    """
    Group Data Base is full, can't add new group
    """

    code = 204
    verbose_code = "Group DB Overflow"


class CoolMasterNetVaDbOverflowError(CoolMasterNetRemoteError):
    """
    Virtual address Data Base is full, can't associate Indoor Unit with new virtual address
    """

    code = 205
    verbose_code = "VA DB Overflow"


class CoolMasterNetFdb5OverflowError(CoolMasterNetRemoteError):
    """
    Properties Data Base is full, can't add new property
    """

    code = 206
    verbose_code = "FDB5 Overflow"


class CoolMasterNetLinkDbOverflowError(CoolMasterNetRemoteError):
    """
    Link Data Base is full, can't link new CoolPlug device with Indoor Unit
    """

    code = 250
    verbose_code = "Link DB Overflow"


class CoolMasterNetNoCoolhubLineError(CoolMasterNetRemoteError):
    """
    CoolHub line not defined, define it to proceed
    """

    code = 251
    verbose_code = "No CoolHub Line"


class CoolMasterNetAutoVisibilityFailedError(CoolMasterNetRemoteError):
    """
    During link creation there was an error on adding visibility props
    """

    code = 252
    verbose_code = "Auto Visibility Failed"


class CoolMasterNetLinkAlreadyExistsError(CoolMasterNetRemoteError):
    """
    CoolPlug device already linked, delete previous link before creating the new one
    """

    code = 253
    verbose_code = "Link already exists"


class CoolMasterNetKnxDbOverflowError(CoolMasterNetRemoteError):
    """
    KNX Data Base is full, can't add new group
    """

    code = 307
    verbose_code = "KNX DB Overflow"


class KNXErrorMixin:
    """
    Mixin for KNX-related errors.
    """


class CoolMasterNetKnxNotConnectedError(KNXErrorMixin, CoolMasterNetRemoteError):
    """
    No connection with KNX chip
    """

    code = 309
    verbose_code = "KNX Not Connected"


class CoolMasterNetKnxLineNotStartedError(KNXErrorMixin, CoolMasterNetRemoteError):
    """
    KNX line not defined
    """

    code = 310
    verbose_code = "KNX Line Not Started"


class CoolMasterNetUnknownError(CoolMasterNetRemoteError):
    """
    Catch-all exception for any error we haven't got a mapping for.

    If you encounter this please open an issue so we can create a proper exception class for it.
    """


RESULT_VERBOSE_CODE_TO_EXCEPTION_MAP = {
    c.verbose_code: c for c in CoolMasterNetRemoteError.__subclasses__() if hasattr(c, "verbose_code")
}

RESULT_CODE_TO_EXCEPTION_MAP = {c.code: c for c in CoolMasterNetRemoteError.__subclasses__() if hasattr(c, "code")}
