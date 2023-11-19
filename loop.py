from mpu_spi import MPU6050

# from imu import IMU
from PID import PID_Controller
from pwm import ESC
from ppm import Decoder
import os
from logger import Logger


from machine import Pin
from pyb import SPI
from time import sleep, ticks_us, sleep_us
from led import LED

LOOP_TIME = 2000


class FC:
    def __init__(self) -> None:
        self.mpu_spi = SPI(
            1, SPI.MASTER, baudrate=115200, polarity=1, phase=1, firstbit=SPI.MSB
        )
        self.cs = Pin("A4", Pin.OUT_PP)
        self.mpu = MPU6050(self.mpu_spi, self.cs)
        # self.imu = IMU(self.mpu_spi, self.cs)
        self.pid = PID_Controller(400, -400)
        self.armed = False
        self.motors = [ESC(i) for i in range(4)]
        self.ppm = Decoder("PPM")
        self.controls = {
            "roll": 0,
            "pitch": 0,
            "throttle": 0,
            "yaw": 0,
            "arm": 0,
            "aux": 0,
        }
        self.control_offsets = {
            "roll": 11,
            "pitch": 20,
            "throttle": 33,
            "yaw": 20,
            "arm": 33,
            "aux": 33,
        }
        self.state = {"roll": 0, "pitch": 0, "yaw": 0}
        # self.log_file = open("./logs/"+str(len(os.listdir("./logs"))), "a")
        self.led = LED()
        self.led.blink(0.5)
        self.logger = Logger()
        self.loop_exec_time = 0

    def arm(self) -> None:
        self.armed = True
        for motor in self.motors:
            motor.armed = True
        # self.imu.state["yaw"] = 0
        self.led.blink(0.1)

    def disarm(self) -> None:
        self.armed = False
        for motor in self.motors:
            motor.move(0)
            motor.armed = False
        self.led.blink(0.5)

    def log(self):
        self.log.append(
            [
                self.state["roll"],
                self.state["pitch"],
                self.state["yaw"],
                self.controls["roll"],
                self.controls["pitch"],
                self.controls["yaw"],
                self.controls["throttle"],
                self.loop_exec_time,
            ]
        )

    def update_motors(self, throttle, pid_corrections) -> None:
        if self.armed:
            self.motors[0].move(
                throttle - pid_corrections[0] + pid_corrections[1] + pid_corrections[2]
            )
            self.motors[1].move(
                throttle + pid_corrections[0] - pid_corrections[1] + pid_corrections[2]
            )
            self.motors[2].move(
                throttle + pid_corrections[0] + pid_corrections[1] - pid_corrections[2]
            )
            self.motors[3].move(
                throttle - pid_corrections[0] - pid_corrections[1] - pid_corrections[2]
            )

    def loop(self) -> None:
        loop_start_time = ticks_us()
        self.controls["roll"] = (
            self.ppm.get_channel_value(0) + self.control_offsets["roll"]
        )
        self.controls["pitch"] = (
            self.ppm.get_channel_value(1) + self.control_offsets["pitch"]
        )
        self.controls["throttle"] = (
            min(self.ppm.get_channel_value(2), 1800) + self.control_offsets["throttle"]
        )
        self.controls["yaw"] = (
            self.ppm.get_channel_value(3) + self.control_offsets["yaw"]
        )
        self.controls["aux"] = (
            self.ppm.get_channel_value(4) + self.control_offsets["aux"]
        )
        self.controls["arm"] = (
            self.ppm.get_channel_value(5) + self.control_offsets["arm"]
        )
        # self.state = self.imu.get_state()
        (
            _,
            _,
            _,
            self.state["pitch"],
            self.state["roll"],
            self.state["yaw"],
        ) = self.mpu.get_data()

        self.pid.set_state(
            self.state,
            [
                self.controls["roll"],
                self.controls["pitch"],
                self.controls["yaw"],
                self.controls["throttle"],
            ],
        )
        if not self.armed:
            if self.controls["arm"] > 1600:
                self.arm()
            return

        if self.armed and self.controls["arm"] < 1400:
            self.disarm()
            return

        self.update_motors(self.controls["throttle"], self.pid.outputs)
        self.log()
        self.loop_exec_time = ticks_us() - loop_start_time
        sleep_us(LOOP_TIME - self.loop_exec_time)
        # self.log()


# fc = FC()
# counter  = 0
# while True:
#     t0 = ticks_us()
#     counter+=1
#     fc.loop()
#      print("-" * 10, "Loop Time:", ticks_us() - t0, "-" * 10)
#      print(fc.state)
#     loop_time = ticks_us() - t0
#     if counter == 500:
#         print(fc.controls)
#         counter = 0
#         print(fc.pid.outputs)
#         print(fc.pid.errors)
#         print(fc.state)
#         print("-" * 10, "Loop Time:", loop_time, "-" * 10)
