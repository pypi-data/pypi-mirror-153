import time
from enum import Enum
from typing import Optional


class DecayFunction(Enum):
    UNIFORM = 1


class TimedDecay:
    def __init__(self,
                 time_until_zero_ms: float,
                 init_value: float = None,
                 decay_function: DecayFunction = None):
        self.time_until_zero_ms = time_until_zero_ms
        self.start_perf = None
        self.init_value = init_value if init_value else 1
        self.decay_function = decay_function if decay_function else DecayFunction.UNIFORM

        self._r = 1 / self.time_until_zero_ms * 1000

    def set_timer(self, at_time):
        self.start_perf = at_time

    def check(self, at_time) -> Optional[float]:
        if self.start_perf is None:
            return None
        t = at_time - self.start_perf

        if self.decay_function == DecayFunction.UNIFORM:
            val = max((1 - self._r * t), 0) * self.init_value
        else:
            raise ValueError(f"Unhandled decay_function type")

        return val

    @property
    def end_time(self):
        if not self.start_perf:
            return None

        return self.start_perf + self.time_until_zero_ms / 1000

    def progress_time(self, at_time):
        if not self.start_perf:
            return None

        return min((at_time - self.start_perf) / (self.end_time - self.start_perf), 1)

    def progress_val(self, at_time):
        if not self.start_perf:
            return None

        return min((self.init_value - self.check(at_time)) / (self.init_value))


class Timer:
    def __init__(self,
                 time_ms: int,
                 start_on_init: bool = False
                 ):
        self._time_ms = time_ms
        self._decayer: Optional[TimedDecay] = None

        if start_on_init:
            self.reset()

    def reset(self, time_ms: int = None):
        if time_ms:
            self._time_ms = time_ms

        self._decayer = TimedDecay(self._time_ms)
        self._decayer.set_timer(time.perf_counter())

    @property
    def finished(self) -> bool:
        # expect this to return True if the timer has reached zero, False o/w
        if self._decayer:
            return self._decayer.check(time.perf_counter()) == 0

        return False

    @property
    def start_perf(self):
        if not self._decayer:
            return None

        return self._decayer.start_perf

    @property
    def progress(self):
        if not self._decayer:
            return None

        return self._decayer.progress_time(time.perf_counter())

    @property
    def time_ms(self):
        return self._time_ms

if __name__ == "__main__":
    start = time.perf_counter()

    timer = Timer(3000, start_on_init=True)

    has_reset = False
    while True:
        print(timer.finished)
        time.sleep(.5)
        if time.perf_counter() - start > 10 and not has_reset:
            timer.reset()
            has_reset = True
            print("reset")

