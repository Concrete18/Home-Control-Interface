from Set_to_ABC import Change_to_ABC, Check_If_Youtube_TV
from tkinter import Tk, Button, LabelFrame, ttk
from Home_Class import Home_Interface
from pyHS100 import SmartPlug
from functools import partial
import PySimpleGUIWx as sg
from phue import Bridge
from ahk import AHK
import subprocess
import threading
import socket
import runpy
import time
import os

Home =  Home_Interface()

while True:
    event = tray.Read()
    print(event)
    if event == 'Exit':
            quit()
    elif event == 'Lights On':
        Home.SetScene('Normal')
    elif event == 'Lights Off':
        Home.SetLightsOff()
    elif event == '__DOUBLE_CLICKEF__':
        print('Double Clicked')
    elif event == '__ACTIVATED__':
        # TODO Add focus activation if window is already open.
        cwd = os.getcwd()
        # TODO Create try statements for anything with connections that could fail.
        b = Bridge('192.168.0.134')  # Hue Hub Connection
        Heater = SmartPlug("192.168.0.146")  # Heater Smart Plug Connection
        # print(pf(Heater.get_sysinfo()))  # this prints lots of information about the device

        Lighthouse = SmartPlug("192.168.0.196")  # Lighthouse Smart Plug Connection
        # print(pf(Lighthouse.get_sysinfo()))  # this prints lots of information about the device


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
                        command=partial(Home.SetScene(), 'Normal'), font=("Arial", 19), width=15)
        LightsOn.grid(column=0, row=1, padx=FPadX, pady=FPadY)

        TurnAllOff = Button(HueLightControlFrame, text="Lights Off",
                            command=Home.SetLightsOff(), font=("Arial", 19), width=15)
        TurnAllOff.grid(column=1, row=1, padx=FPadX, pady=FPadY)

        BackLight = Button(HueLightControlFrame, text="BackLight Mode",
                        command=partial(Home.SetScene(), 'Backlight'), font=("Arial", 19), width=15)
        BackLight.grid(column=0, row=2, padx=FPadX, pady=FPadY)

        DimmedMode = Button(HueLightControlFrame, text="Dimmed Mode",
                            command=partial(Home.SetScene(), 'Dimmed'), font=("Arial", 19), width=15)
        DimmedMode.grid(column=1, row=2, padx=FPadX, pady=FPadY)

        Nightlight = Button(HueLightControlFrame, text="Night Light",
                            command=partial(Home.SetScene(), 'Night light'), font=("Arial", 19), width=15)
        Nightlight.grid(column=0, row=3, padx=FPadX, pady=FPadY)

        HeaterButton = Button(SmartPlugControlFrame, text="Heater Toggle", command=Home.HeaterToggle, font=("Arial", 19), width=15)
        HeaterButton.grid(column=0, row=5, padx=FPadX, pady=FPadY)

        UnsetButton = Button(SmartPlugControlFrame, text="Unset", state='disabled', command=Home.HeaterToggle,
                            font=("Arial", 19), width=15)
        UnsetButton.grid(column=1, row=5, padx=FPadX, pady=FPadY)

        Script_Shortcuts = LabelFrame(LightControl, text='Script Shortcuts',
                                        bg=Background, font=BaseFont, padx=FPadX, pady=FPadY, width=300, height=200)
        Script_Shortcuts.grid(column=0, row=3, padx=FPadX, pady=FPadY, sticky='nsew')

        RokuButton = Button(Script_Shortcuts, text="Set Roku to ABC", command=Change_to_ABC,
                    font=("Arial", 19), width=15)
        RokuButton.grid(column=0, row=0, padx=FPadX, pady=FPadY)

        if Check_If_Youtube_TV():
            RokuButton.config(relief='sunken')
        else:
            RokuButton.config(relief='raised')

        TimerControl = Button(Script_Shortcuts, text="Power Control", command=Home.Timed_Power_Control,
                    font=("Arial", 19), width=15)
        TimerControl.grid(column=1, row=0, padx=FPadX, pady=FPadY)

        # Checks Device State and updates the button.
        def PlugStateCheck(Device, DeviceButton):
            '''Gets current state of entered device and updates button relief.'''
            try:
                if Device.get_sysinfo()["relay_state"] == 1:
                    DeviceButton.config(relief='sunken')  # On State
                else:
                    DeviceButton.config(relief='raised')  # Off State
            except:
                print('Smart Plug Communication Error')

        Current_PC = socket.gethostbyname()
        if Current_PC == 'Aperture-Two':
            print(Current_PC)
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

        elif Current_PC == 'Surface-1':
            print(Current_PC)
            AudioToSpeakers = Button(AudioSettingsFrame, text="Speaker Audio",
                                    command=partial(SetSoundDevice, ahk_SurfaceSpeakers), font=("Arial", 19), width=15)
            AudioToSpeakers.grid(column=0, row=7, padx=FPadX, pady=FPadY)

            AudioToHeadphones = Button(AudioSettingsFrame, text="Headphone Audio",
                                    command=partial(SetSoundDevice, ahk_SurfaceAux), font=("Arial", 19),width=15)
            AudioToHeadphones.grid(column=1, row=7, padx=FPadX, pady=FPadY)


        #  Smart Plugs running through State check function.
        PlugStateCheck(Heater, HeaterButton)

        LightControl.mainloop()
