"""Read the current state of Xbox Controllers"""
from ctypes import *

# Xinput DLL
try:
    _xinput = windll.xinput1_4
except OSError as err:
    _xinput = windll.xinput1_3


class _xinput_gamepad(Structure):
    """CType XInput Gamepad Object"""
    _fields_ = [("wButtons", c_ushort), ("left_trigger", c_ubyte),
                ("right_trigger", c_ubyte), ("thumb_lx", c_short),
                ("thumb_ly", c_short), ("thumb_rx", c_short),
                ("thumb_ry", c_short)]

    def __repr__(self):
        fields = [
            'wButtons',
            'left_trigger',
            'right_trigger',
            'thumb_lx',
            'thumb_ly',
            'thumb_rx',
            'thumb_ry'
        ]

        return {field: self.__getattribute__(field) for field in fields}

    def __str__(self):
        return str(self.__repr__())


class _xinput_state(Structure):
    """CType XInput State Object"""
    _fields_ = [("dwPacketNumber", c_uint),
                ("XINPUT_GAMEPAD", _xinput_gamepad)]

    def __repr__(self):
        fields = [
            'dwPacketNumber',
            'XINPUT_GAMEPAD'
        ]

        return {field: self.__getattribute__(field) for field in fields}

    def __str__(self):
        return str(self.__repr__())


class rController(object):
    """XInput Controller State reading object"""

    # All possible button values
    _buttons = {
        'DPAD_UP': 0x0001,
        'DPAD_DOWN': 0x0002,
        'DPAD_LEFT': 0x0004,
        'DPAD_RIGHT': 0x0008,
        'START': 0x0010,
        'BACK': 0x0020,
        'LEFT_THUMB': 0x0040,
        'RIGHT_THUMB': 0x0080,
        'LEFT_SHOULDER': 0x0100,
        'RIGHT_SHOULDER': 0x0200,
        'A': 0x1000,
        'B': 0x2000,
        'X': 0x4000,
        'Y': 0x8000
    }

    def __init__(self, ControllerID):
        """Initialise Controller object"""
        self.ControllerID = ControllerID
        self.dwPacketNumber = c_uint()

    def gamepad(self):
        """Returns the current gamepad state. Buttons pressed is shown as a raw integer value.
        Use rController.buttons() for a list of buttons pressed.
        """
        state = _xinput_state()
        _xinput.XInputGetState(self.ControllerID - 1, pointer(state))
        self.dwPacketNumber = state.dwPacketNumber
        return state.XINPUT_GAMEPAD

    def buttons(self):
        """Returns a list of buttons currently pressed"""
        return [name for name, value in rController._buttons.items()
                if self.gamepad().wButtons & value == value]


def main():
    """Test the functionality of the rController object"""
    import time

    print('Testing controller in position 1:')
    print('Running 3 x 3 seconds tests')

    # Initialise Controller
    con = rController(1)

    # Loop printing controller state and buttons held
    for i in range(3):
        print('State: ', con.gamepad())
        print('Buttons: ', con.buttons())
        time.sleep(3)

    print('Done!')


if __name__ == '__main__':
    main()
