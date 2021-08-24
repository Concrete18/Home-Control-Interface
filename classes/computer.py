import sys, subprocess, threading, socket, time, json, os
import tkinter as tk
from tkinter import messagebox
from ahk import AHK

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


    def display_switch(self, mode, script_dir):
        '''
        Switches display to the mode entered as an argument. Works for PC and TV mode.
        '''
        def callback(mode):
            subprocess.call([f'{script_dir}/Batches/{mode} Mode.bat'])
            time.sleep(10)
            if mode == 'PC':
                self.set_sound_device('Logitech Speakers')
            else:
                self.display_switch('SONY TV')
            print(f'{mode} Mode Set')
        Switch = threading.Thread(target=callback, args=(mode,))
        Switch.start()


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
