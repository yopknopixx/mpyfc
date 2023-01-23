from mpu_spi import MPU6050
from imu import IMU
from PID import PID_Controller
from PWM import ESC
from ppm import Decoder
import os


from machine import Pin
from pyb import SPI
from time import sleep, ticks_us


class FC:
    def __init__(self) -> None:
        self.mpu_spi = SPI(
            1, SPI.MASTER, baudrate=115200, polarity=1, phase=1, firstbit=SPI.MSB
        )
        self.cs = Pin("A4", Pin.OUT_PP)
        self.imu = IMU(self.mpu_spi, self.cs)
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
        self.state = {"roll": 0, "pitch": 0, "yaw": 0}
        # self.log_file = open("./logs/"+str(len(os.listdir("./logs"))), "a")

    def arm(self) -> None:
        self.armed = True
        for motor in self.motors:
            motor.armed = True
        self.imu.state["yaw"] = 0

    def disarm(self) -> None:
        self.armed = False
        for motor in self.motors:
            motor.move(0)
            motor.armed = False

    def log(self):
        self.log_file.write(
            f'{self.state["roll"]}, {self.state["pitch"]}, {self.state["yaw"]}, {self.controls["roll"]}, {self.controls["pitch"]}, {self.controls["yaw"]}, {self.controls["throttle"]}, {self.controls["arm"]}, {self.controls["aux"]}, {self.pid.outputs[0]}, {self.pid.outputs[1]}, {self.pid.outputs[2]} \n'
        )

    def update_motors(self, throttle, pid_corrections) -> None:
        if self.armed:
            self.motors[0].move(
                throttle - pid_corrections[0] + pid_corrections[1] + pid_corrections[2]
            )
            self.motors[1].move(
                throttle + pid_corrections[0] + pid_corrections[1] - pid_corrections[2]
            )
            self.motors[2].move(
                throttle + pid_corrections[0] - pid_corrections[1] + pid_corrections[2]
            )
            self.motors[3].move(
                throttle - pid_corrections[0] - pid_corrections[1] - pid_corrections[2]
            )

    def loop(self) -> None:
        self.controls["roll"] = self.ppm.get_channel_value(0)
        self.controls["pitch"] = self.ppm.get_channel_value(1)
        self.controls["throttle"] = self.ppm.get_channel_value(2)
        self.controls["yaw"] = self.ppm.get_channel_value(3)
        self.controls["aux"] = self.ppm.get_channel_value(4)
        self.controls["arm"] = self.ppm.get_channel_value(5)
        self.state = self.imu.get_state()
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
        # self.log()


fc = FC()

while True:
    t0 = ticks_us()
    fc.loop()
#     print("Loop Time:", ticks_us() - t0)
#     print(fc.state)
#     print(fc.controls)
#     print(fc.pid.outputs)
#     print(fc.pid.errors)
