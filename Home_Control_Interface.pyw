from tkinter import Tk, Button, Label
from phue import Bridge
from pyHS100 import SmartPlug
from ahk import AHK
from functools import partial
import subprocess

b = Bridge('192.168.0.134')  # Hue Hub Connection
Heater = SmartPlug("192.168.0.146")  # Heater Smart Plug Connection
#  print(pf(Heater.get_sysinfo()))  # this prints lots of information about the device

Lighthouse = SmartPlug("192.168.0.196")  # Lighthouse Smart Plug Connection
#  print(pf(Lighthouse.get_sysinfo()))  # this prints lots of information about the device


#  Hue Bulb Functions
def SetScene(SceneName):
    b.run_scene('My Bedroom', SceneName, 1)


def SetLightsOff():
    b.set_group('My Bedroom', 'on', False)


def HeaterToggle():
    if Heater.get_sysinfo()["relay_state"] == 0:
        Heater.turn_on()
        HeaterButton.config(relief='sunken')  # On State
    else:
        Heater.turn_off()
        HeaterButton.config(relief='raised')  # Off State


def LighthouseToggle():
    if Lighthouse.get_sysinfo()["relay_state"] == 0:
        Lighthouse.turn_on()
        VRLighthouseButton.config(relief='sunken')
    else:
        Lighthouse.turn_off()
        VRLighthouseButton.config(relief='raised')


def StartVR():
    # if Lighthouse.get_sysinfo()["relay_state"] == 0:
    #     Lighthouse.turn_on()
    # VRLighthouseButton.config(relief='sunken')
    subprocess.call("D:/My Installed Games/Steam Games/steamapps/common/SteamVR/bin/win64/vrstartup.exe")


#  Requires AHK and NirCMD to work
ahk = AHK(executable_path=r'C:\Program Files\AutoHotkey\AutoHotkey.exe')
#  These simply name AHK commands that are ran as functions.
ahk_headphones = 'Run nircmd setdefaultsounddevice "Headphones"'
ahk_speakers = 'Run nircmd setdefaultsounddevice "Logitech Speakers"'


def SetSoundDevice(Device):
    ahk.run_script(Device, blocking=False)


#  ESC to Close Function
#  Empty parameter allows this to work
def close(event):
    LightControl.destroy()


LightControl = Tk()
LightControl.title("Computer Control Interface")
LightControl.iconbitmap('bulb.ico')
LightControl.configure(bg='white')

#  Binding for ESC Close
LightControl.bind("<Escape>", close)

#  Lighting Modes
LightModes = Label(LightControl, text="Hue Light Control", bg='white', font=("Arial Bold", 20))
LightModes.grid(column=1, row=1)
#  Grid Spacing with no other function
BlankSpace = Label(LightControl, text="", bg='white', font=("Arial Bold", 20))
BlankSpace.grid(column=0, row=1)

LightsOn = Button(LightControl, text="Lights On",
                  command=partial(SetScene, 'Normal'), font=("Arial", 19), width=15)
LightsOn.grid(column=0, row=2, padx=10, pady=10)

TurnAllOff = Button(LightControl, text="Lights Off",
                    command=SetLightsOff, font=("Arial", 19), width=15)
TurnAllOff.grid(column=0, row=3, padx=10, pady=10)

BackLight = Button(LightControl, text="BackLight Mode",
                   command=partial(SetScene, 'Backlight'), font=("Arial", 19), width=15)
BackLight.grid(column=1, row=2, padx=10, pady=10)

DimmedMode = Button(LightControl, text="Dimmed Mode",
                    command=partial(SetScene, 'Dimmed'), font=("Arial", 19), width=15)
DimmedMode.grid(column=2, row=2, padx=10, pady=10)

Nightlight = Button(LightControl, text="Night Light",
                    command=partial(SetScene, 'Night light'), font=("Arial", 19), width=15)
Nightlight.grid(column=1, row=3, padx=10, pady=10)

#  Smart Switch
SmartPlug = Label(LightControl, text="Smart Plug Control", bg='white', font=("Arial Bold", 20))
SmartPlug.grid(column=1, row=4)

BlankSpace = Label(LightControl, text="", bg='white', font=("Arial Bold", 20))
BlankSpace.grid(column=0, row=4, padx=10)

HeaterButton = Button(LightControl, text="Heater Switch", command=HeaterToggle, font=("Arial", 19), width=15)
HeaterButton.grid(column=0, row=5, padx=10, pady=10)

UnsetButton = Button(LightControl, text="Unset", state='disabled', command=HeaterToggle, font=("Arial", 19), width=15)
UnsetButton.grid(column=1, row=5, padx=10, pady=10)

#  VR Settings
VRSettings = Label(LightControl, text="VR Settings", bg='white', font=("Arial Bold", 20))
VRSettings.grid(column=1, row=8)

BlankSpace = Label(LightControl, text="", bg='white', font=("Arial Bold", 20))
BlankSpace.grid(column=0, row=4, padx=10)

StartVRButton = Button(LightControl, text="Start VR", command=StartVR, font=("Arial", 19),
                            width=15)
StartVRButton.grid(column=0, row=9, padx=10)

VRLighthouseButton = Button(LightControl, text="Lighthouse Switch", command=LighthouseToggle, font=("Arial", 19),
                            width=15)
VRLighthouseButton.grid(column=1, row=9, padx=10, pady=10)


#  Checks Device State and updates the button.
def PlugStateCheck(Device, DeviceButton):
    if Device.get_sysinfo()["relay_state"] == 1:
        DeviceButton.config(relief='sunken')  # On State
    else:
        DeviceButton.config(relief='raised')  # Off State


#  Smart Plugs running through State check function.
PlugStateCheck(Heater, HeaterButton)
PlugStateCheck(Lighthouse, VRLighthouseButton)


#  Audio Settings
BlankSpace = Label(LightControl, text="", bg='white', font=("Arial Bold", 20))
BlankSpace.grid(column=0, row=6, padx=10)

AudioSettings = Label(LightControl, text="Audio Settings", bg='white', font=("Arial Bold", 20))
AudioSettings.grid(column=1, row=6)

AudioToSpeakers = Button(LightControl, text="Speaker Audio", command=partial(SetSoundDevice, ahk_speakers), font=("Arial", 19), width=15)
AudioToSpeakers.grid(column=0, row=7, padx=10, pady=10)

AudioToHeadphones = Button(LightControl, text="Headphone Audio", command=partial(SetSoundDevice, ahk_headphones), font=("Arial", 19),
                           width=15)
AudioToHeadphones.grid(column=1, row=7, padx=10, pady=10)

LightControl.mainloop()
