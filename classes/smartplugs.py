from pyHS100 import SmartPlug, Discover
import re

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
        print('Checking for active smart plugs:')
        found_plug = False
        pattern = "\d{1,3}.\d{1,3}\.\d{1,3}\.\d{1,3}"
        for dev in Discover.discover().values():
            ip = re.findall(pattern, str(dev))
            if len(ip) > 0:
                if 'heater' in str(dev).lower():
                    print('> Heater Found')
                    self.Heater = SmartPlug(ip[0])
                    self.heater_plugged_in = 1
                    found_plug = True
                if 'vr device' in str(dev).lower():
                    print('> Lighthouse Found')
                    self.Lighthouse = SmartPlug(ip[0])
                    self.lighthouse_plugged_in = 1
                    found_plug = True
        if found_plug is False:
            print('> None found')


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
