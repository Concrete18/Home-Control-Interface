from pyHS100 import SmartPlug
import PySimpleGUIWx as sg
from phue import Bridge



class Home_Interface:
    def __init__(self):
        tray = sg.SystemTray(menu= ['menu',['Exit', 'Lights On']], filename='bulb.ico', tooltip='Home Control Interface')
        b = Bridge('192.168.0.134')  # Hue Hub Connection
        Heater = SmartPlug("192.168.0.146")  # Heater Smart Plug Connection
        # print(pf(Heater.get_sysinfo()))  # this prints lots of information about the device
        Lighthouse = SmartPlug("192.168.0.196")  # Lighthouse Smart Plug Connection
        # print(pf(Lighthouse.get_sysinfo()))  # this prints lots of information about the device


    # Hue Bulb Functions
    def SetScene(self,SceneName):
        b.run_scene('My Bedroom', SceneName, 1)


    def SetLightsOff(self):
        b.set_group('My Bedroom', 'on', False)


    def HeaterToggle():
        try:
            if Heater.get_sysinfo()["relay_state"] == 0:
                Heater.turn_on()
                HeaterButton.config(relief='sunken')  # On State
            else:
                Heater.turn_off()
                HeaterButton.config(relief='raised')  # Off State
        except:
            print('Heater Error')


    def LighthouseToggle():
        try:
            if Lighthouse.get_sysinfo()["relay_state"] == 0:
                Lighthouse.turn_on()
                VRLighthouseButton.config(relief='sunken')
            else:
                Lighthouse.turn_off()
                VRLighthouseButton.config(relief='raised')
        except:
            print('Lighthouse Error')


    def StartVR():
        if Lighthouse.get_sysinfo()["relay_state"] == 0:
            Lighthouse.turn_on()
            VRLighthouseButton.config(relief='sunken')
        subprocess.call("D:/My Installed Games/Steam Games/steamapps/common/SteamVR/bin/win64/vrstartup.exe")


    def display_switch(mode):
        '''Switches display to the mode entered as an argument. Works for PC and TV mode.'''
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


    def Timed_Power_Control():
        script = "D:/Google Drive/Coding/Python/Scripts/1-Complete-Projects/Timed-Shutdown/Timed_Shutdown.pyw"
        os.system(script)
