from .exceptions import InvalidSpeedError


class Motor:
    """DC motor controlled via two direction pins and one PWM pin.

    Speed is expressed as a percentage (0-100).  The underlying
    pyfirmata2 PWM value is normalised automatically.
    """

    def __init__(self, board, direction1, direction2, pwm, name=None):
        self._direction1 = board.get_pin(f"d:{direction1}:o")
        self._direction2 = board.get_pin(f"d:{direction2}:o")
        self._pwm = board.get_pin(f"d:{pwm}:p")

        self.name = name
        self._speed = 0
        self._direction = "stopped"

    def __repr__(self):
        return (
            f"Motor("
            f"direction='{self._direction}', "
            f"speed={self._speed})"
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _validate_speed(self, speed):
        if not isinstance(speed, (int, float)):
            raise InvalidSpeedError("Speed must be a number.")
        if not 0 <= speed <= 100:
            raise InvalidSpeedError("Speed must be between 0 and 100.")

    def _apply_speed(self, speed):
        self._pwm.write(speed / 100)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def speed(self):
        """Current speed (0-100)."""
        return self._speed

    @speed.setter
    def speed(self, speed):
        self.set_speed(speed)

    @property
    def direction(self):
        """Current direction: 'forward', 'backward', 'stopped', or 'braked'."""
        return self._direction

    # ------------------------------------------------------------------
    # Movement commands
    # ------------------------------------------------------------------

    def forward(self, speed=100):
        """Run the motor forward at *speed* (0-100)."""
        self._validate_speed(speed)
        self._direction1.write(1)
        self._direction2.write(0)
        self._apply_speed(speed)
        self._speed = speed
        self._direction = "forward"

    def backward(self, speed=100):
        """Run the motor backward at *speed* (0-100)."""
        self._validate_speed(speed)
        self._direction1.write(0)
        self._direction2.write(1)
        self._apply_speed(speed)
        self._speed = speed
        self._direction = "backward"

    def stop(self):
        """Stop the motor (coast)."""
        self._direction1.write(0)
        self._direction2.write(0)
        self._apply_speed(0)
        self._speed = 0
        self._direction = "stopped"

    def brake(self):
        """Brake the motor by shorting the driver outputs."""
        self._direction1.write(1)
        self._direction2.write(1)
        self._apply_speed(0)
        self._speed = 0
        self._direction = "braked"

    def set_speed(self, speed):
        """Adjust the motor speed without changing its direction."""
        self._validate_speed(speed)
        self._apply_speed(speed)
        self._speed = speed
