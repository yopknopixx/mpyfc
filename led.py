import pyb


# create a class for the LED that can blink at a given rate (in seconds) using a timer
class LED:
    def __init__(self):
        self.led = pyb.LED(1)
        self.led.on()
        self.state = False
        self.timer = pyb.Timer(1)

    def toggle(self, timer):
        self.state = not self.state
        if self.state:
            self.led.on()
        else:
            self.led.off()

    def blink(self, rate: int):
        self.timer.init(freq=1 / rate, callback=self.toggle)
