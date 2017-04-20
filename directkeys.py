from ctypes import *
import time

xinput = windll.XInput1_4


class Vibration(Structure):
    _fields_ = [("wLeftMotorSpeed", c_uint), ("wRightMotorSpeed", c_uint)]


VIB_ON = Vibration(65535, 65535)
VIB_OFF = Vibration(0, 0)

xinput.XInputSetState.argtypes = [c_uint, POINTER(Vibration)]

for x in range(-100, 100):
    p1 = (100 - abs(x)) / 100
    p2 = 1 - p1
    xinput.XInputSetState(0, Vibration(int(65535 * p1), int(65535 * p2)))
    time.sleep(0.05)

xinput.XInputSetState(0, VIB_OFF)
