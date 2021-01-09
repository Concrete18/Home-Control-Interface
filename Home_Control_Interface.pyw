from tkinter import Tk, Button, LabelFrame, messagebox
from pyHS100 import SmartPlug
from pyHS100 import Discover  # unused normally
import PySimpleGUIWx as sg
from phue import Bridge
from time import sleep
from ahk import AHK
import subprocess
import threading
import socket
import os


class Home:


    def __init__(self):
        self.check_pi_status = 1
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        if os.getcwd() != self.script_dir:
            print('Current Working Directory is Different.')
            os.chdir(self.script_dir)
        self.window_title = 'Home Control Interface'
        self.update_delay = 1000
        # device init
        self.Hue_Hub = Bridge('192.168.0.134')
        self.Heater = SmartPlug('192.168.0.146')
        self.heater_plugged_in = 1
        self.Lighthouse = SmartPlug('192.168.0.197')
        self.lighthouse_plugged_in = 0
        self.ras_pi = '192.168.0.114'
        # AHK
        self.ahk = AHK(executable_path='C:/Program Files/AutoHotkey/AutoHotkey.exe')
        # Python Scripts
        self.switch_to_abc = "D:/Google Drive/Coding/Python/Scripts/1-Complete-Projects/Roku-Control/Instant_Set_to_ABC.py"
        self.timed_shutdown = "D:/Google Drive/Coding/Python/Scripts/1-Complete-Projects/Timed-Shutdown/Timed_Shutdown.pyw"


    def check_pi(self):
        '''
        Checks if Pi is up.
        '''
        def callback():
            sleep(10)
            if self.check_pi_status == 1:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex((self.ras_pi, 22))
                if result == 0:
                    print("Raspberry Pi is running")
                else:
                    messagebox.showwarning(title=self.window_title, message=f'Raspberry Pi is not online.')
        pi_thread = threading.Thread(target=callback)
        pi_thread.start()


    # Hue Bulb Functions`
    def set_scene(self, scene_name):
        '''
        Set Hue scene function.
        '''
        self.Hue_Hub.run_scene('My Bedroom', scene_name, 1)


    @staticmethod
    def smart_plug_toggle(name, device, button):
        '''
        Smart Plug toggle function.
        '''
        try:
            if device.get_sysinfo()["relay_state"] == 0:
                device.turn_on()
                button.config(relief='sunken')  # On State
            else:
                device.turn_off()
                button.config(relief='raised')  # Off State
        except:
            print(f'{name} Error')


    def start_vr(self):
        '''
        Runs SteamVR shortcut and turns on lighthouse plugged into smart plug for tracking if it is off.
        '''
        if self.lighthouse_plugged_in and self.Lighthouse.get_sysinfo()["relay_state"] == 0:
            self.Lighthouse.turn_on()
            self.LighthouseButton.config(relief='sunken')
        steamvr_path = "D:/My Installed Games/Steam Games/steamapps/common/SteamVR/bin/win64/vrstartup.exe"
        if os.path.isfile(steamvr_path):
            subprocess.call(steamvr_path)


    def set_sound_device(self, device):
        '''
        Set Sound Device Function. Requires AHK and NirCMD to work.
        '''
        self.ahk.run_script(f'Run nircmd setdefaultsounddevice "{device}" 1', blocking=False)


    def display_switch(self, mode):
        '''
        Switches display to the mode entered as an argument. Works for PC and TV mode.
        '''
        def callback(mode):
            subprocess.call([f'{self.script_dir}/Batches/{mode} Mode.bat'])
            sleep(10)
            if mode == 'PC':
                self.set_sound_device('Logitech Speakers')
            else:
                self.display_switch('SONY TV')
            print(f'{mode} Mode Set')
        Switch = threading.Thread(target=callback, args=(mode,))
        Switch.start()


    def python_script_runner(self, script):
        '''
        Runs Timed Power Control Function after switching the directory to it's location.
        '''
        os.chdir(os.path.split(script)[0])
        subprocess.call(["python", script], shell=False)
        os.chdir(self.script_dir)


    def create_window(self):
        '''
        Creates Home Control Interface.
        '''
        self.Home_Interface = Tk()
        window_width = 1108
        window_height = 580
        width = int((self.Home_Interface.winfo_screenwidth()-window_width)/2)
        height = int((self.Home_Interface.winfo_screenheight()-window_height)/2)
        self.Home_Interface.geometry(f'{window_width}x{window_height}+{width}+{height}')
        self.Home_Interface.title(self.window_title)
        self.Home_Interface.iconbitmap(self.Home_Interface, 'bulb.ico')
        self.Home_Interface.configure(bg='white')
        self.Home_Interface.resizable(width=False, height=False)

        # default values for interface
        background = 'white'
        base_font = ('Arial Bold', 20)
        pad_x = 10
        pad_y = 10

        # Frames
        HueLightControlFrame = LabelFrame(self.Home_Interface, text='Hue Light Control', bg=background,
            font=base_font, padx=pad_x, pady=pad_y, width=2000, height=4000)
        HueLightControlFrame.grid(column=0, rowspan=2, padx=pad_x, pady=pad_y, sticky='nsew')

        SmartPlugControlFrame = LabelFrame(self.Home_Interface, text='Smart Plug Control', bg=background,
            font=base_font, padx=pad_x, pady=pad_y, width=300, height=390)
        SmartPlugControlFrame.grid(column=1, row=0, padx=pad_x, pady=pad_y, sticky='nsew')

        AudioSettingsFrame = LabelFrame(self.Home_Interface, text='Audio Settings', bg=background, font=base_font,
            padx=pad_x, pady=pad_y, width=300, height=390)
        AudioSettingsFrame.grid(column=1, row=1, padx=pad_x, pady=pad_y, sticky='nsew')

        # Buttons
        LightsOn = Button(HueLightControlFrame, text="Lights On", command=lambda: self.set_scene('Normal'),
            font=("Arial", 19), width=15)
        LightsOn.grid(column=0, row=1, padx=pad_x, pady=pad_y)

        TurnAllOff = Button(HueLightControlFrame, text="Lights Off",
            command=lambda: self.Hue_Hub.set_group('My Bedroom', 'on', False), font=("Arial", 19), width=15)
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

        self.HeaterButton = Button(SmartPlugControlFrame, text="Heater Toggle", font=("Arial", 19), width=15,
            command=lambda: self.smart_plug_toggle('Heater', self.Heater, self.HeaterButton), state='disabled',)
        self.HeaterButton.grid(column=0, row=5, padx=pad_x, pady=pad_y)

        UnsetButton = Button(SmartPlugControlFrame, text="Unset", state='disabled',
            command='ph', font=("Arial", 19), width=15)
        UnsetButton.grid(column=1, row=5, padx=pad_x, pady=pad_y)

        Script_Shortcuts = LabelFrame(self.Home_Interface, text='Script Shortcuts', bg=background, font=base_font,
            padx=pad_x, pady=pad_y, width=300, height=200)
        Script_Shortcuts.grid(column=0, row=3, padx=pad_x, pady=pad_y, sticky='nsew')

        RokuButton = Button(Script_Shortcuts, text="Set Roku to ABC",
            command=lambda: self.python_script_runner(self.switch_to_abc), font=("Arial", 19), width=15)
        RokuButton.grid(column=0, row=0, padx=pad_x, pady=pad_y)

        TimerControl = Button(Script_Shortcuts, text="Power Control",
            command=lambda: self.python_script_runner(self.timed_shutdown), font=("Arial", 19), width=15)
        TimerControl.grid(column=1, row=0, padx=pad_x, pady=pad_y)

        current_pc = socket.gethostname()
        if current_pc == 'Aperture-Two':
            VRFrame = LabelFrame(self.Home_Interface, text='VR Settings', bg=background, font=base_font,
                padx=pad_x, pady=pad_y, width=300, height=400)
            VRFrame.grid(column=0, row=2, padx=pad_x, pady=pad_x, sticky='nsew')

            StartVRButton = Button(VRFrame, text="Start VR",
                command=self.start_vr, font=("Arial", 19), width=15)
            StartVRButton.grid(column=0, row=9, padx=pad_x, pady=pad_y)

            self.LighthouseButton = Button(VRFrame, text="Lighthouse Toggle", state='disabled', font=("Arial", 19),
                command=lambda: self.smart_plug_toggle('Lighthouse', self.Lighthouse, self.LighthouseButton), width=15,)
            self.LighthouseButton.grid(column=1, row=9, padx=pad_x, pady=pad_y)

            AudioToSpeakers = Button(AudioSettingsFrame, text="Speaker Audio",
                command=lambda: self.set_sound_device('Logitech Speakers'), font=("Arial", 19), width=15)
            AudioToSpeakers.grid(column=0, row=7, padx=pad_x, pady=pad_y)

            AudioToHeadphones = Button(AudioSettingsFrame, text="Headphone Audio",
                command=lambda: self.set_sound_device('Headphones'), font=("Arial", 19),width=15)
            AudioToHeadphones.grid(column=1, row=7, padx=pad_x, pady=pad_y)

            ProjectionFrame = LabelFrame(self.Home_Interface, text='Projection', bg=background, font=base_font,
                padx=pad_x, pady=pad_y, width=300, height=400)
            ProjectionFrame.grid(column=1, row=2, padx=pad_x, pady=pad_y, sticky='nsew')

            SwitchToPCMode = Button(ProjectionFrame, text="PC Mode", command=lambda: self.display_switch('PC'),
                font=("Arial", 19), width=15)
            SwitchToPCMode.grid(column=0, row=9, padx=pad_x, pady=pad_y)

            SwitchToTVMode = Button(ProjectionFrame, text="TV Mode", command=lambda: self.display_switch('SONY TV'),
                font=("Arial", 19), width=15)
            SwitchToTVMode.grid(column=1, row=9, padx=pad_x, pady=pad_y)
        elif current_pc == 'Surface-1':
            AudioToSpeakers = Button(AudioSettingsFrame, text="Speaker Audio",
                command=lambda: self.set_sound_device('Speakers'), font=("Arial", 19), width=15)
            AudioToSpeakers.grid(column=0, row=7, padx=pad_x, pady=pad_y)

            AudioToHeadphones = Button(AudioSettingsFrame, text="Headphone Audio",
                command=lambda: self.set_sound_device('Aux'), font=("Arial", 19),width=15)
            AudioToHeadphones.grid(column=1, row=7, padx=pad_x, pady=pad_y)
        else:
            messagebox.showwarning(title=self.window_title, message='Current PC is unknown.')

        #  Smart Plugs running through state check function.
        self.plug_state_check()

        self.Home_Interface.mainloop()


    def plug_state_check(self):
        '''
        Gets current state of entered device and updates button relief.
        '''
        def callback():
            buttons = {}
            if self.lighthouse_plugged_in:
                buttons[self.Lighthouse] = self.LighthouseButton
                self.LighthouseButton.config(state='normal')
            if self.heater_plugged_in:
                buttons[self.Heater] = self.HeaterButton
                self.HeaterButton.config(state='normal')
            for device, button in buttons.items():
                try:
                    if device.get_sysinfo()["relay_state"] == 1:
                        button.config(relief='sunken')  # On State
                    else:
                        button.config(relief='raised')  # Off State
                except Exception as e:
                    print('Smart Plug', e)
                    messagebox.showwarning(title=self.window_title, message=f'Error communicating with {device}.')
        pi_thread = threading.Thread(target=callback)
        pi_thread.start()
        self.Home_Interface.after(1000, self.plug_state_check)


    def create_tray(self):
        '''
        Creates the system tray. Clicking the Lightbulb ones the interface and right clicking it shows quick
        lighting control options.
        '''
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
                self.Hue_Hub.set_group('My Bedroom', 'on', False)
            elif event == '__ACTIVATED__':
                self.create_window()


if __name__ == "__main__":
    Home =  Home()
    Home.check_pi()
    Home.create_tray()
