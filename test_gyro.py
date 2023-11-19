from pyb import SPI
from machine import Pin
from mpu_spi import MPU6050

spi = SPI(1, SPI.MASTER, baudrate=115200, polarity=1, phase=1, firstbit=SPI.MSB)
cs = Pin("A4", Pin.OUT_PP)
offsets = [-0.3556935, -0.3157556, -0.197359]

mpu = MPU6050(spi, cs)

while True:
    _, _, _, roll, pitch, yaw = mpu.get_data()
    #     print("Roll:\t", roll - offsets[0], "Pitch:\t", pitch - offsets[1], "Yaw:\t", yaw - offsets[2])
    t = [roll, pitch, yaw]
    a = ["Roll", "Pitch", "Yaw"]
    i = t.index(max(t))
    print("Moving:", a[i], end="\r")
