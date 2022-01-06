from pathlib import Path
from pyHS100 import SmartPlug
from phue import Bridge

import sys, subprocess, threading, socket, time, json, os, playsound
import tkinter as tk
from tkinter import messagebox
from ahk import AHK

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

class Computer:

    with open('config.json') as json_file:
        data = json.load(json_file)
    # settings
    check_pi_status = data['Settings']['check_pi_status']
    computer_status_interval = data['Settings']['computer_status_interval']  # interval in seconds
    # raspberry pi
    rasp_pi = data['IP_Addresses']['rasp_pi']
    # ahk
    ahk = AHK(executable_path='C:/Program Files/AutoHotkey/AutoHotkey.exe')


    def shutdown(self):
        '''
        Shutdown the PC after running some other custom commands.
        '''
        # TODO add proper icon or new window type without using messagebox
        tk.Tk().withdraw()
        response = messagebox.askquestion(title='Shutdown', message=f'Do you want to run custom shutdown?.')
        print(response)
        if response == 'yes':
            print('Shutting Down')
            os.system("shutdown /s /t 1")

    def set_sound_device(self, device):
        '''
        Set Sound Device Function. Requires AHK and NirCMD to work.
        '''
        if device == 'Headphones':
            self.ahk.run_script(f'Run nircmd setdefaultsounddevice "{device}" 0', blocking=False)
            self.ahk.run_script(f'Run nircmd setdefaultsounddevice "{device}" 2', blocking=False)
            self.ahk.run_script(f'Run nircmd setdefaultsounddevice "Headset Microphone" 2', blocking=False)
        else:
            self.ahk.run_script(f'Run nircmd setdefaultsounddevice "{device}" 1', blocking=False)

    @staticmethod
    def python_script_runner(script):
        '''
        Runs script using full path after changing the working directory in case of relative paths in script.
        '''
        subprocess.run([sys.executable, script], cwd=os.path.dirname(script))

    def display_switch(self, mode, script_dir, root_window=None):
        '''
        Switches display to the mode entered as an argument. Works for PC and TV mode.
        '''
        print(script_dir)
        def callback(mode):
            subprocess.call([f'{script_dir}/Batches/{mode} Mode.bat'])
            if mode == 'PC':
                self.set_sound_device('Logitech Speakers')
            else:
                time.sleep(10)
                self.set_sound_device('SONY TV')
            print(f'{mode} Mode Set')
        Switch = threading.Thread(target=callback, args=(mode,))
        Switch.start()
        if root_window != None:
            root_window.destroy()

    def check_pi(self):
        '''
        Sets rpi_status based on if the Pi is online or not.
        '''
        if self.check_pi_status == 1:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((self.rasp_pi, 22))
            if result == 0:
                self.rpi_status = 'Online'
            else:
                self.rpi_status = 'Offline'

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

class Lights:

    with open('config.json') as json_file:
        data = json.load(json_file)
    hue_hub = Bridge(data['IP_Addresses']['hue_hub'])


    def on(self):
        '''
        Sets all lights to on.
        '''
        print('Turning Lights On.')
        self.hue_hub.run_scene('My Bedroom', 'Normal', 1)

    def off(self):
        '''
        Sets all lights to off.
        '''
        print('Turning Lights Off.')
        self.hue_hub.set_group('My Bedroom', 'on', False)

    def set_scene(self, scene):
        '''
        Sets the Hue lights to the entered scene.
        '''
        print(f'Setting lights to {scene}.')
        self.hue_hub.run_scene('My Bedroom', scene, 1)

    def toggle_lights(self):
        '''
        Turns on all lights if they are all off or turns lights off if any are on.
        '''
        for lights in self.hue_hub.lights:
            if self.hue_hub.get_light(lights.name, 'on'):
                self.off()
                return
        self.on()

    def run(self):
        '''
        Runs in CLI mode.
        '''
        try:
            type = sys.argv[1].lower()
        except IndexError:
            type = 'toggle'
        if type == 'toggle':
            self.toggle_lights()
        elif type == 'on':
            self.on()
        elif type == 'off':
            self.off()

class Home:

    with open('config.json') as json_file:
        data = json.load(json_file)
    # settings
    debug = data['Settings']['debug']
    # classes init
    lights = Lights()
    computer = Computer()

    # plug setup
    json_file = Path('data.json')
    with open(json_file, 'r') as f:
        data = json.load(f)
        if data['heater']:
            heater = SmartPlug(data['heater'])
        else:
            heater = False
        if data['lighthouse']:
            lighthouse = SmartPlug(data['lighthouse'])
        else:
            lighthouse = False

    @staticmethod
    def toggle(device):
        '''
        Smart Plug toggle function.
        '''
        try:
            if device.get_sysinfo()["relay_state"] == 0:
                device.turn_on()
            else:
                device.turn_off()
        except Exception as error:
            print(f'Error toggling device\n{error}')


    def run_command(self):
        '''
        Runs `command`.
        '''
        lights = Lights()
        if len(sys.argv) == 1:
            print('No args.')
            return
        command = sys.argv[1]
        if command == 'toggle_lights':
            lights.toggle_lights()

        elif command == 'backlight':
            self.lights.set_scene('Backlight')

        elif command == 'switch_to_pc':
            self.computer.display_switch('PC', self.script_dir)

        elif command == 'switch_to_tv':
            self.computer.display_switch('TV', self.script_dir)

        elif command == 'toggle_heater':
            if self.heater:
                self.toggle(device=self.heater)
            else:
                playsound('Audio/Heater_not_found.wav')


if __name__ == "__main__":
    control = Home()
    control.run_command()
