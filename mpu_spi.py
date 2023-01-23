from machine import Pin
from pyb import SPI
from time import sleep, ticks_us

# define all registers
# Constants for MPU-6000 registers
USER_CTRL = 0x6A
SIGNAL_PATH_RESET = 0x68
PWR_MGMT_1 = 0x6B
PWR_MGMT_2 = 0x6C
SMPLRT_DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
ACCEL_CONFIG = 0x1C
FIFO_EN = 0x23
INT_ENABLE = 0x38
INT_STATUS = 0x3A
ACCEL_XOUT_H = 0x3B
ACCEL_XOUT_L = 0x3C
ACCEL_YOUT_H = 0x3D
ACCEL_YOUT_L = 0x3E
ACCEL_ZOUT_H = 0x3F
ACCEL_ZOUT_L = 0x40
TEMP_OUT_H = 0x41
TEMP_OUT_L = 0x42
GYRO_XOUT_H = 0x43
GYRO_XOUT_L = 0x44
GYRO_YOUT_H = 0x45
GYRO_YOUT_L = 0x46
GYRO_ZOUT_H = 0x47
GYRO_ZOUT_L = 0x48


@micropython.native
class MPU6050:
    def __init__(self, spi, cs):
        self.spi = spi
        self.cs = cs
        self.status = bytearray(1)
        self.init()
        self.gyro_offset = {"x": -0.9586164, "y": -0.3348694, "z": 0.6497115}

    def read(self, reg, buf):
        self.cs.low()
        self.spi.send(reg | 0x80)
        self.spi.recv(buf, timeout=1000)
        self.cs.high()

    def write(self, reg, val):
        self.cs.low()
        self.spi.send(reg)
        self.spi.send(val)
        self.cs.high()

    def read_reg(self, reg):
        self.cs.low()
        self.spi.send(reg | 0x80)
        self.spi.recv(self.status, timeout=1000)
        self.cs.high()
        return self.status[0]

    def write_reg(self, reg, val):
        self.cs.low()
        self.spi.send(reg)
        self.spi.send(val)
        self.cs.high()

    def spi_write_bit(self, register, bit, value):
        # read the current value from the specified register
        current_value = bytearray(1)
        self.read(register, current_value)
        current_value = current_value[0]
        # set or clear the bit based on the value argument
        # print("Curr:", current_value)
        if value:
            current_value |= 1 << bit
        else:
            current_value &= ~(1 << bit)
        # write the modified value back to the register
        # print("Mod:", current_value)
        self.write_reg(register, current_value)

    def init(self):
        # set cs high
        self.cs.high()
        # reset the chip
        self.spi_write_bit(PWR_MGMT_1, 7, 1)
        sleep(0.1)
        # disable sleep mode
        self.spi_write_bit(PWR_MGMT_1, 6, 0)
        # Set GYRO_RESET = ACCEL_RESET = TEMP_RESET = 1 (register SIGNAL_PATH_RESET)
        self.spi_write_bit(SIGNAL_PATH_RESET, 2, 1)
        self.spi_write_bit(SIGNAL_PATH_RESET, 1, 1)
        self.spi_write_bit(SIGNAL_PATH_RESET, 0, 1)
        sleep(0.1)
        # Disable I2C interface (register USER_CTRL)
        self.spi_write_bit(USER_CTRL, 5, 1)
        # Disable FIFO (register USER_CTRL and FIFO_EN)
        self.spi_write_bit(USER_CTRL, 6, 0)
        self.spi_write_bit(FIFO_EN, 6, 0)
        # Set Gyro Full Scale Range to 500 deg/s (register GYRO_CONFIG)
        self.spi_write_bit(GYRO_CONFIG, 4, 0)
        self.spi_write_bit(GYRO_CONFIG, 3, 1)
        # Set Accelerometer Full Scale Range to +-8g (register ACCEL_CONFIG)
        self.spi_write_bit(ACCEL_CONFIG, 4, 1)
        self.spi_write_bit(ACCEL_CONFIG, 3, 0)
        # Set Sample Rate Divider to 0 (register SMPLRT_DIV)
        self.write_reg(SMPLRT_DIV, 0)
        # Set Digital Low Pass Filter to ~43Hz (register CONFIG)
        self.spi_write_bit(CONFIG, 0, 1)
        self.spi_write_bit(CONFIG, 1, 1)

    def get(self):
        data = bytearray(14)
        self.read(ACCEL_XOUT_H, data)
        # print(data)
        return data

    def bytes_to_int(self, firstbyte, secondbyte):
        if not firstbyte & 0x80:
            return firstbyte << 8 | secondbyte
        return -(((firstbyte ^ 255) << 8) | (secondbyte ^ 255) + 1)

    def process_data(self, data):
        # 16-bit signed integer
        ax = self.bytes_to_int(data[0], data[1])
        ay = self.bytes_to_int(data[2], data[3])
        az = self.bytes_to_int(data[4], data[5])
        temp = self.bytes_to_int(data[6], data[7])
        gx = self.bytes_to_int(data[8], data[9])
        gy = self.bytes_to_int(data[10], data[11])
        gz = self.bytes_to_int(data[12], data[13])
        # print(ax, ay, az, gx, gy, gz, temp)
        return ax, ay, az, gx, gy, gz, temp

    def scale_data(self, data):
        ax, ay, az, gx, gy, gz, temp = self.process_data(data)
        ax = ax / 4096.0
        ay = ay / 4096.0
        az = az / 4096.0
        gx = (gx / 65.5) - (self.gyro_offset["x"])
        gy = gy / 65.5 - (self.gyro_offset["y"])
        gz = gz / 65.5 - (self.gyro_offset["z"])
        temp = temp / 340.0 + 36.53
        return ax, ay, az, gx, gy, gz, temp

    def get_data(self):
        data = self.get()
        ax, ay, az, gx, gy, gz, temp = self.scale_data(data)
        return ax, ay, az, gx, gy, gz

    def print_data(self):
        t = ticks_us()
        data = self.get()
        t_diff = ticks_us() - t
        ax, ay, az, gx, gy, gz, temp = self.scale_data(data)
        print(
            "Accel:  X: {:6.2f}  Y: {:6.2f}  Z: {:6.2f}  Gyro:  X: {:6.2f}  Y: {:6.2f}  Z: {:6.2f}  Temp: {:6.2f}  Time: {:6.2f}us".format(
                ax, ay, az, gx, gy, gz, temp, t_diff
            )
        )
