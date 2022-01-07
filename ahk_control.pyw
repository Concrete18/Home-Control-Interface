from pyHS100 import SmartPlug
import sys, json, os
from playsound import playsound
from pathlib import Path
# classes
from classes.lights import Lights
from classes.computer import Computer

class Hotkey:

    script_dir = os.path.dirname(os.path.abspath(__file__))

    # config loader
    with open('config.json') as json_file:
        data = json.load(json_file)
    debug = data['Settings']['debug']
    # classes init
    lights = Lights()
    computer = Computer()

    # special plug setup for quick use
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
    hotkey = Hotkey()
    hotkey.run_command()
