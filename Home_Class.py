import PySimpleGUIWx as sg
from ahk import AHK
import subprocess
import threading
import time
import os

class Home_Interface:

    # Hue Bulb Functions
    def SetScene(self, obj, SceneName):
        '''Set Scene Function.

        Args = obj, SceneName.'''
        obj.run_scene('My Bedroom', SceneName, 1)


    def SetLightsOff(self, obj):
        '''Set Scene Function.

        Args = obj.'''
        obj.set_group('My Bedroom', 'on', False)


    def HeaterToggle(self, obj, button):
        '''Heater Toggle Function.

        Args = obj, button.'''
        try:
            if obj.get_sysinfo()["relay_state"] == 0:
                obj.turn_on()
                button.config(relief='sunken')  # On State
            else:
                obj.turn_off()
                button.config(relief='raised')  # Off State
        except:
            print('Heater Error')


    def LighthouseToggle(self, obj, button):
        '''Lighthouse Toggle Function.

        Args = obj, button.'''
        try:
            if obj.get_sysinfo()["relay_state"] == 0:
                obj.turn_on()
                button.config(relief='sunken')
            else:
                obj.turn_off()
                button.config(relief='raised')
        except:
            print('Lighthouse Error')


    def StartVR(self, obj, button):
        '''Start VR Function.

        Args = obj, button.'''
        if obj.get_sysinfo()["relay_state"] == 0:
            obj.turn_on()
            button.config(relief='sunken')
        subprocess.call("D:/My Installed Games/Steam Games/steamapps/common/SteamVR/bin/win64/vrstartup.exe")


    # Requires AHK and NirCMD to work
    ahk = AHK(executable_path='C:/Program Files/AutoHotkey/AutoHotkey.exe')


    def SetSoundDevice(self, device):
        '''Set Sound Device Function.

        Args = device.'''
        ahk.run_script(device, blocking=False)

    ahk_speakers = 'Run nircmd setdefaultsounddevice "Logitech Speakers" 1'
    ahk_tv = 'Run nircmd setdefaultsounddevice "SONY TV" 1'

    def Display_Switch(self, obj, mode):
        '''Switches display to the mode entered as an argument. Works for PC and TV mode.

        Args = obj, mode.'''
        def callback():
            subprocess.call([f'{os.getcwd()}/Batches/{mode} Mode.bat'])
            time.sleep(10)
            if mode == 'PC':
                obj.run_script(ahk_speakers, blocking=False)
            else:
                obj.run_script(ahk_tv, blocking=False)
            print(f'{mode} Mode Set')
        Switch = threading.Thread(target=callback)
        Switch.start()


    def Timed_Power_Control(self):
        '''Runs Timed Power Control Function.

        Currently WIP.'''
        script = "D:/Google Drive/Coding/Python/Scripts/1-Complete-Projects/Timed-Shutdown/Timed_Shutdown.pyw"
        os.system(script)


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
