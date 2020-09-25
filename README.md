# Home Control Interface

Control interface that allows control  of my lights, smart plugs, and PC audio default settings.
Click Taskbar Icon to bring up the interface and right click the icon and click exit to close script completely.

## Coding Techniques used

I have made use of threading to allow the gui to not freeze while some buttons make use of a time.sleep in order to make sure commands work during projection mode changes.
The socket module is used to get the computer name so that the interface can differ based on my desktop and laptop. I have no need for many settings on the laptop so it becomes a less featured interface.
An AHK wrapper is used to make use of NIRCMD. I found no easy way around this as I am already familiar with NIRCMD using AHK.

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
