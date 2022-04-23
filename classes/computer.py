import sys, subprocess, threading, socket, time, json, os
import tkinter as tk
from tkinter import messagebox
from ahk import AHK
from pathlib import Path


class Computer:

    with open("config.json") as json_file:
        data = json.load(json_file)
    # settings
    check_pi_status = data["Settings"]["check_pi_status"]
    # interval in seconds
    computer_status_interval = data["Settings"]["status_interval"]
    # raspberry pi ip
    rasp_pi = data["IP_Addresses"]["rasp_pi"]
    # AHK path
    ahk = AHK(executable_path="C:/Program Files/AutoHotkey/AutoHotkey.exe")
    logitech_options = Path(
        "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Logitech\Logitech Options.lnk"
    )

    def shutdown(self):
        """
        Shutdown the PC after running some other custom commands.
        """
        # TODO add proper icon or new window type without using messagebox
        tk.Tk().withdraw()
        msg = f"Do you want to run custom shutdown?."
        response = messagebox.askquestion(title="Shutdown", message=msg)
        if response == "yes":
            print("Shutting Down")
            self.display_switch("PC")
            time.sleep(2)
            os.system("shutdown /s /t 1")

    def set_sound_device(self, device):
        """
        Set Sound Device Function. Requires AHK and NirCMD to work.

        Console = 0
        Multimedia = 1
        Communications = 2
        """
        base_cmd = "Run nircmd setdefaultsounddevice"
        if device == "Headphones":
            self.ahk.run_script(f'{base_cmd} "{device}" 0', blocking=False)
            self.ahk.run_script(f'{base_cmd} "{device}" 2', blocking=False)
            self.ahk.run_script(
                f'{base_cmd} "Headset Microphone" 2',
                blocking=False,
            )
        else:
            self.ahk.run_script(f'{base_cmd} "{device}" 1', blocking=False)

    @staticmethod
    def python_script_runner(script):
        """
        Runs script using full path after changing the working directory in case of relative paths in script.
        """
        subprocess.run([sys.executable, script], cwd=os.path.dirname(script))

    def display_switch(self, mode, root_window=None):
        """
        Switches display to the mode entered as an argument. Works for PC and TV mode.
        """

        def callback(mode):
            subprocess.call([f"Batches/{mode} Mode.bat"])
            if mode == "PC":
                self.set_sound_device("Logitech Speakers")
                if self.logitech_options.exists:
                    try:
                        subprocess.call([self.logitech_options])
                    except OSError:
                        print("Failed to run Logitech Options")
            else:
                time.sleep(10)
                self.set_sound_device("SONY TV")
            print(f"{mode} Mode Set")

        Switch = threading.Thread(target=callback, args=(mode,))
        Switch.start()
        if root_window != None:
            root_window.destroy()

    def check_pi(self):
        """
        Sets rpi_status based on if the Pi is online or not.
        """
        if self.check_pi_status == 1:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((self.rasp_pi, 22))
            if result == 0:
                self.rpi_status = "Online"
            else:
                self.rpi_status = "Offline"
        return self.rpi_status

    @staticmethod
    def readable_time_since(seconds):
        """
        Returns time since based on seconds argument in the unit of time that makes the most sense
        rounded to 1 decimal place.
        """
        if seconds < (60 * 60):  # seconds in minute * minutes in hour
            minutes = round(seconds / 60, 1)  # seconds in a minute
            return f"{minutes} minutes"
        elif seconds < (
            60 * 60 * 24
        ):  # seconds in minute * minutes in hour * hours in a day
            hours = round(seconds / (60 * 60), 1)  # seconds in minute * minutes in hour
            return f"{hours} hours"
        else:
            days = round(
                seconds / 86400, 1
            )  # seconds in minute * minutes in hour * hours in a day
            return f"{days} days"


if __name__ == "__main__":
    App = Computer()
    App.display_switch(mode="PC")
    # print(App.check_pi())
