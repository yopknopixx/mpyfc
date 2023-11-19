import pyb
import time

pyb.country("IN")

# time.sleep(15)
# if not pyb.USB_VCP().isconnected():
from loop import FC

fc = FC()
while True:
    fc.loop()
