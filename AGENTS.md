# AGENTS.md — PyFirmata Simplifier

Small single-package Python library (~300 LOC) wrapping PyFirmata2 for Arduino-style motor and servo control.

## Architecture

- **`src/pyfirmata_simplifier/`** — the only package. `setuptools` with `find-packages` scoped to `src/`.
- **`Board`** (`board.py`) — wraps a pyfirmata2 `Arduino` connection. Two wiring patterns coexist:
  - **Motors** — created via `Board.attach_motor()`, which passes the raw `self._board` (pyfirmata2 `Arduino`) into `Motor.__init__`.
  - **Servos** — created standalone (`Servo()`), then access the board via a module-level singleton: `import pyfirmata_simplifier.board as board_module` → `board_module.Board.get_active_board()`. Only one `Board` can be active at a time.
- **No tests, no CI, no linters, no type checker, no formatter config** exist in this repo.
- `from pyfirmata_simplifier import *` works (explicit `__all__`).

## Developer commands

```powershell
# Editable install
pip install -e .

# Build sdist + wheel
python -m build

# Run any example directly
python examples/single_motor.py
```

No test runner, no lint command.

## API gotchas

- **Motor speed** is 0–100 (percentage). Internally mapped to pyfirmata2 PWM via `speed / 100`.
- **Servo angle** is clamped to [0, 180]. `_validate_and_clamp_angle()` casts to `int` (truncates, not rounds) then applies `max(0, min(180, …))`.
- **`Servo.read()`** raises `RuntimeError` if `write()` has never been called (no hardware read-back).
- **`Servo.sweep()`** requires `step > 0`; raises `ValueError` otherwise.
- **`Servo.attach(pin)`** requires `Board(...)` to have been called first, or it raises `RuntimeError`.
- **`Board.wake()`/`sleep()`** require `stby=` pin to have been passed in constructor; otherwise raise `StandbyNotConfiguredError`.

## Exception hierarchy (backward-compatible)

```
PyFirmataSimplifierError
  └─ MotorLikeArduinoError      ← still catchable by old motor-like-arduino code
       ├─ InvalidSpeedError
       ├─ BoardConnectionError
       └─ StandbyNotConfiguredError
```

## Port conventions (not hard-coded, but expected by examples)

| OS      | Typical port        |
|---------|---------------------|
| Linux   | `/dev/ttyUSB0`      |
| macOS   | `/dev/tty.usbserial-*` |
| Windows | `COM3`              |

## Key constraint for agents

If adding features: **do not break the two wiring patterns** above. Motor users call `board.attach_motor()`; servo users call `Board(...)` then `Servo().attach(pin)`. Both must continue to work on the same `Board` instance.
