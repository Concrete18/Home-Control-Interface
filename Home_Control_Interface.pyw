from Set_to_ABC import Change_to_ABC, Check_If_Youtube_TV
from tkinter import Tk, Button, LabelFrame, ttk
from Home_Class import Home_Interface
from pyHS100 import SmartPlug
import PySimpleGUIWx as sg
from phue import Bridge
from ahk import AHK
import socket
import time
import os

Tray = sg.SystemTray(
    menu= ['menu',['Lights On', 'Lights Off', 'Exit']],
    filename='bulb.ico',
    tooltip='Home Control Interface'
    )

Hue_Hub = Bridge('192.168.0.134')
Heater = SmartPlug('192.168.0.146')
Lighthouse = SmartPlug('192.168.0.196')
Home =  Home_Interface(Hue_Hub, Heater, Lighthouse)

while True:
    event = Tray.Read()
    print(event)
    if event == 'Exit':
            quit()
    # TODO Add more taskbar items with loop.
    elif event == 'Lights On':
        Home.SetScene(Home.Hue_Hub, 'Normal')
    elif event == 'Lights Off':
        Home.SetLightsOff(Home.Hue_Hub)
    elif event == '__DOUBLE_CLICKEF__':
        print('Double Clicked')
    elif event == '__ACTIVATED__':
        # TODO Add focus activation if window is already open.

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

        HueLightControlFrame = LabelFrame(LightControl, text='Hue Light Control', bg=Background,
            font=BaseFont, padx=FPadX, pady=FPadY, width=2000, height=4000)
        HueLightControlFrame.grid(column=0, rowspan=2, padx=FPadX, pady=FPadY, sticky='nsew')

        SmartPlugControlFrame = LabelFrame(LightControl, text='Smart Plug Control', bg=Background,
            font=BaseFont, padx=FPadX, pady=FPadY, width=300, height=390)
        SmartPlugControlFrame.grid(column=1, row=0, padx=FPadX, pady=FPadY, sticky='nsew')

        AudioSettingsFrame = LabelFrame(LightControl, text='Audio Settings', bg=Background, font=BaseFont,
            padx=FPadX, pady=FPadY, width=300, height=390)
        AudioSettingsFrame.grid(column=1, row=1, padx=FPadX, pady=FPadY, sticky='nsew')

        LightsOn = Button(HueLightControlFrame, text="Lights On", command=lambda: Home.SetScene('Normal'),
            font=("Arial", 19), width=15)
        LightsOn.grid(column=0, row=1, padx=FPadX, pady=FPadY)

        TurnAllOff = Button(HueLightControlFrame, text="Lights Off",command=lambda: Home.SetLightsOff(),
            font=("Arial", 19), width=15)
        TurnAllOff.grid(column=1, row=1, padx=FPadX, pady=FPadY)

        BackLight = Button(HueLightControlFrame, text="BackLight Mode",
            command=lambda: Home.SetScene('Backlight'), font=("Arial", 19), width=15)
        BackLight.grid(column=0, row=2, padx=FPadX, pady=FPadY)

        DimmedMode = Button(HueLightControlFrame, text="Dimmed Mode",command=lambda: Home.SetScene('Dimmed'),
            font=("Arial", 19), width=15)
        DimmedMode.grid(column=1, row=2, padx=FPadX, pady=FPadY)

        Nightlight = Button(HueLightControlFrame, text="Night Light",
            command=lambda: Home.SetScene('Night light'), font=("Arial", 19), width=15)
        Nightlight.grid(column=0, row=3, padx=FPadX, pady=FPadY)

        HeaterButton = Button(SmartPlugControlFrame, text="Heater Toggle",
            command=lambda: Home.HeaterToggle(HeaterButton), font=("Arial", 19), width=15)
        HeaterButton.grid(column=0, row=5, padx=FPadX, pady=FPadY)

        UnsetButton = Button(SmartPlugControlFrame, text="Unset", state='disabled',
            command='ph', font=("Arial", 19), width=15)
        UnsetButton.grid(column=1, row=5, padx=FPadX, pady=FPadY)

        Script_Shortcuts = LabelFrame(LightControl, text='Script Shortcuts', bg=Background, font=BaseFont,
            padx=FPadX, pady=FPadY, width=300, height=200)
        Script_Shortcuts.grid(column=0, row=3, padx=FPadX, pady=FPadY, sticky='nsew')

        RokuButton = Button(Script_Shortcuts, text="Set Roku to ABC", command=Change_to_ABC, font=("Arial", 19),
            width=15)
        RokuButton.grid(column=0, row=0, padx=FPadX, pady=FPadY)


        Check_If_Youtube_TV(RokuButton)


        TimerControl = Button(Script_Shortcuts, text="Power Control", command=Home.Timed_Power_Control,
            font=("Arial", 19), width=15)
        TimerControl.grid(column=1, row=0, padx=FPadX, pady=FPadY)

        # These simply name AHK commands that are ran as functions.
        ahk_headphones = 'Run nircmd setdefaultsounddevice "Headphones"'
        ahk_speakers = 'Run nircmd setdefaultsounddevice "Logitech Speakers" 1'
        ahk_SurfaceAux = 'Run nircmd setdefaultsounddevice "Aux"'
        ahk_SurfaceSpeakers = 'Run nircmd setdefaultsounddevice "Speakers"'

        Current_PC = socket.gethostname()
        if Current_PC == 'Aperture-Two':
            print(Current_PC)

            VRSettingsFrame = LabelFrame(LightControl, text='VR Settings', bg=Background, font=BaseFont,
                padx=FPadX, pady=FPadY, width=300, height=400)
            VRSettingsFrame.grid(column=0, row=2, padx=FPadX, pady=FPadX, sticky='nsew')

            StartVRButton = Button(VRSettingsFrame, text="Start VR",
                command=lambda: Home.StartVR(VRLighthouseButton), font=("Arial", 19), width=15)
            StartVRButton.grid(column=0, row=9, padx=FPadX, pady=FPadY)

            VRLighthouseButton = Button(VRSettingsFrame, text="Lighthouse Toggle",
                command=lambda: Home.LighthouseToggle(VRLighthouseButton), font=("Arial", 19), width=15)
            VRLighthouseButton.grid(column=1, row=9, padx=FPadX, pady=FPadY)

            AudioToSpeakers = Button(AudioSettingsFrame, text="Speaker Audio",
                command=lambda: Home.SetSoundDevice(ahk_speakers), font=("Arial", 19), width=15)
            AudioToSpeakers.grid(column=0, row=7, padx=FPadX, pady=FPadY)

            AudioToHeadphones = Button(AudioSettingsFrame, text="Headphone Audio",
                command=lambda: Home.SetSoundDevice(ahk_headphones), font=("Arial", 19),width=15)
            AudioToHeadphones.grid(column=1, row=7, padx=FPadX, pady=FPadY)

            ProjectionFrame = LabelFrame(LightControl, text='Projection', bg=Background, font=BaseFont,
                padx=FPadX, pady=FPadY, width=300, height=400)
            ProjectionFrame.grid(column=1, row=2, padx=FPadX, pady=FPadY, sticky='nsew')

            SwitchToPCMode = Button(ProjectionFrame, text="PC Mode", command=lambda: Home.display_switch('PC'),
                font=("Arial", 19), width=15)
            SwitchToPCMode.grid(column=0, row=9, padx=FPadX, pady=FPadY)

            SwitchToTVMode = Button(ProjectionFrame, text="TV Mode", command=lambda: Home.display_switch('TV'),
                font=("Arial", 19), width=15)
            SwitchToTVMode.grid(column=1, row=9, padx=FPadX, pady=FPadY)


            Home.PlugStateCheck(Lighthouse, VRLighthouseButton)


        elif Current_PC == 'Surface-1':
            print(Current_PC)

            AudioToSpeakers = Button(AudioSettingsFrame, text="Speaker Audio",
                command=lambda: Home.SetSoundDevice(ahk_SurfaceSpeakers), font=("Arial", 19), width=15)
            AudioToSpeakers.grid(column=0, row=7, padx=FPadX, pady=FPadY)

            AudioToHeadphones = Button(AudioSettingsFrame, text="Headphone Audio",
                command=lambda: Home.SetSoundDevice(ahk_SurfaceAux), font=("Arial", 19),width=15)
            AudioToHeadphones.grid(column=1, row=7, padx=FPadX, pady=FPadY)


        #  Smart Plugs running through State check function.
        Home.PlugStateCheck(Heater, HeaterButton)


        LightControl.mainloop()
