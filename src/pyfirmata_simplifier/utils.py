import time


def delay(ms):
    """Pause execution for *ms* milliseconds (Arduino-style)."""
    time.sleep(ms / 1000)


def millis():
    """Return the number of milliseconds since the epoch."""
    return int(time.time() * 1000)
