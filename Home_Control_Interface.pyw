from tkinter import Tk, Button, LabelFrame
from phue import Bridge
from pyHS100 import SmartPlug
from ahk import AHK
from functools import partial
import threading
import subprocess
import socket
import time
import os
import PySimpleGUIWx as sg

tray = sg.SystemTray(menu= ['menu',['Exit']], filename='bulb.ico', tooltip='Home Control Interface')
while True:
    event = tray.Read()
    print(event)
    if event == 'Exit':
        quit()
    elif event == '__DOUBLE_CLICKEF__':
        print('Double Clicked')
    elif event == '__ACTIVATED__':
        CurrentPC = socket.gethostname()
        cwd = os.getcwd()

        b = Bridge('192.168.0.134')  # Hue Hub Connection
        Heater = SmartPlug("192.168.0.146")  # Heater Smart Plug Connection
        # print(pf(Heater.get_sysinfo()))  # this prints lots of information about the device

        Lighthouse = SmartPlug("192.168.0.196")  # Lighthouse Smart Plug Connection
        # print(pf(Lighthouse.get_sysinfo()))  # this prints lots of information about the device


        # Hue Bulb Functions
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
            if Lighthouse.get_sysinfo()["relay_state"] == 0:
                Lighthouse.turn_on()
                VRLighthouseButton.config(relief='sunken')
            subprocess.call("D:/My Installed Games/Steam Games/steamapps/common/SteamVR/bin/win64/vrstartup.exe")


        def display_switch(mode):
            def callback():
                subprocess.call([f'{cwd}/Batches/{mode} Mode.bat'])
                time.sleep(10)
                if mode == 'PC':
                    ahk.run_script(ahk_speakers, blocking=False)
                else:
                    ahk.run_script(ahk_tv, blocking=False)
                print(f'{mode} Mode Set')
            t = threading.Thread(target=callback)
            t.start()


        # Requires AHK and NirCMD to work
        ahk = AHK(executable_path='C:/Program Files/AutoHotkey/AutoHotkey.exe')
        # These simply name AHK commands that are ran as functions.
        ahk_headphones = 'Run nircmd setdefaultsounddevice "Headphones"'
        ahk_speakers = 'Run nircmd setdefaultsounddevice "Logitech Speakers" 1'
        ahk_tv = 'Run nircmd setdefaultsounddevice "SONY TV" 1'
        ahk_SurfaceAux = 'Run nircmd setdefaultsounddevice "Aux"'
        ahk_SurfaceSpeakers = 'Run nircmd setdefaultsounddevice "Speakers"'


        def SetSoundDevice(Device):
            ahk.run_script(Device, blocking=False)


        LightControl = Tk()
        LightControl.title("Home Control Interface")
        LightControl.iconbitmap('bulb.ico')
        LightControl.configure(bg='white')
        LightControl.resizable(width=False, height=False)
        LightControl.geometry("+600+600")


        # Frames
        Background = 'white'
        BaseFont = ('Arial Bold', 20)
        FPadX = 10
        FPadY = 10

        HueLightControlFrame = LabelFrame(LightControl, text='Hue Light Control',
                                        bg=Background, font=BaseFont, padx=FPadX, pady=FPadY, width=2000, height=4000)
        HueLightControlFrame.grid(column=0, rowspan=2, padx=FPadX, pady=FPadY, sticky='nsew')

        SmartPlugControlFrame = LabelFrame(LightControl, text='Smart Plug Control',
                                        bg=Background, font=BaseFont, padx=FPadX, pady=FPadY, width=300, height=390)
        SmartPlugControlFrame.grid(column=1, row=0, padx=FPadX, pady=FPadY, sticky='nsew')

        AudioSettingsFrame = LabelFrame(LightControl, text='Audio Settings',
                                        bg=Background, font=BaseFont, padx=FPadX, pady=FPadY, width=300, height=390)
        AudioSettingsFrame.grid(column=1, row=1, padx=FPadX, pady=FPadY, sticky='nsew')

        LightsOn = Button(HueLightControlFrame, text="Lights On",
                        command=partial(SetScene, 'Normal'), font=("Arial", 19), width=15)
        LightsOn.grid(column=0, row=1, padx=FPadX, pady=FPadY)

        TurnAllOff = Button(HueLightControlFrame, text="Lights Off",
                            command=SetLightsOff, font=("Arial", 19), width=15)
        TurnAllOff.grid(column=1, row=1, padx=FPadX, pady=FPadY)

        BackLight = Button(HueLightControlFrame, text="BackLight Mode",
                        command=partial(SetScene, 'Backlight'), font=("Arial", 19), width=15)
        BackLight.grid(column=0, row=2, padx=FPadX, pady=FPadY)

        DimmedMode = Button(HueLightControlFrame, text="Dimmed Mode",
                            command=partial(SetScene, 'Dimmed'), font=("Arial", 19), width=15)
        DimmedMode.grid(column=1, row=2, padx=FPadX, pady=FPadY)

        Nightlight = Button(HueLightControlFrame, text="Night Light",
                            command=partial(SetScene, 'Night light'), font=("Arial", 19), width=15)
        Nightlight.grid(column=0, row=3, padx=FPadX, pady=FPadY)

        HeaterButton = Button(SmartPlugControlFrame, text="Heater Toggle", command=HeaterToggle, font=("Arial", 19), width=15)
        HeaterButton.grid(column=0, row=5, padx=FPadX, pady=FPadY)

        UnsetButton = Button(SmartPlugControlFrame, text="Unset", state='disabled', command=HeaterToggle,
                            font=("Arial", 19), width=15)
        UnsetButton.grid(column=1, row=5, padx=FPadX, pady=FPadY)


        # Checks Device State and updates the button.
        def PlugStateCheck(Device, DeviceButton):
            if Device.get_sysinfo()["relay_state"] == 1:
                DeviceButton.config(relief='sunken')  # On State
            else:
                DeviceButton.config(relief='raised')  # Off State


        if CurrentPC == 'Aperture-Two':
            print(CurrentPC)
            VRSettingsFrame = LabelFrame(LightControl, text='VR Settings',
                                        bg=Background, font=BaseFont, padx=FPadX, pady=FPadY, width=300, height=400)
            VRSettingsFrame.grid(column=0, row=2, padx=FPadX, pady=FPadX, sticky='nsew')

            StartVRButton = Button(VRSettingsFrame, text="Start VR", command=StartVR, font=("Arial", 19), width=15)
            StartVRButton.grid(column=0, row=9, padx=FPadX, pady=FPadY)

            VRLighthouseButton = Button(VRSettingsFrame, text="Lighthouse Toggle",
                                        command=LighthouseToggle, font=("Arial", 19), width=15)
            VRLighthouseButton.grid(column=1, row=9, padx=FPadX, pady=FPadY)

            AudioToSpeakers = Button(AudioSettingsFrame, text="Speaker Audio",
                                    command=partial(SetSoundDevice, ahk_speakers), font=("Arial", 19), width=15)
            AudioToSpeakers.grid(column=0, row=7, padx=FPadX, pady=FPadY)

            AudioToHeadphones = Button(AudioSettingsFrame, text="Headphone Audio",
                                    command=partial(SetSoundDevice, ahk_headphones), font=("Arial", 19),width=15)
            AudioToHeadphones.grid(column=1, row=7, padx=FPadX, pady=FPadY)

            ProjectionFrame = LabelFrame(LightControl, text='Projection', bg=Background,
                                        font=BaseFont, padx=FPadX, pady=FPadY, width=300, height=400)
            ProjectionFrame.grid(column=1, row=2, padx=FPadX, pady=FPadY, sticky='nsew')

            SwitchToPCMode = Button(ProjectionFrame, text="PC Mode", command=partial(display_switch, 'PC'), font=("Arial", 19), width=15)
            SwitchToPCMode.grid(column=0, row=9, padx=FPadX, pady=FPadY)

            SwitchToTVMode = Button(ProjectionFrame, text="TV Mode", command=partial(display_switch, 'TV'), font=("Arial", 19), width=15)
            SwitchToTVMode.grid(column=1, row=9, padx=FPadX, pady=FPadY)

            PlugStateCheck(Lighthouse, VRLighthouseButton)

        elif CurrentPC == 'Surface-1':
            print(CurrentPC)
            AudioToSpeakers = Button(AudioSettingsFrame, text="Speaker Audio",
                                    command=partial(SetSoundDevice, ahk_SurfaceSpeakers), font=("Arial", 19), width=15)
            AudioToSpeakers.grid(column=0, row=7, padx=FPadX, pady=FPadY)

            AudioToHeadphones = Button(AudioSettingsFrame, text="Headphone Audio",
                                    command=partial(SetSoundDevice, ahk_SurfaceAux), font=("Arial", 19),width=15)
            AudioToHeadphones.grid(column=1, row=7, padx=FPadX, pady=FPadY)


        #  Smart Plugs running through State check function.
        PlugStateCheck(Heater, HeaterButton)

        LightControl.mainloop()
