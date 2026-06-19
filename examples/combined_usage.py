"""Example: using both a DC motor and a servo from the same board."""
import time

from pyfirmata_simplifier import Board, Servo, delay

board = Board("/dev/ttyUSB0")

# --- DC motor on pins 2, 4, 11 ---
motor = board.attach_motor(2, 4, 11, "drive")

# --- Servo on pin 9 ---
servo = Servo()
servo.attach(9)

# Drive forward while sweeping the servo
motor.forward(75)

for angle in range(0, 181, 10):
    servo.write(angle)
    delay(200)

motor.stop()

time.sleep(1)

# Drive backward while sweeping back
motor.backward(50)

for angle in range(180, -1, -10):
    servo.write(angle)
    delay(200)

motor.stop()

board.close()
print("Done!")
