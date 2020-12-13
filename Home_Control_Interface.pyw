from Set_to_ABC import Change_to_ABC, Check_If_Youtube_TV
from tkinter import Tk, Button, LabelFrame, messagebox
from pyHS100 import SmartPlug
import PySimpleGUIWx as sg
from phue import Bridge
from ahk import AHK
import subprocess
import threading
import socket
import time
import os


class Home:


    def __init__(self):
        # device init
        self.Hue_Hub = Bridge('192.168.0.134')
        self.Heater = SmartPlug('192.168.0.146')
        self.Lighthouse = SmartPlug('192.168.0.197')
        # AHK
        self.ahk = AHK(executable_path='C:/Program Files/AutoHotkey/AutoHotkey.exe')
        self.ahk_speakers = 'Run nircmd setdefaultsounddevice "Logitech Speakers" 1'
        self.ahk_tv = 'Run nircmd setdefaultsounddevice "SONY TV" 1'
        self.ahk_headphones = 'Run nircmd setdefaultsounddevice "Headphones"'
        self.ahk_SurfaceAux = 'Run nircmd setdefaultsounddevice "Aux"'
        self.ahk_SurfaceSpeakers = 'Run nircmd setdefaultsounddevice "Speakers"'


    # Hue Bulb Functions
    def set_scene(self, scene_name):
        '''
        Set Scene Function.

        Args = scene_name
        '''
        self.Hue_Hub.run_scene('My Bedroom', scene_name, 1)


    def set_lights_off(self):
        '''
        Turn Lights off function.
        '''
        self.Hue_Hub.set_group('My Bedroom', 'on', False)


    def heater_toggle(self):
        '''
        Heater Toggle Function.
        '''
        try:
            if self.Heater.get_sysinfo()["relay_state"] == 0:
                self.Heater.turn_on()
                self.HeaterButton.config(relief='sunken')  # On State
            else:
                self.Heater.turn_off()
                self.HeaterButton.config(relief='raised')  # Off State
        except:
            print('Heater Error')


    def lighthouse_toggle(self):
        '''
        Lighthouse Toggle Function.
        '''
        try:
            if self.Lighthouse.get_sysinfo()["relay_state"] == 0:
                self.Lighthouse.turn_on()
                self.VRLighthouseButton.config(relief='sunken')
            else:
                self.Lighthouse.turn_off()
                self.VRLighthouseButton.config(relief='raised')
        except:
            print('Lighthouse Error')


    def start_vr(self):
        '''
        Start VR Function.
        '''
        if self.Lighthouse.get_sysinfo()["relay_state"] == 0:
            self.Lighthouse.turn_on()
            self.VRLighthouseButton.config(relief='sunken')
        subprocess.call("D:/My Installed Games/Steam Games/steamapps/common/SteamVR/bin/win64/vrstartup.exe")


    # Requires AHK and NirCMD to work
    def set_sound_device(self, device):
        '''
        Set Sound Device Function.

        Args = device.
        '''
        self.ahk.run_script(device, blocking=False)


    def display_switch(self, mode):
        '''
        Switches display to the mode entered as an argument. Works for PC and TV mode.

        Args = mode.
        '''
        # FIXME Display Switch
        def callback(mode):
            subprocess.call([f'{os.getcwd()}/Batches/{mode} Mode.bat'])
            time.sleep(10)
            if mode == 'PC':
                self.ahk.run_script(self.ahk_speakers, blocking=False)
            else:
                self.ahk.run_script(self.ahk_tv, blocking=False)
            print(f'{mode} Mode Set')
        Switch = threading.Thread(target=callback(mode))
        Switch.start()


    def timed_power_control(self):
        '''
        Runs Timed Power Control Function.
        '''
        script = "D:/Google Drive/Coding/Python/Scripts/1-Complete-Projects/Timed-Shutdown/Timed_Shutdown.pyw"
        subprocess.call(["python", script])


    # Checks Device State and updates the button.
    def plug_state_check(self):
        '''
        Gets current state of entered device and updates button relief.
        '''
        buttons = {
        self.Heater:self.HeaterButton,
        self.Lighthouse:self.VRLighthouseButton
        }
        for device, button in buttons.items():
            try:
                if device.get_sysinfo()["relay_state"] == 1:
                    button.config(relief='sunken')  # On State
                else:
                    button.config(relief='raised')  # Off State
            except Exception  as e:
                print('Smart Plug', e)
                messagebox.showwarning(title='Game Save Manager', message=f'Error communicating with {device}.')


    def create_window(self):
        Home_Interface = Tk()
        window_width = 1108
        window_height = 580
        width = int((Home_Interface.winfo_screenwidth()-window_width)/2)
        height = int((Home_Interface.winfo_screenheight()-window_height)/2)
        Home_Interface.geometry(f'{window_width}x{window_height}+{width}+{height}')
        Home_Interface.title("Home Control Interface")
        Home_Interface.iconbitmap('bulb.ico')
        Home_Interface.configure(bg='white')
        Home_Interface.resizable(width=False, height=False)

        background = 'white'
        base_font = ('Arial Bold', 20)
        pad_x = 10
        pad_y = 10

        # Frames
        HueLightControlFrame = LabelFrame(Home_Interface, text='Hue Light Control', bg=background,
            font=base_font, padx=pad_x, pady=pad_y, width=2000, height=4000)
        HueLightControlFrame.grid(column=0, rowspan=2, padx=pad_x, pady=pad_y, sticky='nsew')

        SmartPlugControlFrame = LabelFrame(Home_Interface, text='Smart Plug Control', bg=background,
            font=base_font, padx=pad_x, pady=pad_y, width=300, height=390)
        SmartPlugControlFrame.grid(column=1, row=0, padx=pad_x, pady=pad_y, sticky='nsew')

        AudioSettingsFrame = LabelFrame(Home_Interface, text='Audio Settings', bg=background, font=base_font,
            padx=pad_x, pady=pad_y, width=300, height=390)
        AudioSettingsFrame.grid(column=1, row=1, padx=pad_x, pady=pad_y, sticky='nsew')

        # Buttons
        LightsOn = Button(HueLightControlFrame, text="Lights On", command=lambda: self.set_scene('Normal'),
            font=("Arial", 19), width=15)
        LightsOn.grid(column=0, row=1, padx=pad_x, pady=pad_y)

        TurnAllOff = Button(HueLightControlFrame, text="Lights Off",command=lambda: self.set_lights_off(),
            font=("Arial", 19), width=15)
        TurnAllOff.grid(column=1, row=1, padx=pad_x, pady=pad_y)

        BackLight = Button(HueLightControlFrame, text="BackLight Mode",
            command=lambda: self.set_scene('Backlight'), font=("Arial", 19), width=15)
        BackLight.grid(column=0, row=2, padx=pad_x, pady=pad_y)

        DimmedMode = Button(HueLightControlFrame, text="Dimmed Mode",command=lambda: self.set_scene('Dimmed'),
            font=("Arial", 19), width=15)
        DimmedMode.grid(column=1, row=2, padx=pad_x, pady=pad_y)

        Nightlight = Button(HueLightControlFrame, text="Night Light",
            command=lambda: self.set_scene('Night light'), font=("Arial", 19), width=15)
        Nightlight.grid(column=0, row=3, padx=pad_x, pady=pad_y)

        self.HeaterButton = Button(SmartPlugControlFrame, text="Heater Toggle",
            command=lambda: self.heater_toggle(), font=("Arial", 19), width=15)
        self.HeaterButton.grid(column=0, row=5, padx=pad_x, pady=pad_y)

        UnsetButton = Button(SmartPlugControlFrame, text="Unset", state='disabled',
            command='ph', font=("Arial", 19), width=15)
        UnsetButton.grid(column=1, row=5, padx=pad_x, pady=pad_y)

        Script_Shortcuts = LabelFrame(Home_Interface, text='Script Shortcuts', bg=background, font=base_font,
            padx=pad_x, pady=pad_y, width=300, height=200)
        Script_Shortcuts.grid(column=0, row=3, padx=pad_x, pady=pad_y, sticky='nsew')

        RokuButton = Button(Script_Shortcuts, text="Set Roku to ABC", command=Change_to_ABC, font=("Arial", 19),
            width=15)
        RokuButton.grid(column=0, row=0, padx=pad_x, pady=pad_y)

        TimerControl = Button(Script_Shortcuts, text="Power Control", command=self.timed_power_control,
            font=("Arial", 19), width=15)
        TimerControl.grid(column=1, row=0, padx=pad_x, pady=pad_y)

        current_pc = socket.gethostname()
        if current_pc == 'Aperture-Two':
            VRSettingsFrame = LabelFrame(Home_Interface, text='VR Settings', bg=background, font=base_font,
                padx=pad_x, pady=pad_y, width=300, height=400)
            VRSettingsFrame.grid(column=0, row=2, padx=pad_x, pady=pad_x, sticky='nsew')

            StartVRButton = Button(VRSettingsFrame, text="Start VR",
                command=lambda: self.start_vr(VRLighthouseButton), font=("Arial", 19), width=15)
            StartVRButton.grid(column=0, row=9, padx=pad_x, pady=pad_y)

            self.VRLighthouseButton = Button(VRSettingsFrame, text="Lighthouse Toggle",
                command=lambda: self.lighthouse_toggle(), font=("Arial", 19), width=15)
            self.VRLighthouseButton.grid(column=1, row=9, padx=pad_x, pady=pad_y)

            AudioToSpeakers = Button(AudioSettingsFrame, text="Speaker Audio",
                command=lambda: self.set_sound_device(self.ahk_speakers), font=("Arial", 19), width=15)
            AudioToSpeakers.grid(column=0, row=7, padx=pad_x, pady=pad_y)

            AudioToHeadphones = Button(AudioSettingsFrame, text="Headphone Audio",
                command=lambda: self.set_sound_device(self.ahk_headphones), font=("Arial", 19),width=15)
            AudioToHeadphones.grid(column=1, row=7, padx=pad_x, pady=pad_y)

            ProjectionFrame = LabelFrame(Home_Interface, text='Projection', bg=background, font=base_font,
                padx=pad_x, pady=pad_y, width=300, height=400)
            ProjectionFrame.grid(column=1, row=2, padx=pad_x, pady=pad_y, sticky='nsew')

            SwitchToPCMode = Button(ProjectionFrame, text="PC Mode", command=lambda: self.display_switch('PC'),
                font=("Arial", 19), width=15)
            SwitchToPCMode.grid(column=0, row=9, padx=pad_x, pady=pad_y)

            SwitchToTVMode = Button(ProjectionFrame, text="TV Mode", command=lambda: self.display_switch('TV'),
                font=("Arial", 19), width=15)
            SwitchToTVMode.grid(column=1, row=9, padx=pad_x, pady=pad_y)


        elif current_pc == 'Surface-1':
            AudioToSpeakers = Button(AudioSettingsFrame, text="Speaker Audio",
                command=lambda: self.set_sound_device(self.ahk_SurfaceSpeakers), font=("Arial", 19), width=15)
            AudioToSpeakers.grid(column=0, row=7, padx=pad_x, pady=pad_y)

            AudioToHeadphones = Button(AudioSettingsFrame, text="Headphone Audio",
                command=lambda: self.set_sound_device(self.ahk_SurfaceAux), font=("Arial", 19),width=15)
            AudioToHeadphones.grid(column=1, row=7, padx=pad_x, pady=pad_y)


        #  Smart Plugs running through state check function.
        self.plug_state_check()


        Home_Interface.mainloop()


    def create_tray(self):
        Tray = sg.SystemTray(
            menu=['menu',[
            'Lights On',
            'Backlight',
            'Lights Off',
            'Exit'
            ]],
            filename='bulb.ico',
            tooltip='Home Control Interface'
            )

        while True:
            event = Tray.Read()
            if event == 'Exit':
                    quit()
            elif event == 'Lights On':
                self.set_scene('Normal')
            elif event == 'Backlight':
                self.set_scene('Backlight')
            elif event == 'Lights Off':
                self.set_lights_off()
            elif event == '__ACTIVATED__':
                self.create_window()


if __name__ == "__main__":
    Home =  Home()

    Home.create_tray()
