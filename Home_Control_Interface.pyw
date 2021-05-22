from tkinter import Tk, Button, Label, LabelFrame, messagebox
import tkinter as tk
import psutil, time, sys, os, socket, threading, subprocess, re, json
from pyHS100 import SmartPlug, Discover
import PySimpleGUIWx as sg
from phue import Bridge
from time import sleep
from ahk import AHK


class Smart_Hub:
    pass


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

    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    with open('config.json') as json_file:
        data = json.load(json_file)
    # settings
    debug = data['Settings']['debug']
    check_pi_status = data['Settings']['check_pi_status']
    computer_status_interval = data['Settings']['computer_status_interval']  # interval in seconds
    # defaults
    icon = 'bulb.ico'
    window_title = 'Home Control Interface'
    window_state = 0
    # device init
    Lights = Lights()
    rasp_pi = data['IP_Addresses']['rasp_pi']
    # ahk
    ahk = AHK(executable_path='C:/Program Files/AutoHotkey/AutoHotkey.exe')
    # python scripts
    switch_to_abc = "D:/Google Drive/Coding/Python/Scripts/1-Complete-Projects/Roku-Control/Instant_Set_to_ABC.py"
    timed_shutdown = "D:/Google Drive/Coding/Python/Scripts/1-Complete-Projects/Timed-Shutdown/Timed_Shutdown.pyw"
    # Status vars
    rpi_status = 'Checking Status'
    boot_time = psutil.boot_time()
    # tray buttons


    def discover_smart_plugs(self):
        '''
        Finds all smartplugs on the network and turns on ones used within this script if its name shows up.
        '''
        print('Checking for active smart plugs:')
        self.lighthouse_plugged_in = 0
        self.heater_plugged_in = 0
        pattern = "\d{1,3}.\d{1,3}\.\d{1,3}\.\d{1,3}"
        for dev in Discover.discover().values():
            ip = re.findall(pattern, str(dev))
            if len(ip) > 0:
                if 'heater' in str(dev).lower():
                    print('> Heater Found')
                    self.Heater = SmartPlug(ip[0])
                    self.heater_plugged_in = 1
                if 'tv light house' in str(dev).lower():
                    print('> Lighthouse Found')
                    self.Lighthouse = SmartPlug(ip[0])
                    self.lighthouse_plugged_in = 1


    def setup_tray(self):
        '''
        Sets up tray object with options.
        '''
        buttons = [
            'Lights On',
            'Lights Off',
            'Backlight Scene',
            '---',
            'Set audio to Speaker',
            'Set audio to Headphones',
            '---'
        ]
        # togglable options
        if self.heater_plugged_in:
            buttons.extend(['Heater Toggle', '---'])
        # end of options
        buttons.append('Exit')
        # tray object creation
        self.Tray = sg.SystemTray(
            menu=['menu', buttons],
            filename=self.icon,
            tooltip=self.window_title)
        print('Tray Setup')


    def update_tray(self):
        event = self.Tray.Read()
        if event == 'Exit':
            exit()
        elif event == 'Lights On':
            self.Lights.on()
        elif event == 'Lights Off':
            self.Lights.off()
        elif event == 'Backlight Scene':
            self.Lights.set_scene('Backlight')
        elif event == 'Heater Toggle':
            self.smart_plug_toggle(self.Heater)
        elif event == '__ACTIVATED__':
            self.create_window()
        self.Home_Interface.after(0, self.update_tray)


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


    def check_computer_status(self):
        mem = psutil.virtual_memory()
        virt_mem = f'{round(mem.used/1024/1024/1024, 1)}/{round(mem.total/1024/1024/1024, 1)}'
        self.uptime.set(self.readable_time_since(int(time.time() - self.boot_time)))
        self.cpu_util.set(f'{psutil.cpu_percent(interval=0.1)}%')
        self.virt_mem.set(f'{virt_mem} GB')
        self.Home_Interface.after(self.computer_status_interval*1000, self.check_computer_status)


    @staticmethod
    def smart_plug_toggle(device, name='device', button=0):
        '''
        Smart Plug toggle function.
        '''
        try:
            if device.get_sysinfo()["relay_state"] == 0:
                device.turn_on()
                if button != 0:
                    button.config(relief='sunken')  # On State
            else:
                device.turn_off()
                if button != 0:
                    button.config(relief='raised')  # Off State
        except Exception as error:
            print(f'Error toggling device\n{error}\n{name}')


    def start_vr(self):
        '''
        Runs SteamVR shortcut and turns on lighthouse plugged into smart plug for tracking if it is off.
        '''
        self.Lights.on()
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


    @staticmethod
    def python_script_runner(script):
        '''
        Runs script using full path after changing the working directory in case of relative paths in script.
        '''
        subprocess.run([sys.executable, script], cwd=os.path.dirname(script))


    def create_window(self):
        '''
        Creates Home Control Interface.
        '''
        self.Home_Interface = Tk()
        self.uptime = tk.StringVar()
        self.cpu_util = tk.StringVar()
        self.cpu_util.set('Checking')
        self.virt_mem = tk.StringVar()
        self.virt_mem.set('Checking')
        self.pi_status = tk.StringVar()
        self.pi_status.set(self.rpi_status)
        window_height = 724
        window_width = 1108
        height = int((self.Home_Interface.winfo_screenheight()-window_height)/2)
        width = int((self.Home_Interface.winfo_screenwidth()-window_width)/2)
        self.Home_Interface.geometry(f'+{width}+{height}')
        # self.Home_Interface.geometry(f'{window_width}x{window_height}+{width}+{height}')
        self.Home_Interface.title(self.window_title)
        self.Home_Interface.iconbitmap(self.Home_Interface, self.icon)
        self.Home_Interface.configure(bg='white')
        self.Home_Interface.resizable(width=False, height=False)

        # default values for interface
        background = 'white'
        bold_base_font = ('Arial Bold', 20)
        small_bold_base_font = ('Arial Bold', 16)
        small_base_font = ('Arial', 15)
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
        ci_padx = 13
        self.ComputerInfo = Label(ComputerStatus, text='PC Uptime', bg=background, font=small_bold_base_font)
        self.ComputerInfo.grid(column=0, row=0, padx=ci_padx)
        self.ComputerInfo = Label(ComputerStatus, textvariable=self.uptime, bg=background, font=small_base_font)
        self.ComputerInfo.grid(column=0, row=1)

        self.ComputerInfo = Label(ComputerStatus, text='CPU Util', bg=background, font=small_bold_base_font)
        self.ComputerInfo.grid(column=1, row=0, padx=ci_padx)
        self.ComputerInfo = Label(ComputerStatus, textvariable=self.cpu_util, bg=background, font=small_base_font)
        self.ComputerInfo.grid(column=1, row=1)

        self.ComputerInfo = Label(ComputerStatus, text='Memory', bg=background, font=small_bold_base_font)
        self.ComputerInfo.grid(column=2, row=0, padx=ci_padx)
        self.ComputerInfo = Label(ComputerStatus, textvariable=self.virt_mem, bg=background, font=small_base_font)
        self.ComputerInfo.grid(column=2, row=1)

        self.ComputerInfo = Label(ComputerStatus, text='Rasberry Pi', bg=background, font=small_bold_base_font)
        self.ComputerInfo.grid(column=3, row=0, padx=ci_padx)
        self.ComputerInfo = Label(ComputerStatus, textvariable=self.pi_status, bg=background, font=small_base_font)
        self.ComputerInfo.grid(column=3, row=1)

        # Buttons
        LightsOn = Button(HueLightControlFrame, text="Lights On",
            command=lambda: self.Lights.on(), font=("Arial", 19), width=15)
        LightsOn.grid(column=0, row=1, padx=pad_x, pady=pad_y)

        TurnAllOff = Button(HueLightControlFrame, text="Lights Off",
            command=lambda: self.Lights.off(), font=("Arial", 19), width=15)
        TurnAllOff.grid(column=1, row=1, padx=pad_x, pady=pad_y)

        BackLight = Button(HueLightControlFrame, text="BackLight Mode",
            command=lambda: self.Lights.set_scene('Backlight'), font=("Arial", 19), width=15)
        BackLight.grid(column=0, row=2, padx=pad_x, pady=pad_y)

        DimmedMode = Button(HueLightControlFrame, text="Dimmed Mode",
            command=lambda: self.Lights.set_scene('Dimmed'), font=("Arial", 19), width=15)
        DimmedMode.grid(column=1, row=2, padx=pad_x, pady=pad_y)

        Nightlight = Button(HueLightControlFrame, text="Night Light",
            command=lambda: self.Lights.set_scene('Night light'), font=("Arial", 19), width=15)
        Nightlight.grid(column=0, row=3, padx=pad_x, pady=pad_y)

        self.HeaterButton = Button(SmartPlugControlFrame, text="Heater Toggle", font=("Arial", 19), width=15,
            command=lambda: self.smart_plug_toggle(name='Heater', device=self.Heater, button=self.HeaterButton),
            state='disabled')
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

        StartVRButton = Button(VRFrame, text="Start VR",
            command=self.start_vr, font=("Arial", 19), width=15)
        StartVRButton.grid(column=0, row=9, padx=pad_x, pady=pad_y)

        self.LighthouseButton = Button(VRFrame, text="Lighthouse Toggle", state='disabled', font=("Arial", 19),
            command=lambda: self.smart_plug_toggle(name='Lighthouse', device=self.Lighthouse,
            button=self.LighthouseButton), width=15)
        self.LighthouseButton.grid(column=1, row=9, padx=pad_x, pady=pad_y)

        SwitchToPCMode = Button(ProjectionFrame, text="PC Mode", command=lambda: self.display_switch('PC'),
            font=("Arial", 19), width=15)
        SwitchToPCMode.grid(column=0, row=9, padx=pad_x, pady=pad_y)

        SwitchToTVMode = Button(ProjectionFrame, text="TV Mode", command=lambda: self.display_switch('SONY TV'),
            font=("Arial", 19), width=15)
        SwitchToTVMode.grid(column=1, row=9, padx=pad_x, pady=pad_y)

        # computer specific setup
        current_pc = socket.gethostname()
        if current_pc == 'Aperture-Two':
            AudioToSpeakers = Button(AudioSettingsFrame, text="Speaker Audio",
                command=lambda: self.set_sound_device('Logitech Speakers'), font=("Arial", 19), width=15)
            AudioToSpeakers.grid(column=0, row=7, padx=pad_x, pady=pad_y)

            AudioToHeadphones = Button(AudioSettingsFrame, text="Headphone Audio",
                command=lambda: self.set_sound_device('Headphones'), font=("Arial", 19),width=15)
            AudioToHeadphones.grid(column=1, row=7, padx=pad_x, pady=pad_y)
        else:
            AudioToSpeakers = Button(AudioSettingsFrame, text="Speaker Audio",
                command=lambda: self.set_sound_device('Speakers'), font=("Arial", 19), width=15)
            AudioToSpeakers.grid(column=0, row=7, padx=pad_x, pady=pad_y)

            AudioToHeadphones = Button(AudioSettingsFrame, text="Headphone Audio",
                command=lambda: self.set_sound_device('Aux'), font=("Arial", 19),width=15)
            AudioToHeadphones.grid(column=1, row=7, padx=pad_x, pady=pad_y)
            # disables buttons that dont work on laptop
            SwitchToPCMode.config(state='disabled')
            SwitchToTVMode.config(state='disabled')
            StartVRButton.config(state='disabled')

        #  Smart Plugs running through state check function.
        self.plug_state_check()
        self.check_computer_status()
        # self.update_tray()

        # TODO Fix incorrect height
        if self.debug:
            self.Home_Interface.update()
            print(self.Home_Interface.winfo_width())
            print(self.Home_Interface.winfo_height())

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
        pi_thread = threading.Thread(target=callback, daemon=True)
        pi_thread.start()


    def create_tray(self):
        '''
        Creates the system tray. Clicking the Lightbulb ones the interface and right clicking it shows quick
        lighting control options.
        '''
        # FIXME threading issue where tray does not work when interface is open
        # TODO open/close window when icon pressed
        print('Tray Created')
        while True:
            event = self.Tray.Read()
            if event == 'Exit':
                exit()
            elif event == 'Lights On':
                self.Lights.on()
            elif event == 'Lights Off':
                self.Lights.off()
            elif event == 'Backlight Scene':
                self.Lights.set_scene('Backlight')
            elif event == 'Heater Toggle':
                self.smart_plug_toggle(self.Heater)
            elif event == 'Set audio to Speaker':
                self.set_sound_device('Logitech Speakers')
            elif event == 'Set audio to Headphones':
                self.set_sound_device('Headphones')
            elif event == '__ACTIVATED__':
                self.create_window()


    def run(self):
        '''
        Runs main script functions.
        '''
        start = time.perf_counter()
        self.discover_smart_plugs()
        threading.Thread(target=self.check_pi).start()
        self.setup_tray()
        finish = time.perf_counter()
        elapsed = round(finish-start, 2)
        print(f'Startup Time: {elapsed} seconds')
        self.create_tray()


if __name__ == "__main__":
    Home().run()
