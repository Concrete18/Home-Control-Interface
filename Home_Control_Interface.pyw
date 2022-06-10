from tkinter import Tk, Button, Label, LabelFrame, messagebox
import tkinter as tk
import psutil, time, os, socket, threading, subprocess, json
import PySimpleGUIWx as sg
from pathlib import Path
from classes.lights import Lights
from classes.computer import Computer
from classes.smartplugs import Smart_Plug


class Home:

    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    with open("config.json") as json_file:
        data = json.load(json_file)
    # settings
    debug = data["Settings"]["debug"]
    check_pi_status = data["Settings"]["check_pi_status"]
    # interval in seconds
    computer_status_interval = data["Settings"]["status_interval"]
    # defaults
    icon = "images/bulb.ico"
    window_title = "Home Control Interface"
    window_state = 0
    # classes init
    lights = Lights()
    computer = Computer()
    plug = Smart_Plug()
    # python scripts
    timed_shutdown = "D:/Google Drive/Coding/Python/Scripts/1-Complete-Projects/Timed-Shutdown/Timed_Shutdown.pyw"
    # Status vars
    rasp_pi = data["IP_Addresses"]["rasp_pi"]
    rpi_status = "Checking Status"
    boot_time = psutil.boot_time()

    def setup_tray(self):
        """
        Sets up tray object with options.
        """
        buttons = [
            "Lights On",
            "Lights Off",
            "Backlight Scene",
            "---",
            "Shutdown",
            "Set audio to Speaker",
            "Set audio to Headphones",
            "---",
        ]
        # togglable options
        if self.plug.lighthouse_plugged_in:
            buttons.append("Lighthouse Toggle")
        if self.plug.power_strip_plugged_in:
            buttons.append("Valve Index Toggle")
        if self.plug.heater_plugged_in:
            buttons.append("Heater Toggle")
        # adds the separator only if it is no already the last entry
        if buttons[len(buttons) - 1] != "---":
            buttons.append("---")
        # end of options
        buttons.append("Exit")
        # tray object creation
        self.Tray = sg.SystemTray(
            menu=["menu", buttons],
            filename=self.icon,
            tooltip=self.window_title,
        )
        print("\nTray Setup")

    def check_computer_status(self):
        """
        Gets and updates vars to computer stats.
        """
        mem = psutil.virtual_memory()
        gigs_used = round(mem.used / 1024 / 1024 / 1024, 1)
        gigs_total = round(mem.total / 1024 / 1024 / 1024, 1)
        virt_mem = f"{gigs_used}/{gigs_total}"
        seconds_since_boot = int(time.time() - self.boot_time)
        self.uptime.set(self.computer.readable_time_since(seconds_since_boot))
        self.cpu_util.set(f"{psutil.cpu_percent(interval=0.1)}%")
        self.virt_mem.set(f"{virt_mem} GB")
        self.Home_Interface.after(
            self.computer_status_interval * 1000, self.check_computer_status
        )

    def start_vr(self):
        """
        Runs SteamVR shortcut and turns on lighthouse plugged into smart plug for tracking if it is off.
        """
        self.lights.on()
        if (
            self.plug.lighthouse_plugged_in
            and self.plug.Lighthouse.get_sysinfo()["relay_state"] == 0
        ):
            self.plug.Lighthouse.turn_on()
            self.LighthouseButton.config(relief="sunken")
        steamvr_shortcut = Path(
            "D:/My Installed Games/Steam Games/steamapps/common/SteamVR/bin/win64/vrstartup.exe"
        )
        if steamvr_shortcut.isfile():
            subprocess.call(steamvr_shortcut.name)

    def create_window(self):
        """
        Creates Home Control Interface.
        """
        self.Home_Interface = Tk()
        self.uptime = tk.StringVar()
        self.cpu_util = tk.StringVar()
        self.cpu_util.set("Checking")
        self.virt_mem = tk.StringVar()
        self.virt_mem.set("Checking")
        self.pi_status = tk.StringVar()
        self.pi_status.set(self.computer.rpi_status)
        window_height = 724
        window_width = 1108
        height = int((self.Home_Interface.winfo_screenheight() - window_height) / 2)
        width = int((self.Home_Interface.winfo_screenwidth() - window_width) / 2)
        self.Home_Interface.geometry(f"+{width}+{height}")
        # self.Home_Interface.geometry(f'{window_width}x{window_height}+{width}+{height}')
        self.Home_Interface.title(self.window_title)
        self.Home_Interface.iconbitmap(self.Home_Interface, self.icon)
        self.Home_Interface.configure(bg="white")
        self.Home_Interface.resizable(width=False, height=False)

        # default values for interface
        background = "white"
        bold_base_font = ("Arial Bold", 20)
        small_bold_base_font = ("Arial Bold", 16)
        small_base_font = ("Arial", 15)
        pad_x = 10
        pad_y = 10

        # Frames
        # Left Frames
        ComputerStatus = LabelFrame(
            self.Home_Interface,
            text="Computer Status",
            bg=background,
            font=bold_base_font,
            padx=pad_x,
            pady=pad_y,
            width=300,
            height=150,
        )
        ComputerStatus.grid(column=0, row=0, padx=pad_x, pady=pad_y, sticky="nsew")

        HueLightControlFrame = LabelFrame(
            self.Home_Interface,
            text="Hue Light Control",
            bg=background,
            font=bold_base_font,
            padx=pad_x,
            pady=pad_y,
            width=300,
            height=400,
        )
        HueLightControlFrame.grid(
            column=0, row=1, rowspan=2, padx=pad_x, pady=pad_y, sticky="nsew"
        )

        Script_Shortcuts = LabelFrame(
            self.Home_Interface,
            text="Script Shortcuts",
            bg=background,
            font=bold_base_font,
            padx=pad_x,
            pady=pad_y,
            width=300,
            height=200,
        )
        Script_Shortcuts.grid(column=0, row=3, padx=pad_x, pady=pad_y, sticky="nsew")

        # Right Frames
        SmartPlugControlFrame = LabelFrame(
            self.Home_Interface,
            text="Smart Plug Control",
            bg=background,
            font=bold_base_font,
            padx=pad_x,
            pady=pad_y,
            width=300,
            height=150,
        )
        SmartPlugControlFrame.grid(
            column=1, row=0, padx=pad_x, pady=pad_y, sticky="nsew"
        )

        AudioSettingsFrame = LabelFrame(
            self.Home_Interface,
            text="Audio Settings",
            bg=background,
            font=bold_base_font,
            padx=pad_x,
            pady=pad_y,
            width=300,
            height=390,
        )
        AudioSettingsFrame.grid(column=1, row=1, padx=pad_x, pady=pad_y, sticky="nsew")

        ProjectionFrame = LabelFrame(
            self.Home_Interface,
            text="Projection",
            bg=background,
            font=bold_base_font,
            padx=pad_x,
            pady=pad_y,
            width=300,
            height=400,
        )
        ProjectionFrame.grid(column=1, row=2, padx=pad_x, pady=pad_y, sticky="nsew")

        VRFrame = LabelFrame(
            self.Home_Interface,
            text="VR Settings",
            bg=background,
            font=bold_base_font,
            padx=pad_x,
            pady=pad_y,
            width=300,
            height=400,
        )
        VRFrame.grid(column=1, row=3, padx=pad_x, pady=pad_x, sticky="nsew")

        # Labels
        ci_padx = 13
        self.ComputerInfo = Label(
            ComputerStatus, text="PC Uptime", bg=background, font=small_bold_base_font
        )
        self.ComputerInfo.grid(column=0, row=0, padx=ci_padx)
        self.ComputerInfo = Label(
            ComputerStatus,
            textvariable=self.uptime,
            bg=background,
            font=small_base_font,
        )
        self.ComputerInfo.grid(column=0, row=1)

        self.ComputerInfo = Label(
            ComputerStatus, text="CPU Util", bg=background, font=small_bold_base_font
        )
        self.ComputerInfo.grid(column=1, row=0, padx=ci_padx)
        self.ComputerInfo = Label(
            ComputerStatus,
            textvariable=self.cpu_util,
            bg=background,
            font=small_base_font,
        )
        self.ComputerInfo.grid(column=1, row=1)

        self.ComputerInfo = Label(
            ComputerStatus, text="Memory", bg=background, font=small_bold_base_font
        )
        self.ComputerInfo.grid(column=2, row=0, padx=ci_padx)
        self.ComputerInfo = Label(
            ComputerStatus,
            textvariable=self.virt_mem,
            bg=background,
            font=small_base_font,
        )
        self.ComputerInfo.grid(column=2, row=1)

        self.ComputerInfo = Label(
            ComputerStatus, text="Rasberry Pi", bg=background, font=small_bold_base_font
        )
        self.ComputerInfo.grid(column=3, row=0, padx=ci_padx)
        self.ComputerInfo = Label(
            ComputerStatus,
            textvariable=self.pi_status,
            bg=background,
            font=small_base_font,
        )
        self.ComputerInfo.grid(column=3, row=1)

        # Buttons
        LightsOn = Button(
            HueLightControlFrame,
            text="Lights On",
            command=lambda: self.lights.on(),
            font=("Arial", 19),
            width=15,
        )
        LightsOn.grid(column=0, row=1, padx=pad_x, pady=pad_y)

        TurnAllOff = Button(
            HueLightControlFrame,
            text="Lights Off",
            command=lambda: self.lights.off(),
            font=("Arial", 19),
            width=15,
        )
        TurnAllOff.grid(column=1, row=1, padx=pad_x, pady=pad_y)

        BackLight = Button(
            HueLightControlFrame,
            text="BackLight Mode",
            command=lambda: self.lights.set_scene("Backlight"),
            font=("Arial", 19),
            width=15,
        )
        BackLight.grid(column=0, row=2, padx=pad_x, pady=pad_y)

        DimmedMode = Button(
            HueLightControlFrame,
            text="Dimmed Mode",
            command=lambda: self.lights.set_scene("Dimmed"),
            font=("Arial", 19),
            width=15,
        )
        DimmedMode.grid(column=1, row=2, padx=pad_x, pady=pad_y)

        Nightlight = Button(
            HueLightControlFrame,
            text="Night Light",
            command=lambda: self.lights.set_scene("Night light"),
            font=("Arial", 19),
            width=15,
        )
        Nightlight.grid(column=0, row=3, padx=pad_x, pady=pad_y)

        self.HeaterButton = Button(
            SmartPlugControlFrame,
            text="Heater Toggle",
            font=("Arial", 19),
            width=15,
            command=lambda: self.plug.toggle(
                name="Heater", device=self.plug.Heater, button=self.HeaterButton
            ),
            state="disabled",
        )
        self.HeaterButton.grid(column=0, row=5, padx=pad_x, pady=pad_y)

        UnsetButton = Button(
            SmartPlugControlFrame,
            text="Unset",
            state="disabled",
            command="ph",
            font=("Arial", 19),
            width=15,
        )
        UnsetButton.grid(column=1, row=5, padx=pad_x, pady=pad_y)

        TimerControl = Button(
            Script_Shortcuts,
            text="Power Control",
            command=lambda: self.computer.python_script_runner(self.timed_shutdown),
            font=("Arial", 19),
            width=15,
        )
        TimerControl.grid(column=1, row=0, padx=pad_x, pady=pad_y)

        StartVRButton = Button(
            VRFrame,
            text="Start VR",
            command=self.start_vr,
            font=("Arial", 19),
            width=15,
        )
        StartVRButton.grid(column=0, row=9, padx=pad_x, pady=pad_y)

        self.LighthouseButton = Button(
            VRFrame,
            text="Lighthouse Toggle",
            state="disabled",
            font=("Arial", 19),
            command=lambda: self.plug.toggle(
                name="VR Device",
                device=self.plug.Lighthouse,
                button=self.LighthouseButton,
            ),
            width=15,
        )
        self.LighthouseButton.grid(column=1, row=9, padx=pad_x, pady=pad_y)

        SwitchToPCMode = Button(
            ProjectionFrame,
            text="PC Mode",
            font=("Arial", 19),
            width=15,
            command=lambda: self.computer.display_switch("PC"),
        )
        SwitchToPCMode.grid(column=0, row=9, padx=pad_x, pady=pad_y)

        SwitchToTVMode = Button(
            ProjectionFrame,
            text="TV Mode",
            font=("Arial", 19),
            width=15,
            command=lambda: self.computer.display_switch("TV", self.Home_Interface),
        )
        SwitchToTVMode.grid(column=1, row=9, padx=pad_x, pady=pad_y)

        # computer specific setup
        current_pc = socket.gethostname()
        if current_pc == "Aperture-Two":
            AudioToSpeakers = Button(
                AudioSettingsFrame,
                text="Speaker Audio",
                command=lambda: self.computer.set_sound_device("Logitech Speakers"),
                font=("Arial", 19),
                width=15,
            )
            AudioToSpeakers.grid(column=0, row=7, padx=pad_x, pady=pad_y)

            AudioToHeadphones = Button(
                AudioSettingsFrame,
                text="Headphone Audio",
                command=lambda: self.computer.set_sound_device("Headphones"),
                font=("Arial", 19),
                width=15,
            )
            AudioToHeadphones.grid(column=1, row=7, padx=pad_x, pady=pad_y)
        else:
            AudioToSpeakers = Button(
                AudioSettingsFrame,
                text="Speaker Audio",
                command=lambda: self.computer.set_sound_device("Speakers"),
                font=("Arial", 19),
                width=15,
            )
            AudioToSpeakers.grid(column=0, row=7, padx=pad_x, pady=pad_y)

            AudioToHeadphones = Button(
                AudioSettingsFrame,
                text="Headphone Audio",
                command=lambda: self.computer.set_sound_device("Aux"),
                font=("Arial", 19),
                width=15,
            )
            AudioToHeadphones.grid(column=1, row=7, padx=pad_x, pady=pad_y)
            # disables buttons that dont work on laptop
            SwitchToPCMode.config(state="disabled")
            SwitchToTVMode.config(state="disabled")
            StartVRButton.config(state="disabled")

        #  Smart Plugs running through state check function.
        self.plug_state_check()
        self.check_computer_status()

        # TODO Fix incorrect height
        if self.debug:
            self.Home_Interface.update()
            print(self.Home_Interface.winfo_width())
            print(self.Home_Interface.winfo_height())

        self.Home_Interface.mainloop()

    def plug_state_check(self):
        """
        Gets current state of entered device and updates button relief.
        """

        def callback():
            buttons = {}
            if self.plug.lighthouse_plugged_in:
                buttons[self.plug.Lighthouse] = self.LighthouseButton
                self.LighthouseButton.config(state="normal")
            if self.plug.heater_plugged_in:
                buttons[self.plug.Heater] = self.HeaterButton
                self.HeaterButton.config(state="normal")
            for device, button in buttons.items():
                try:
                    if device.get_sysinfo()["relay_state"] == 1:
                        button.config(relief="sunken")  # On State
                    else:
                        button.config(relief="raised")  # Off State
                except Exception as e:
                    print("Smart Plug", e)
                    messagebox.showwarning(
                        title=self.window_title,
                        message=f"Error communicating with {device}.",
                    )

        pi_thread = threading.Thread(target=callback, daemon=True)
        pi_thread.start()

    def create_tray(self):
        """
        Creates the system tray. Clicking the Lightbulb ones the interface and right clicking it shows quick
        lighting control options.
        """
        # FIXME threading issue where tray does not work when interface is open
        # TODO open/close window when icon pressed
        print("Tray Created\n")
        while True:
            event = self.Tray.Read()
            # general
            if event == "Exit":
                exit()
            elif event == "__ACTIVATED__":
                self.create_window()
            # lights
            elif event == "Lights On":
                self.lights.on()
            elif event == "Lights Off":
                self.lights.off()
            elif event == "Backlight Scene":
                self.lights.set_scene("Backlight")
            # computer
            elif event == "Shutdown":
                self.plug.turn_off_plug(self.plug.Lighthouse)
                self.computer.shutdown()
            elif event == "Set audio to Speaker":
                self.computer.set_sound_device("Logitech Speakers")
            elif event == "Set audio to Headphones":
                self.computer.set_sound_device("Headphones")
            # smart plugs
            elif event == "Lighthouse Toggle":
                self.plug.toggle(self.plug.Lighthouse)
                self.plug.toggle_strip("VR Device")
            elif event == "Valve Index Toggle":
                self.plug.toggle_strip("Valve Index")
            elif event == "Heater Toggle":
                self.plug.toggle(self.plug.Heater)

    def run(self):
        """
        Runs main script functions.
        """
        start = time.perf_counter()
        self.plug.discover()
        threading.Thread(target=self.computer.check_pi).start()
        self.setup_tray()
        finish = time.perf_counter()
        elapsed = round(finish - start, 2)
        print(f"Startup Time: {elapsed} seconds")
        self.create_tray()


if __name__ == "__main__":
    Home().run()
