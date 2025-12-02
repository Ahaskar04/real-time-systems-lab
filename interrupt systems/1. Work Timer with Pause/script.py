from enum import Enum, auto

class TimerState(Enum):
    STOPPED = auto()
    RUNNING = auto()
    PAUSED = auto()

import time

class WorkTimer:
    def __init__(self, total_duration: float):
        self.total_duration = total_duration  # invariant
        self.state = TimerState.STOPPED

        self.elapsed_time = 0.0               # accumulated work time
        self.last_start_timestamp = None      # only valid while RUNNING

    def start(self) -> bool:
        if self.state != TimerState.STOPPED:
            return False

        self.elapsed_time = 0.0
        self.last_start_timestamp = time.time()
        self.state = TimerState.RUNNING
        return True

    def pause(self) -> bool:
        if self.state != TimerState.RUNNING:
            return False

        now = time.time()
        self.elapsed_time += now - self.last_start_timestamp

        self.last_start_timestamp = None
        self.state = TimerState.PAUSED
        return True

    def resume(self) -> bool:
        if self.state != TimerState.PAUSED:
            return False

        self.last_start_timestamp = time.time()
        self.state = TimerState.RUNNING
        return True

    def get_elapsed_time(self) -> float:
        if self.state == TimerState.RUNNING:
            return (
                self.elapsed_time +
                (time.time() - self.last_start_timestamp)
            )

        return self.elapsed_time

    def is_finished(self) -> bool:
        return self.get_elapsed_time() >= self.total_duration

