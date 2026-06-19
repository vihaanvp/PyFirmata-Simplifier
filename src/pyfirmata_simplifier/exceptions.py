class PyFirmataSimplifierError(Exception):
    """Base exception for pyfirmata_simplifier."""
    pass


class MotorLikeArduinoError(PyFirmataSimplifierError):
    """Base exception for motor-like-arduino (backward-compatible alias)."""
    pass


class InvalidSpeedError(MotorLikeArduinoError):
    """Raised when speed is outside 0-100."""
    pass


class BoardConnectionError(MotorLikeArduinoError):
    """Raised when the board cannot be reached."""
    pass


class StandbyNotConfiguredError(MotorLikeArduinoError):
    """Raised when wake() or sleep() is called without an STBY pin."""
    pass
