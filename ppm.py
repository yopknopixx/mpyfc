import pyb
import micropython

micropython.alloc_emergency_exception_buf(200)


class Decoder:
    def __init__(self, pin: str):
        self.pin = pin
        self.current_channel = -1
        self.channels = {i: 0 for i in range(10)}  # up to 10 channels
        self.timer = pyb.Timer(
            4, prescaler=83, period=0x3FFFFFFF
        )  # prescaler divides peripheral clock frequency, period is when the counter is incremented
        self.timer.counter(0)
        # clear any previously set interrupt
        pyb.ExtInt(pin, pyb.ExtInt.IRQ_RISING, pyb.Pin.PULL_NONE, None)
        self.ext_int = pyb.ExtInt(
            pin, pyb.ExtInt.IRQ_RISING, pyb.Pin.PULL_NONE, self._callback
        )

    def _callback(self, line) -> None:
        ticks = self.timer.counter()
        if ticks > 2100:
            self.current_channel = 0
        elif self.current_channel > -1:
            self.channels[self.current_channel] = ticks
            self.current_channel += 1
        self.timer.counter(0)

    def get_channel_value(self, channel: int) -> int:
        return self.channels[channel]

    def enable(self):
        self.ext_int.enable()

    def disable(self):
        self.ext_int.disable()
