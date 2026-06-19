# PyFirmata Simplifier

Arduino-style DC motor **and** servo control for Python, built on PyFirmata2.

This library combines the functionality of **motor-like-arduino** and
**servo-like-arduino** into a single, unified package.  Control motors and
servos connected to an Arduino running StandardFirmata using simple,
intuitive commands inspired by the Arduino ecosystem.

```python
from pyfirmata_simplifier import Board, Motor, Servo, delay

board = Board("/dev/ttyUSB0")

# --- DC motor ---
motor = board.attach_motor(2, 4, 11)
motor.forward(100)

# --- Servo ---
servo = Servo()
servo.attach(9)
servo.write(90)
```

---

## Why PyFirmata Simplifier?

Most Python motor and servo libraries expose low-level driver details.

PyFirmata Simplifier focuses on simplicity:

```python
motor.forward(100)
motor.backward(50)
motor.stop()
motor.brake()

servo.write(90)
servo.move_smooth(180)
servo.sweep(start=0, end=180, step=1, delay_ms=15)
```

No PWM calculations. No complicated setup. Just simple control.

---

## Installation

```bash
pip install pyfirmata-simplifier
```

Or install from source:

```bash
git clone https://github.com/VihaanParlikar/pyfirmata-simplifier.git
cd pyfirmata-simplifier
pip install -r requirements.txt
pip install -e .
```

---

## Quick Start

### DC Motor

```python
from pyfirmata_simplifier import Board
import time

board = Board("/dev/ttyUSB0")

motor = board.attach_motor(
    2,  # Direction Pin 1
    4,  # Direction Pin 2
    11  # PWM Pin
)

motor.forward(100)
time.sleep(2)
motor.stop()

board.close()
```

### Servo

```python
from pyfirmata_simplifier import Board, Servo, delay

Board("/dev/ttyUSB0")

servo = Servo()
servo.attach(9)

servo.write(90)
delay(1000)

servo.sweep(start=0, end=180, step=1, delay_ms=15)
```

### Both Together

```python
from pyfirmata_simplifier import Board, Motor, Servo, delay
import time

board = Board("/dev/ttyUSB0")

# Motor
motor = board.attach_motor(2, 4, 11)
motor.forward(75)

# Servo
servo = Servo()
servo.attach(9)
servo.write(45)

time.sleep(2)
motor.stop()
board.close()
```

---

## Multiple Motors

```python
from pyfirmata_simplifier import Board

board = Board("/dev/ttyUSB0")

left = board.attach_motor(2, 4, 11, "left")
right = board.attach_motor(5, 3, 10, "right")

left.forward(50)
right.forward(100)

board.stop_all()
board.close()
```

---

## Features

### DC Motor Control
- Simple Arduino-inspired API
- Percentage-based speed control (0-100)
- Forward and backward movement
- Stop and brake support
- Multiple motors per board
- Optional TB6612FNG standby support (`stby=` parameter)
- Automatic speed validation

### Servo Control
- Arduino-style syntax
- Servo attach / detach
- Absolute angle write
- Smooth movement (`move_smooth`)
- Sweep functionality (`sweep`)
- `delay()` and `millis()` utilities

### General
- Built on top of PyFirmata2
- Unified Board class — one connection for motors **and** servos
- Safe board shutdown (`close()` / context manager)
- Custom exceptions

---

## Supported Motor Drivers

Any motor driver that uses 2 direction pins and 1 PWM pin, including:

- TB6612FNG
- L293D
- L298N
- MX1508

---

## Optional TB6612FNG Standby Support

```python
board = Board("/dev/ttyUSB0", stby=6)
board.sleep()
board.wake()
```

---

## Included Examples

The `examples/` directory contains ready-to-run scripts:

| Example                  | Description                          |
|--------------------------|--------------------------------------|
| `single_motor.py`        | Forward, wait, stop                  |
| `dual_motor.py`          | Two motors at different speeds       |
| `tank_drive.py`          | Tank-drive style control             |
| `keyboard_control.py`    | Interactive keyboard control         |
| `servo_test.py`          | Write and sweep a servo              |
| `move_smooth.py`         | Smooth servo movement                |
| `endless_sweep.py`       | Continuous servo sweep               |
| `combined_usage.py`      | Motor and servo on the same board    |

---

## Requirements

- Python 3.8+
- Arduino running StandardFirmata (File > Examples > Firmata > StandardFirmata)

---

## Author

Vihaan Parlikar
