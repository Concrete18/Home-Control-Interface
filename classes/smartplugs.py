from pyHS100 import SmartPlug, Discover
from pathlib import Path
import re, json


class Smart_Plug:

    lighthouse_plugged_in = False
    heater_plugged_in = False


    def __init__(self):
        '''
        ph
        '''
        pass


    def discover(self):
        '''
        Finds all smart plugs on the network and turns on ones used within this script if its name shows up.
        '''

        # {
        #     "Settings":{
        #         "check_pi_status":1,
        #         "computer_status_interval":1,
        #         "debug":0
        #     },
        #     "IP_Addresses":{
        #         "hue_hub":"192.168.0.134",
        #         "rasp_pi":"192.168.0.115",
        #         "heater": "192.168.0.146",
        #         "lighthouse": "192.168.0.197"
        #     }
        # }


        print('Checking for active smart plugs:')
        found_plug = False
        with open('config.json') as json_file:
            data = json.load(json_file)
        pattern = "\d{1,3}.\d{1,3}\.\d{1,3}\.\d{1,3}"
        for dev in Discover.discover().values():
            ip = re.findall(pattern, str(dev))[0]
            if len(ip) > 0:
                if 'heater' in str(dev).lower():
                    print('> Heater Found')
                    self.Heater = SmartPlug(ip)
                    data['IP_Addresses']['heater'] = ip
                    self.heater_plugged_in = 1
                    found_plug = True
                if 'vr device' in str(dev).lower():
                    print('> Lighthouse Found')
                    self.Lighthouse = SmartPlug(ip)
                    data['IP_Addresses']['lighthouse'] = ip
                    self.lighthouse_plugged_in = 1
                    found_plug = True
        if found_plug is False:
            print('> None found')
        json_file = Path('config.json')
        json_file.touch(exist_ok=True)
        with open(json_file, 'r+') as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def toggle(device, name='device', button=0):
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

    @staticmethod
    def turn_off_plug(device, name='device', button=0):
        '''
        Smart Plug toggle function.
        '''
        try:
            if device.get_sysinfo()["relay_state"] == 1:
                device.turn_off()
        except Exception as error:
            print(f'Error toggling device\n{error}\n{name}')
