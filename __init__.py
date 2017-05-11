from ctypes import *
import os
import platform

if platform.architecture()[0] == '32bit':
    arc = '86'
else:
    arc = '64'

_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    'vXboxInterface-x{}'.format(arc),
    'vXboxInterface.dll'
))
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

from .virtual_controller import vController
from .read_state import rController
from .virtual_controller import main as test_virtual
from .read_state import main as test_read
