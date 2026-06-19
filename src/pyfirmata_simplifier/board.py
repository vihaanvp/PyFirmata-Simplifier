from pyfirmata2 import Arduino

from .motor import Motor
from .exceptions import (
    BoardConnectionError,
    StandbyNotConfiguredError,
)

_active_board = None


class Board:
    """Unified Board for controlling motors and servos on an Arduino.

    Combines the functionality of motor-like-arduino and servo-like-arduino
    into a single interface.  Supports:

    * DC motors via :meth:`attach_motor` (returns a :class:`Motor`)
    * Servos via the global singleton pattern used by :class:`Servo`
    * Optional TB6612FNG-style standby pin
    """

    def __init__(self, port, stby=None):
        global _active_board

        try:
            self._board = Arduino(port)
        except Exception as e:
            raise BoardConnectionError(str(e))

        _active_board = self
        self.motors = []

        if stby is not None:
            self._stby = self._board.get_pin(f"d:{stby}:o")
            self._stby.write(1)
        else:
            self._stby = None

    # ------------------------------------------------------------------
    # Singleton access (used by Servo)
    # ------------------------------------------------------------------

    @staticmethod
    def get_active_board():
        """Return the currently-active Board instance.

        Raises RuntimeError if no Board has been created yet.
        """
        if _active_board is None:
            raise RuntimeError("No board initialized. Create a Board first.")
        return _active_board

    # ------------------------------------------------------------------
    # Motor helpers
    # ------------------------------------------------------------------

    def attach_motor(self, direction1, direction2, pwm, name=None):
        """Create and register a new :class:`Motor`.

        Parameters
        ----------
        direction1 : int
            Digital pin for direction input 1.
        direction2 : int
            Digital pin for direction input 2.
        pwm : int
            PWM-capable pin for speed control.
        name : str, optional
            Human-readable label for the motor.

        Returns
        -------
        Motor
        """
        motor = Motor(self._board, direction1, direction2, pwm, name)
        self.motors.append(motor)
        return motor

    def stop_all(self):
        """Stop every motor registered on this board."""
        for motor in self.motors:
            motor.stop()

    # ------------------------------------------------------------------
    # Standby control (TB6612FNG and similar)
    # ------------------------------------------------------------------

    def wake(self):
        """Bring the motor driver out of standby (STBY = HIGH)."""
        if self._stby is None:
            raise StandbyNotConfiguredError("No STBY pin configured.")
        self._stby.write(1)

    def sleep(self):
        """Put the motor driver into standby (STBY = LOW)."""
        if self._stby is None:
            raise StandbyNotConfiguredError("No STBY pin configured.")
        self._stby.write(0)

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def close(self):
        """Stop all motors, de-assert STBY, and release the Arduino."""
        self.stop_all()
        if self._stby is not None:
            self._stby.write(0)
        self._board.exit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
