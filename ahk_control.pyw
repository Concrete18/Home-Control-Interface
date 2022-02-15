from pyHS100 import SmartPlug
from playsound import playsound
from pathlib import Path
import sys, json, os
# classes
from classes.lights import Lights
from classes.computer import Computer


class Hotkey:


    script_dir = os.path.dirname(os.path.abspath(__file__))

    # config loader
    with open('config.json') as json_file:
        data = json.load(json_file)
    debug = data['Settings']['debug']

    def setup_plugs(self):
        # special plug setup for quick use
        json_file = Path('config.json')
        with open(json_file, 'r') as f:
            data = json.load(f)
            heater_ip = data['IP_Addresses']['heater']
            lighthouse_ip = data['IP_Addresses']['lighthouse']
            if heater_ip:
                self.heater = SmartPlug(heater_ip)
            else:
                playsound('Audio/Heater_not_found.wav')
                self.heater = False
            if lighthouse_ip:
                self.lighthouse = SmartPlug(lighthouse_ip)
            else:
                self.lighthouse = False
        plugs = [self.lighthouse, self.heater]
        return any(plugs)

    def toggle_plug(self, device):
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
                

    def run_command(self, command=None):
        '''
        Runs given `command`.
        '''
        # determines what the command is
        if command is not None:
            print('Running test command.')
        elif len(sys.argv) > 1:
            command = sys.argv[1]
        else:
            print('No args.')
            return
        # command activation
        light_commands = [
            'toggle_lights',
            'backlight',
            'toggle_lights',
            'toggle_lights',
        ]
        plug_commands = [
            'toggle_heater',
            'toggle_lighthouse'
        ]
        # light check
        if command in light_commands:
            self.lights = Lights()
            if command == 'toggle_lights':
                self.lights.toggle_lights(all=True)
            elif command == 'backlight':
                self.lights.set_scene('Backlight')
        # plug check
        elif command in plug_commands:
            if not self.setup_plugs():
                return
            if command == 'toggle_heater':
                self.toggle_plug(self.heater)
        else:
            self.computer = Computer()
            if command == 'switch_to_pc':
                self.computer.display_switch('PC', self.script_dir)
            elif command == 'switch_to_tv':
                self.computer.display_switch('TV', self.script_dir)


if __name__ == "__main__":
    hotkey = Hotkey()
    hotkey.run_command('toggle_heater')
    # hotkey.run_command('toggle_lights')
