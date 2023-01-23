from pyb import Timer, Pin

esc_pins = ["PWM1", "PWM2", "PWM3", "PWM4"]
esc_pins_timers = [3, 3, 2, 2]
esc_pins_channels = [3, 4, 4, 3]
esc_trim = [0, 0, 0, 0]


class ESC:
    freq_min = 950
    freq_max = 2000

    def __init__(self, index):
        self.timer = Timer(esc_pins_timers[index], prescaler=83, period=19999)
        self.channel = self.timer.channel(
            esc_pins_channels[index], Timer.PWM, pin=Pin(esc_pins[index])
        )
        self.trim = esc_trim[index]
        self.armed = False

    def move(self, freq):
        if self.armed:
            freq = min(self.freq_max, max(self.freq_min, freq + self.trim))
            self.channel.pulse_width(int(freq))

    def __del__(self):
        self.timer.deinit()
