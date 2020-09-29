import PySimpleGUIWx as sg
from ahk import AHK
import subprocess
import threading
import time
import os

class Home_Interface:

    def __init__(self, hue, heater, lighthouse):
        self.Hue_Hub = hue
        self.Heater = heater
        self.Lighthouse = lighthouse
        self.ahk = AHK(executable_path='C:/Program Files/AutoHotkey/AutoHotkey.exe')
        self.ahk_speakers = 'Run nircmd setdefaultsounddevice "Logitech Speakers" 1'
        self.ahk_tv = 'Run nircmd setdefaultsounddevice "SONY TV" 1'


    # Hue Bulb Functions
    def SetScene(self, SceneName):
        '''Set Scene Function.

        Args = SceneName.'''
        self.Hue_Hub.run_scene('My Bedroom', SceneName, 1)


    def SetLightsOff(self):
        '''Turn Lights off function.'''
        self.Hue_Hub.set_group('My Bedroom', 'on', False)


    def HeaterToggle(self, button):
        '''Heater Toggle Function.

        Args = button.'''
        try:
            if self.Heater.get_sysinfo()["relay_state"] == 0:
                self.Heater.turn_on()
                button.config(relief='sunken')  # On State
            else:
                self.Heater.turn_off()
                button.config(relief='raised')  # Off State
        except:
            print('Heater Error')


    def LighthouseToggle(self, button):
        '''Lighthouse Toggle Function.

        Args = button.'''
        try:
            if self.Lighthouse.get_sysinfo()["relay_state"] == 0:
                self.Lighthouse.turn_on()
                button.config(relief='sunken')
            else:
                self.Lighthouse.turn_off()
                button.config(relief='raised')
        except:
            print('Lighthouse Error')


    def StartVR(self, button):
        '''Start VR Function.

        Args = button.'''
        if self.Lighthouse.get_sysinfo()["relay_state"] == 0:
            self.Lighthouse.turn_on()
            button.config(relief='sunken')
        subprocess.call("D:/My Installed Games/Steam Games/steamapps/common/SteamVR/bin/win64/vrstartup.exe")


    # Requires AHK and NirCMD to work
    def SetSoundDevice(self, device):
        '''Set Sound Device Function.

        Args = device.'''
        self.ahk.run_script(device, blocking=False)


    def Display_Switch(self, mode):
        '''Switches display to the mode entered as an argument. Works for PC and TV mode.

        Args = mode.'''
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


    def Timed_Power_Control(self):
        '''Runs Timed Power Control Function.

        Currently WIP.'''
        script = "D:/Google Drive/Coding/Python/Scripts/1-Complete-Projects/Timed-Shutdown/Timed_Shutdown.pyw"
        subprocess.call(["python", script])


    # Checks Device State and updates the button.
    def PlugStateCheck(self, device, button):
        '''Gets current state of entered device and updates button relief.

        Args = device, button.'''
        try:
            if device.get_sysinfo()["relay_state"] == 1:
                button.config(relief='sunken')  # On State
            else:
                button.config(relief='raised')  # Off State
        except:
            print('Smart Plug Communication Error')
