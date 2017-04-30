import ctypes
import threading
import time

buttons = {
    'GAMEPAD_DPAD_UP', 0x0001
    'GAMEPAD_DPAD_DOWN', 0x0002
    'GAMEPAD_DPAD_LEFT', 0x0004
    'GAMEPAD_DPAD_RIGHT', 0x0008
    'GAMEPAD_START', 0x0010
    'GAMEPAD_BACK', 0x0020
    'GAMEPAD_LEFT_THUMB', 0x0040
    'GAMEPAD_RIGHT_THUMB', 0x0080
    'GAMEPAD_LEFT_SHOULDER', 0x0100
    'GAMEPAD_RIGHT_SHOULDER', 0x0200
    'GAMEPAD_A', 0x1000
    'GAMEPAD_B', 0x2000
    'GAMEPAD_X', 0x4000
    'GAMEPAD_Y', 0x8000
}

xinput = ctypes.windll.xinput1_3


class xinput_gamepad(ctypes.Structure):
    _fields_ = [("wButtons", ctypes.c_ushort), ("left_trigger", ctypes.c_ubyte),
                ("right_trigger", ctypes.c_ubyte), ("thumb_lx", ctypes.c_short),
                ("thumb_ly", ctypes.c_short), ("thumb_rx", ctypes.c_short),
                ("thumb_ry", ctypes.c_short)]


class xinput_state(ctypes.Structure):
    _fields_ = [("dwPacketNumber", ctypes.c_uint),
                ("XINPUT_GAMEPAD", xinput_gamepad)]


class xinput_vibration(ctypes.Structure):
    _fields_ = [("wLeftMotorSpeed", ctypes.c_ushort),
                ("wRightMotorSpeed", ctypes.c_ushort)]


def main():
    state = xinput_state()
    xinput.XInputGetState(0, ctypes.pointer(state))
    print(bin(state.XINPUT_GAMEPAD.wButtons))


if __name__ == '__main__':
    main()
