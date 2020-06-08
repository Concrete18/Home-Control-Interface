# Home-Control-Interface
Control interface that allows control  of my lights, smart plugs, and PC audio default settings.
Click Taskbar Icon to bring up the interface and right click the icon and click exit to close script completely.

## Requirements
Uses AHK and NIRCMD for control of the default audio device. (AHK and NirCMD must be installed seperately)
Phue and pyHS100 are used for control of Hue bulbs and TP Link Smart Plugs respectively.
Tkinter is used for the interface
PySimpleGUIWx and PythonWx for the task bar icon.

## Computer Name Specific Configuration
On Launch it will check which computer it is on to make sure all buttons work on that computer. 
Anything that has no purpose won't even show up.

![Image of Home Control Interface](https://i.imgur.com/o0ngbfV.png)
