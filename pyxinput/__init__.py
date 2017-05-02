from ctypes import *
import os

_root = os.path.dirname(__file__)
if _root:
    _path = _root + '\\vXboxInterface-x64\\vXboxInterface.dll'
else:
    _path = 'vXboxInterface-x64\\vXboxInterface.dll'

_xinput = WinDLL(_path)


class MissingDependancyError(Exception):
    def __init__(self, message):
        self.message = message


if not _xinput.isVBusExists():
    raise MissingDependancyError(
        '''Unable to find VBus Controller.

Please refer to https://github.com/shauleiz/vXboxInterface/releases
or run "ScpVBus-x64/install.bat" in cmd.exe as administrator'''
    )
