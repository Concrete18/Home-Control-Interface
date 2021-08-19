from pyHS100 import SmartPlug, Discover
import re

# WIP started progress on Smart_Hub class. This is not in use yet
class Smart_Hub:


    def __init__(self, LighthouseButton, HeaterButton, window_title):
        self.LighthouseButton = LighthouseButton
        self.HeaterButton = HeaterButton
        self.window_title = window_title


    def discover_smart_plugs(self):
        '''
        Finds all smart plugs on the network and turns on ones used within this script if its name shows up.
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
                if 'vr device' in str(dev).lower():
                    print('> Lighthouse Found')
                    self.Lighthouse = SmartPlug(ip[0])
                    self.lighthouse_plugged_in = 1


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
