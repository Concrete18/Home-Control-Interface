from pyHS100 import SmartPlug
from playsound import playsound
from pathlib import Path
import sys, json, os, subprocess

# classes
from classes.lights import Lights
from classes.smartplugs import Smart_Plug
from classes.computer import Computer
from classes.helper import Helper, benchmark


class Hotkey(Helper):
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # config loader
    with open("config.json") as json_file:
        data = json.load(json_file)

    def on_sound(self):
        """
        ph
        """
        playsound(r"Audio/upward.mp3")

    @staticmethod
    def off_sound():
        """
        ph
        """
        playsound(r"Audio/downward.mp3")

    def hotkey_activation_action(self, action_type):
        """
        ph
        """
        # TODO add notification
        # self.tray.ShowMessage(self.title, info, time=self.notif_dur * 1000)
        if action_type:
            pass
            # self.on_sound()
        else:
            pass
            # self.off_sound()

    def setup_plugs(self):
        # special plug setup for quick use
        json_file = Path("config.json")
        with open(json_file, "r") as f:
            data = json.load(f)
            # heater
            heater_ip = data["IP_Addresses"]["heater"]
            if heater_ip:
                self.heater = SmartPlug(heater_ip)
            else:
                playsound("Audio/Heater_not_found.wav")
                self.heater = False
            # vr
            lighthouse_ip = data["IP_Addresses"]["lighthouse"]
            if lighthouse_ip:
                self.lighthouse = SmartPlug(lighthouse_ip)
            else:
                self.lighthouse = False
        plugs = [self.lighthouse, self.heater]
        return any(plugs)

    def toggle_plug(self, device, first_run=True):
        """
        Smart Plug toggle function.
        """
        try:
            if device.get_sysinfo()["relay_state"] == 0:
                device.turn_on()
                self.hotkey_activation_action(True)
            else:
                device.turn_off()
                self.hotkey_activation_action(False)
            return True
        except Exception as error:
            print(f"Error toggling device\n{error}")
            self.warning_sound()
            if first_run:
                plug = Smart_Plug()
                plug.discover()
                return False

    @benchmark
    def run_command(self, command=None, first_run=True):
        """
        Runs given `command`.
        """
        # determines what the command is
        if len(sys.argv) > 1:
            command = sys.argv[1].lower()
        elif command is not None:
            print(f"Running {command} command.")
        else:
            print("No args.")
            return

        # light check
        if command in ["toggle_lights", "backlight", "moody", "light_fix"]:
            self.lights = Lights()
            if command == "toggle_lights":
                if self.lights.toggle_lights(all_lights=True):
                    self.hotkey_activation_action(True)
                else:
                    self.hotkey_activation_action(False)
            elif command == "backlight":
                self.lights.set_scene("Backlight")
                self.hotkey_activation_action(True)
            elif command == "moody":
                self.lights.set_scene("Moody")
                self.hotkey_activation_action(True)
            elif command == "light_fix":
                self.lights.set_scene("Blink Fix")
                self.hotkey_activation_action(True)

        # VR
        if command == "vr":
            return
            if not self.setup_plugs():
                return
            self.toggle_plug(self.lighthouse)
            # start steam VR
            steamvr_shortcut = Path(
                "C:/Program Files (x86)/Steam/steamapps/common/SteamVR/bin/win64/vrstartup.exe"
            )
            if steamvr_shortcut.is_file():
                print("yay it works")
                # subprocess.call(steamvr_shortcut.name)

        # plug check
        elif command in ["toggle_heater", "toggle_lighthouse"]:
            if not self.setup_plugs():
                return
            if command == "toggle_heater":
                success = self.toggle_plug(self.heater)
                # rerun if failed and it is the first run
                if not success and first_run:
                    self.run_command(command, first_run=False)

        # other
        elif "pc" in command:
            self.computer = Computer()
            if command == "pc_main":
                self.computer.display_switch("PC Main")
                self.hotkey_activation_action(True)
            elif command == "pc_extend":
                self.computer.display_switch("PC Extend")
                self.hotkey_activation_action(False)
            elif command == "pc_secondary":
                self.computer.display_switch("PC Secondary")
                self.hotkey_activation_action(False)


if __name__ == "__main__":
    hotkey = Hotkey()
    # hotkey.run_command("vr")
    hotkey.run_command("Backlight")
    # hotkey.run_command("pc_extend")
