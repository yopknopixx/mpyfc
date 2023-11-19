from ppm import Decoder
import time

ppm = Decoder("PPM")

controls = {}

while True:
    controls["roll"] = ppm.get_channel_value(0)
    controls["pitch"] = ppm.get_channel_value(1)
    controls["throttle"] = min(ppm.get_channel_value(2), 1800)
    controls["yaw"] = ppm.get_channel_value(3)
    controls["aux"] = ppm.get_channel_value(4)
    controls["arm"] = ppm.get_channel_value(5)
    print(controls)
    time.sleep(1)
