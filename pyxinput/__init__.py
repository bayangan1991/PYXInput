from ctypes import *
import os

_root = os.path.dirname(__file__)
_xinput = WinDLL(os.path.join(_root, 'vXboxInterface-x64\\vXboxInterface.dll'))


class MissingDependancyError(Exception):
    def __init__(self, message):
        self.message = message


if not _xinput.isVBusExists():
    raise MissingDependancyError(
        '''Unable to find VBus Controller.

Please refer to https://github.com/shauleiz/vXboxInterface/releases
or run "ScpVBus-x64/install.bat" in cmd.exe as administrator'''
    )
