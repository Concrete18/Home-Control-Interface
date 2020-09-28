# Home Control Interface

Control interface that allows control  of my lights, smart plugs, and PC audio default settings.
Click Taskbar Icon to bring up the interface and right click the icon and click exit to close script completely.

## Coding Techniques used

* Threading
* Class Functions
* NIRCMD
* Time.Sleep
* Socket for getting computer names
* AHK Wrapper
* Modules for Hue and Smart Plug controls.

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

![Image of Home Control Interface](https://i.imgur.com/I0KfGmk.png)
