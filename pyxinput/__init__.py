from ctypes import *
import os
import platform

if platform.architecture()[0] == '32bit':
    print('Windows 32-Bit unsupported')

_path = os.path.join(
    os.path.dirname(__file__),
    'vXboxInterface-x64',
    'vXboxInterface.dll'
)

_xinput = windll.LoadLibrary(_path)


class MissingDependancyError(Exception):
    def __init__(self, message):
        self.message = message


if not _xinput.isVBusExists():
    raise MissingDependancyError(
        '''Unable to find VBus Controller.

Please refer to https://github.com/shauleiz/vXboxInterface/releases
or run "ScpVBus-x64/install.bat" in cmd.exe as administrator'''
    )
