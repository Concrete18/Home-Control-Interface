from pyHS100 import SmartPlug
import PySimpleGUIWx as sg
from phue import Bridge
from ahk import AHK
import subprocess
import threading
import time
import os

class Home_Interface:
    def __init__(self):
        tray = sg.SystemTray(menu= ['menu',['Exit', 'Lights On']], filename='bulb.ico', tooltip='Home Control Interface')
        b = Bridge('192.168.0.134')  # Hue Hub Connection
        Heater = SmartPlug("192.168.0.146")  # Heater Smart Plug Connection
        # print(pf(Heater.get_sysinfo()))  # this prints lots of information about the device
        Lighthouse = SmartPlug("192.168.0.196")  # Lighthouse Smart Plug Connection
        # print(pf(Lighthouse.get_sysinfo()))  # this prints lots of information about the device


    # Hue Bulb Functions
    def SetScene(self, obj, SceneName):
        obj.run_scene('My Bedroom', SceneName, 1)


    def SetLightsOff(self, obj):
        obj.set_group('My Bedroom', 'on', False)


    def HeaterToggle(self, obj, button):
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
        if obj.get_sysinfo()["relay_state"] == 0:
            obj.turn_on()
            button.config(relief='sunken')
        subprocess.call("D:/My Installed Games/Steam Games/steamapps/common/SteamVR/bin/win64/vrstartup.exe")

    # Requires AHK and NirCMD to work
    ahk = AHK(executable_path='C:/Program Files/AutoHotkey/AutoHotkey.exe')
    # These simply name AHK commands that are ran as functions.
    ahk_headphones = 'Run nircmd setdefaultsounddevice "Headphones"'
    ahk_speakers = 'Run nircmd setdefaultsounddevice "Logitech Speakers" 1'
    ahk_tv = 'Run nircmd setdefaultsounddevice "SONY TV" 1'
    ahk_SurfaceAux = 'Run nircmd setdefaultsounddevice "Aux"'
    ahk_SurfaceSpeakers = 'Run nircmd setdefaultsounddevice "Speakers"'


    def SetSoundDevice(self, device):
        ahk.run_script(device, blocking=False)

    def Display_Switch(self, mode, obj):
        '''Switches display to the mode entered as an argument. Works for PC and TV mode.'''
        def callback():
            subprocess.call([f'{os.getcwd()}/Batches/{mode} Mode.bat'])
            time.sleep(10)
            if mode == 'PC':
                obj.run_script(ahk_speakers, blocking=False)
            else:
                obj.run_script(ahk_tv, blocking=False)
            print(f'{mode} Mode Set')
        t = threading.Thread(target=callback)
        t.start()


    def Timed_Power_Control(self):
        script = "D:/Google Drive/Coding/Python/Scripts/1-Complete-Projects/Timed-Shutdown/Timed_Shutdown.pyw"
        os.system(script)
