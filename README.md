# PYXInput

A Python Library for emulating xbox controllers on Windows as well as reading the state of controllers using standard xinput. This is an adaptation of the the vXbox by vJoy. I have made some changes to [vXboxInterface.dll](https://github.com/bayangan1991/vXboxInterface) that I feel make it easier to work with. The original can be found at [vXboxInterface](http://vjoystick.sourceforge.net/site/index.php/vxbox) but be aware it will not function with the project.

## Getting Started

These instructions will get you a copy of the project up and running on your 64-Bit local machine for development and testing purposes.

### Prerequisites

I have only tested this project on `Windows 64-Bit` with `Python 3.6.1`. I can not guarantee that it will work on any other combination of systems.

This project requires the installation of `ScpVBus` if you intend on using the Virtual Controller object. It can be installed by following the below. For ease I have included it in this project. More information can be found at [ScpVBus](https://github.com/nefarius/ScpVBus).


1. Open `cmd.exe` as administator
2. `cd` in the [ScpVBus-x64](/ScpVBus-x64) directory
3. Execute [install.bat](/ScpVBus-x64/install.bat)

If successful you will receive the following message

```
Device node created. Install is complete when drivers are installed...
Updating drivers for Root\ScpVBus from {Location}\PYXInput\ScpVBus-x64\ScpVBus.inf.
Drivers installed successfully.
```

### Installing

To install run the following command:

```
pip install git+https://github.com/bayangan1991/PYXInput.git
```

To uninstall:

```
pip uninstall PYXInput
```

## Running the tests

This library contains two main modules. [virtual_controller](/virtual_controller.py) is for creating a virtual controller.

[read_state](/read_state.py) is for reading the current state of any xbox controller (virtual or real)

### Testing

Each of these modules has a `main()` defintion which will test functionality.

```
python virtual_controller.py
```

Successful Output:
```
Connecting Controller:
This ID: 1
Available: [2, 3, 4]
Setting TriggerR and AxisLx:
0.0
0.1
0.2
0.3
0.4
0.5
0.6
0.7
0.8
0.9
1.0
Done, disconnecting controller.
Available: [1, 2, 3, 4]
```

### And coding style tests

Each use case of this library can be initialsed as an object

```python
from PYXInput.virtual_controller import vController
from PYXInput.read_state import rController

MyVirtual = vController()

MyRead = rController(1)

MyVirtual.set_value('BtnA', 1)
MyVirtual.set_value('AxisLx', -0.5)

print(MyRead.gamepad())
print(MyRead.buttons())
```

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Authors

* **Ryan Barnes** - *Main Developer* - [bayangan1991](https://github.com/bayangan1991)

See also the list of [contributors](https://github.com/bayangan1991/PYXInput/graphs/contributors) who participated in this project.

## License

This project is licensed under the MIT License

## Acknowledgments

* Everyone at [vJoy](http://vjoystick.sourceforge.net/site/) for the vXboxInterface DLL
* [Sentdex](https://github.com/Sentdex) for the inspiration with his [pygta5](https://github.com/Sentdex/pygta5) project
* [nefarius](https://github.com/nefarius) for [ScpVBus](https://github.com/nefarius/ScpVBus)
