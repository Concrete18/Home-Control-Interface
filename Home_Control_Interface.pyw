from tkinter import Tk, Button, Label, LabelFrame, messagebox, LEFT
import tkinter as tk
from pyHS100 import SmartPlug
from pyHS100 import Discover  # unused normally
import PySimpleGUIWx as sg
from phue import Bridge
from time import sleep
from ahk import AHK
import subprocess
import threading
import socket
import psutil
import time
import os


class Home:


    def __init__(self):
        # sets script directory
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        if os.getcwd() != self.script_dir:
            print('Current Working Directory is Different.')
            os.chdir(self.script_dir)
        # defaults
        self.window_title = 'Home Control Interface'
        # device init
        self.Hue_Hub = Bridge('192.168.0.134')
        self.Heater = SmartPlug('192.168.0.146')
        self.heater_plugged_in = 1
        self.Lighthouse = SmartPlug('192.168.0.197')
        self.lighthouse_plugged_in = 0
        self.ras_pi = '192.168.0.114'
        self.check_pi_status = 1
        # ahk
        self.ahk = AHK(executable_path='C:/Program Files/AutoHotkey/AutoHotkey.exe')
        # python scripts
        self.switch_to_abc = "D:/Google Drive/Coding/Python/Scripts/1-Complete-Projects/Roku-Control/Instant_Set_to_ABC.py"
        self.timed_shutdown = "D:/Google Drive/Coding/Python/Scripts/1-Complete-Projects/Timed-Shutdown/Timed_Shutdown.pyw"
        # Status vars
        self.rpi_status = 'Checking Status'
        self.boot_time = psutil.boot_time()


    def check_pi(self):
        '''
        Checks if Pi is up.
        '''
        def callback():
            if self.check_pi_status == 1:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex((self.ras_pi, 22))
                if result == 0:
                    self.rpi_status = 'Online'
                else:
                    self.rpi_status = 'Offline'
                    messagebox.showwarning(title=self.window_title, message=f'Raspberry Pi is not online.')
        pi_thread = threading.Thread(target=callback)
        pi_thread.start()


    @staticmethod
    def readable_time_since(seconds):
        '''
        Returns time since based on seconds argument in the unit of time that makes the most sense
        rounded to 1 decimal place.
        '''
        if seconds < (60 * 60):  # seconds in minute * minutes in hour
            minutes = round(seconds / 60, 1)  # seconds in a minute
            return f'{minutes} minutes'
        elif seconds < (60 * 60 * 24):  # seconds in minute * minutes in hour * hours in a day
            hours = round(seconds / (60 * 60), 1)  # seconds in minute * minutes in hour
            return f'{hours} hours'
        else:
            days = round(seconds / 86400, 1)  # seconds in minute * minutes in hour * hours in a day
            return f'{days} days'


    def check_computer_status(self):
        def callback():
            mem = psutil.virtual_memory()
            virt_mem = f'{round(mem.available/1024/1024/1024, 1)}/{round(mem.total/1024/1024/1024, 1)}'
            self.uptime.set(self.readable_time_since(int(time.time() - self.boot_time)))
            self.cpu_util.set(f'{psutil.cpu_percent(interval=1)}%')
            self.virt_mem.set(f'{virt_mem} GB')
            self.pi_status.set(self.rpi_status)
        pi_thread = threading.Thread(target=callback)
        pi_thread.start()
        self.Home_Interface.after(5000, self.check_computer_status)


    # Hue Bulb Functions
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
        Runs script using full path after changing the working directory in case of relative paths in script.
        '''
        os.chdir(os.path.split(script)[0])
        subprocess.call(["python", script], shell=False)
        os.chdir(self.script_dir)


    def create_window(self):
        '''
        Creates Home Control Interface.
        '''
        self.Home_Interface = Tk()
        self.uptime = tk.StringVar()
        self.cpu_util = tk.StringVar()
        self.cpu_load = tk.StringVar()
        self.virt_mem = tk.StringVar()
        self.pi_status = tk.StringVar()
        self.pi_status.set(self.rpi_status)
        window_height = 724
        window_width = 1108
        height = int((self.Home_Interface.winfo_screenheight()-window_height)/2)
        width = int((self.Home_Interface.winfo_screenwidth()-window_width)/2)
        self.Home_Interface.geometry(f'+{width}+{height}')
        # self.Home_Interface.geometry(f'{window_width}x{window_height}+{width}+{height}')
        self.Home_Interface.title(self.window_title)
        self.Home_Interface.iconbitmap(self.Home_Interface, 'bulb.ico')
        self.Home_Interface.configure(bg='white')
        self.Home_Interface.resizable(width=False, height=False)

        # default values for interface
        background = 'white'
        bold_base_font = ('Arial Bold', 20)
        small_bold_base_font = ('Arial Bold', 16)
        small_base_font = ('Arial', 12)
        pad_x = 10
        pad_y = 10

        # Frames
        # Left Frames
        ComputerStatus = LabelFrame(self.Home_Interface, text='Computer Status', bg=background,
            font=bold_base_font, padx=pad_x, pady=pad_y, width=300, height=150)
        ComputerStatus.grid(column=0, row=0, padx=pad_x, pady=pad_y, sticky='nsew')

        HueLightControlFrame = LabelFrame(self.Home_Interface, text='Hue Light Control', bg=background,
            font=bold_base_font, padx=pad_x, pady=pad_y, width=300, height=400)
        HueLightControlFrame.grid(column=0, row=1, rowspan=2, padx=pad_x, pady=pad_y, sticky='nsew')

        Script_Shortcuts = LabelFrame(self.Home_Interface, text='Script Shortcuts', bg=background, font=bold_base_font,
            padx=pad_x, pady=pad_y, width=300, height=200)
        Script_Shortcuts.grid(column=0, row=3, padx=pad_x, pady=pad_y, sticky='nsew')

        # Right Frames
        SmartPlugControlFrame = LabelFrame(self.Home_Interface, text='Smart Plug Control', bg=background,
            font=bold_base_font, padx=pad_x, pady=pad_y, width=300, height=150)
        SmartPlugControlFrame.grid(column=1, row=0, padx=pad_x, pady=pad_y, sticky='nsew')

        AudioSettingsFrame = LabelFrame(self.Home_Interface, text='Audio Settings', bg=background, font=bold_base_font,
            padx=pad_x, pady=pad_y, width=300, height=390)
        AudioSettingsFrame.grid(column=1, row=1, padx=pad_x, pady=pad_y, sticky='nsew')

        ProjectionFrame = LabelFrame(self.Home_Interface, text='Projection', bg=background, font=bold_base_font,
            padx=pad_x, pady=pad_y, width=300, height=400)
        ProjectionFrame.grid(column=1, row=2, padx=pad_x, pady=pad_y, sticky='nsew')

        VRFrame = LabelFrame(self.Home_Interface, text='VR Settings', bg=background, font=bold_base_font,
            padx=pad_x, pady=pad_y, width=300, height=400)
        VRFrame.grid(column=1, row=3, padx=pad_x, pady=pad_x, sticky='nsew')

        # Labels
        self.ComputerInfo = Label(ComputerStatus, text='|PC Uptime|', bg=background, font=small_bold_base_font)
        self.ComputerInfo.grid(column=0, row=0)
        self.ComputerInfo = Label(ComputerStatus, textvariable=self.uptime, bg=background, font=small_base_font)
        self.ComputerInfo.grid(column=0, row=1)

        self.ComputerInfo = Label(ComputerStatus, text='|CPU Util|', bg=background, font=small_bold_base_font)
        self.ComputerInfo.grid(column=1, row=0)
        self.ComputerInfo = Label(ComputerStatus, textvariable=self.cpu_util, bg=background, font=small_base_font)
        self.ComputerInfo.grid(column=1, row=1)

        self.ComputerInfo = Label(ComputerStatus, text='|Memory|', bg=background, font=small_bold_base_font)
        self.ComputerInfo.grid(column=2, row=0)
        self.ComputerInfo = Label(ComputerStatus, textvariable=self.virt_mem, bg=background, font=small_base_font)
        self.ComputerInfo.grid(column=2, row=1)

        self.ComputerInfo = Label(ComputerStatus, text='|Pi Status|', bg=background, font=small_bold_base_font)
        self.ComputerInfo.grid(column=3, row=0)
        self.ComputerInfo = Label(ComputerStatus, textvariable=self.pi_status, bg=background, font=small_base_font)
        self.ComputerInfo.grid(column=3, row=1)

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

        RokuButton = Button(Script_Shortcuts, text="Set Roku to ABC",
            command=lambda: self.python_script_runner(self.switch_to_abc), font=("Arial", 19), width=15)
        RokuButton.grid(column=0, row=0, padx=pad_x, pady=pad_y)

        TimerControl = Button(Script_Shortcuts, text="Power Control",
            command=lambda: self.python_script_runner(self.timed_shutdown), font=("Arial", 19), width=15)
        TimerControl.grid(column=1, row=0, padx=pad_x, pady=pad_y)

        current_pc = socket.gethostname()
        if current_pc == 'Aperture-Two':
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
        self.check_computer_status()

        self.Home_Interface.update()
        print (self.Home_Interface.winfo_width())
        # TODO Fix incorrect height
        print (self.Home_Interface.winfo_height())

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
