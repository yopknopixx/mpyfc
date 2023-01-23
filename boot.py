import pyb
import machine

pyb.country("IN")

from loop import FC

fc = FC()

while True:
    fc.loop()
