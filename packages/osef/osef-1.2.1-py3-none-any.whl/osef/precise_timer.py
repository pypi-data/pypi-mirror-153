"""Precise timer"""
# Standard imports
import time


def sleep_ms(duration: float):
    """Sleep for a precise duration.

    :param duration: Duration to sleep in seconds."""
    end_time = time.perf_counter_ns() + duration * 1000000
    while time.perf_counter_ns() < end_time:
        time.sleep(5e-4)
