# Contributing to PyFirmata Simplifier

> **Note:** This file has been modified using AI.

Thank you for contributing to **PyFirmata Simplifier** — a unified Arduino-style motor and servo control library for Python, combining `motor-like-arduino` and `servo-like-arduino` into a single package.

## Quick Links

- **PyPI:** `pip install pyfirmata-simplifier`
- **Issues:** GitHub Issues
- **Discussions:** GitHub Discussions

---

## Ways to Contribute

### Bug Reports
- Search existing issues first
- Include: Python version, OS, Arduino board, motor driver / servo model, PyFirmata2 version
- Minimal reproducible example
- Note which wiring pattern you use (motor via `board.attach_motor()` or servo via `Servo().attach()`)

### Feature Requests
- Explain the use case
- Consider impact on both wiring patterns (must not break either)
- Keep it simple — this library focuses on *unified, simple* control

### Pull Requests
**We welcome PRs for:**
- Bug fixes (especially dual-pattern compatibility)
- Additional motor driver / servo features
- Documentation improvements
- Type hints / stubs
- Tests in `tests/`
- Example scripts in `examples/`

**Before submitting:**
1. Run examples: `python examples/combined_usage.py`
2. Test both patterns work on same `Board` instance
3. Follow existing code style (PEP 8, type hints, comprehensive docstrings)
4. Update `CHANGELOG.md` under `## Unreleased`
5. Keep changes focused — one logical change per PR

---

## Development Setup

```bash
git clone https://github.com/vihaanvp/pyfirmata-simplifier.git
cd pyfirmata-simplifier
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

**Requirements:**
- Python 3.8+
- Arduino running StandardFirmata (File → Examples → Firmata → StandardFirmata)
- `pyfirmata2`, `pyserial`

---

## Project Structure

```
pyfirmata-simplifier/
├── src/pyfirmata_simplifier/      # Package source
│   ├── __init__.py                # Public exports + exception hierarchy
│   ├── board.py                   # Unified Board (singleton + attach_motor)
│   ├── motor.py                   # Motor class (from motor-like-arduino)
│   ├── servo.py                   # Servo class (from servo-like-arduino)
│   ├── utils.py                   # delay(), millis()
│   ├── exceptions.py              # Exception hierarchy (backward-compatible)
│   └── version.py                 # __version__
├── examples/                      # Runnable examples
│   ├── single_motor.py
│   ├── dual_motor.py
│   ├── tank_drive.py
│   ├── keyboard_control.py
│   ├── servo_test.py
│   ├── move_smooth.py
│   ├── endless_sweep.py
│   └── combined_usage.py
├── tests/                         # (Add tests here)
├── pyproject.toml                 # Build config (setuptools)
├── requirements.txt
├── README.md
├── AGENTS.md                      # AI assistant guidance
├── LICENSE
└── CONTRIBUTING.md                # This file
```

---

## Critical Architecture: Two Wiring Patterns

**This is the most important constraint.** The library supports two coexisting patterns that **must both continue to work**:

### Pattern 1: Motor (explicit board reference)
```python
board = Board("/dev/ttyUSB0")
motor = board.attach_motor(2, 4, 11)  # Board passes itself to Motor
motor.forward(100)
```
- `Motor.__init__` receives the raw `pyfirmata2.Arduino` instance
- Motor lifecycle managed by `Board.motors` list

### Pattern 2: Servo (global singleton)
```python
Board("/dev/ttyUSB0")  # Creates board, sets module-level _active_board
servo = Servo()
servo.attach(9)        # Servo calls Board.get_active_board()
servo.write(90)
```
- `Servo` accesses board via `Board.get_active_board()` (module-level singleton)
- Only one `Board` can be active at a time

**When making changes, verify BOTH patterns work:**
```python
board = Board(port)
motor = board.attach_motor(2, 4, 11)
servo = Servo()
servo.attach(9)
# Both must work simultaneously on the same board
```

---

## Code Conventions

### Motor API (from motor-like-arduino)
- **Speed:** 0–100 (percentage). Mapped to PyFirmata2 PWM via `speed / 100`.
- **Methods:** `forward(speed)`, `backward(speed)`, `stop()`, `brake()`, `set_speed(speed)`
- **Validation:** `InvalidSpeedError` for non-numeric or out-of-range
- **Pin format:** `d:<pin>:o` (direction), `d:<pin>:p` (PWM)

### Servo API (from servo-like-arduino)
- **Angle:** 0–180 degrees. Clamped via `_validate_and_clamp_angle()` (truncates to `int`).
- **Methods:** `attach(pin)`, `detach()`, `write(angle)`, `read()`, `move_smooth(target, delay_ms)`, `sweep(start, end, step, delay_ms)`
- **State:** `current_angle` tracks last written angle (no hardware read-back)
- **Pin format:** `d:<pin>:s` (Firmata servo protocol)

### Shared
- **Board:** Context manager (`with Board(port) as b:`), `close()`, `stop_all()`, `wake()`/`sleep()` (requires STBY pin)
- **Utilities:** `delay(ms)`, `millis()` — Arduino-like timing
- **Exceptions:** Hierarchy in `exceptions.py` (backward-compatible with `motor-like-arduino`)

---

## Exception Hierarchy (Backward Compatible)

```
PyFirmataSimplifierError
  └─ MotorLikeArduinoError      ← catchable by old motor-like-arduino code
       ├─ InvalidSpeedError
       ├─ BoardConnectionError
       └─ StandbyNotConfiguredError
```

**Do not break this hierarchy.** Existing `motor-like-arduino` code must continue to catch `MotorLikeArduinoError`.

---

## Testing

```bash
# Run examples (requires hardware)
python examples/single_motor.py
python examples/dual_motor.py
python examples/tank_drive.py
python examples/keyboard_control.py
python examples/servo_test.py
python examples/move_smooth.py
python examples/endless_sweep.py
python examples/combined_usage.py   # CRITICAL: tests both patterns together
```

**Test Coverage Gaps (help wanted):**
- Mock PyFirmata2 board for CI testing without hardware
- Dual-pattern stress test (multiple motors + servos on same board)
- Edge cases: STBY pin, context manager cleanup, exception hierarchy

---

## Release Process

Maintainer only:
```bash
# Update version in src/pyfirmata_simplifier/version.py
# Update CHANGELOG.md
git tag vX.Y.Z
git push origin vX.Y.Z
python -m build
python -m twine upload dist/*
```

---

## Related Projects

| Project | Purpose |
|---------|---------|
| [motor-like-arduino](https://github.com/vihaanvp/motor-like-arduino) | Standalone DC motor control |
| [servo-like-arduino](https://github.com/vihaanvp/servo-like-arduino) | Standalone servo control |
| [ultrasonic-like-arduino](https://github.com/vihaanvp/ultrasonic-like-arduino) | HC-SR04 ultrasonic sensor |

When adding features, consider API consistency across all four libraries.

---

## License

By contributing, you agree your contributions are licensed under the MIT License (see [LICENSE](LICENSE)).