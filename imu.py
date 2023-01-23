# this is a program for an inertial measurement unit (IMU) using the MPU6050
# sensor. It uses the SPI interface to communicate with the sensor.
# This program will get raw acceleration (g) and gyro (deg/s) data from the sensor
# and calculate the roll and pitch angles by combining the gyro and acceleration data
# using a complementary filter.

import pyb
from pyb import SPI
from time import sleep_us, ticks_us
from mpu_spi import MPU6050
import math


@micropython.native
class IMU:
    def __init__(self, spi, cs):
        self.mpu = MPU6050(spi, cs)
        self.gyro = {"x": 0.0, "y": 0.0, "z": 0.0}
        self.accel = {"x": 0.0, "y": 0.0, "z": 0.0}
        self.state = {"roll": 0.0, "pitch": 0.0, "yaw": 0.0}
        self.last_time = ticks_us()

    def get_data(self):
        (
            self.accel["x"],
            self.accel["y"],
            self.accel["z"],
            self.gyro["x"],
            self.gyro["y"],
            self.gyro["z"],
        ) = self.mpu.get_data()

    def get_angles(self):
        self.get_data()
        # if the refresh rate is 500Hz (or the loop time is 2ms) so dt = 0.002
        dt = (ticks_us() - self.last_time) / 1000000  # convert to seconds
        # print(dt)
        self.last_time = ticks_us()
        # calculate roll and pitch angles from the accelerometer data
        acc_angle_pitch = (
            180 * math.atan2(self.accel["y"], self.accel["z"]) / math.pi
        )  # roll angle
        acc_angle_roll = (
            180
            * math.atan2(
                -self.accel["x"], math.sqrt(self.accel["y"] ** 2 + self.accel["z"] ** 2)
            )
            / math.pi
        )  # pitch angle

        # integrate the gyro data -> int(angularSpeed) = angle
        self.state["roll"] = (
            self.state["roll"] + self.gyro["y"] * dt
        ) * 0.99 + acc_angle_roll * 0.01
        self.state["pitch"] = (
            self.state["pitch"] + self.gyro["x"] * dt
        ) * 0.99 + acc_angle_pitch * 0.01
        self.state["yaw"] += self.gyro["z"] * dt

    def get_state(self):
        self.get_angles()
        return self.state
