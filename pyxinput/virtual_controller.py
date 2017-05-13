"""Virtual Controller Object for Python

Python Implepentation of vXbox from:
http://vjoystick.sourceforge.net/site/index.php/vxbox"""
from ctypes import *
import os
import platform

if '32' in platform.architecture()[0]:
    arc = '86'
else:
    arc = '64'

_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    'vXboxInterface-x{}'.format(arc),
    'vXboxInterface.dll'
))
_xinput = WinDLL(_path)


class MaxInputsReachedError(Exception):
    """Exception when no inputs are available.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message


class vController(object):
    """Virtual Controller Object
    percent, Bool, Determines if absolute or percentage values are passed"""
    DPAD_OFF = 0
    DPAD_UP = 1
    DPAD_DOWN = 2
    DPAD_LEFT = 4
    DPAD_RIGHT = 8

    def __init__(self, percent=True):
        self.percent = percent
        self.id = 0
        self.PlugIn()

    def __del__(self):
        """Unplug self if object is cleaned up"""
        self.UnPlug()

    @classmethod
    def available_ids(self):
        ids = [x for x in range(
            1, 5) if _xinput.isControllerExists(c_int(x)) == 0]

        return ids

    def PlugIn(self):
        """Take next available controller id and plug in to Virtual USB Bus"""
        ids = self.available_ids()
        if len(ids) == 0:
            raise MaxInputsReachedError('Max Inputs Reached')

        self.id = ids[0]

        _xinput.PlugIn(self.id)
        while self.id in self.available_ids():
            pass

    def UnPlug(self, force=False):
        """Unplug controller from Virtual USB Bus and free up ID"""
        if force:
            _xinput.UnPlugForce(c_uint(self.id))
        else:
            _xinput.UnPlug(c_uint(self.id))
        while self.id not in self.available_ids():
            if self.id == 0:
                break

    def set_value(self, control, value=None):
        """Set a value on the controller
    If percent is True all controls will accept a value between -1.0 and 1.0

    If not then:
        Triggers are 0 to 255
        Axis are -32768 to 32767

    Control List:
        AxisLx          , Left Stick X-Axis
        AxisLy          , Left Stick Y-Axis
        AxisRx          , Right Stick X-Axis
        AxisRy          , Right Stick Y-Axis
        BtnBack         , Menu/Back Button
        BtnStart        , Start Button
        BtnA            , A Button
        BtnB            , B Button
        BtnX            , X Button
        BtnY            , Y Button
        BtnThumbL       , Left Thumbstick Click
        BtnThumbR       , Right Thumbstick Click
        BtnShoulderL    , Left Shoulder Button
        BtnShoulderR    , Right Shoulder Button
        Dpad            , Set Dpad Value (0 = Off, Use DPAD_### Contstants)
        TriggerL        , Left Trigger
        TriggerR        , Right Trigger

    """
        func = getattr(_xinput, 'Set' + control)

        if 'Axis' in control:
            target_type = c_short

            if self.percent:
                target_value = int(32767 * value)
            else:
                target_value = value
        elif 'Btn' in control:
            target_type = c_bool
            target_value = bool(value)
        elif 'Trigger' in control:
            target_type = c_byte

            if self.percent:
                target_value = int(255 * value)
            else:
                target_type = value
        elif 'Dpad' in control:
            target_type = c_int
            target_value = int(value)

        func(c_uint(self.id), target_type(target_value))


def main():
    import time
    cons = []

    print('Testings multiple connections')
    while True:
        print('Connecting Controller:')
        try:
            cons.append(vController())
        except MaxInputsReachedError:
            break
        else:
            print('Available:', vController.available_ids())
            print('This ID:', cons[-1].id)

        time.sleep(1)

    print('Done, disconnecting controllers.')
    del cons
    print('Available:', vController.available_ids())
    time.sleep(2)

    print('Testing Value setting')
    print('Connecting Controller:')
    try:
        con = vController()
    except MaxInputsReachedError:
        print('Unable to connect controller for testing.')
    else:
        print('This ID:', con.id)
        print('Available:', vController.available_ids())
        print('Setting TriggerR and AxisLx:')
        for x in range(11):
            val = x / 10
            print(val)
            con.set_value('TriggerR', val)
            con.set_value('AxisLx', val)
            time.sleep(0.5)

        print('Done, disconnecting controller.')
        del con
        print('Available:', vController.available_ids())
        time.sleep(2)


if __name__ == '__main__':
    main()
