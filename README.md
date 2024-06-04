# Home Control Interface

Control interface that allows control of my lights, smart plugs, and PC audio default settings along with many other features.
Click Taskbar Icon to bring up the interface and right click the icon and click exit to close script completely.

## Features

* Full control of all of my Kasa smart plugs and Hue light bulbs.
* Audio and projection control
* VR start functionality that sets up room and PC for VR.
* Shortcuts to some other scripts. (Listed Below)
* Power Control Settings via another app. (Not in Repo)
[Timed Shutdown and Sleep](https://github.com/Concrete18/Timed-Shutdown-Sleep)

## Coding Techniques used

* Threading
* Class Functions
* Time.Sleep
* Screen and window calculations to perfectly center interface
* Socket for getting computer names
* NIRCMD
* AHK Wrapper
* Modules for Hue and Smart Plug controls
* psutil for system information

## Module Download Requirements

Run within your console for pip.

```cmd
pip install -r requirements.txt
```

### See requirements.txt for modules and versions used

* Uses AHK and NIRCMD for control of the default audio device. (AHK and NirCMD must be installed separately)
* Phue and pyHS100 are used for control of Hue bulbs and TP Link Smart Plugs respectively.
* Tkinter is used for the interface
* PySimpleGUIWx and PythonWx for the task bar icon.

![Image of Home Control Interface](https://raw.githubusercontent.com/Concrete18/Home-Control-Interface/master/images/screenshot.png)
