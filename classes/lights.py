from phue import Bridge
import json, sys

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

    def toggle_lights(self, mode='any'):
        '''
        Turns on all lights if they are all off or turns lights off if any are on.
        '''
        lights_on = 0
        for lights in self.hue_hub.lights:
            if self.hue_hub.get_light(lights.name, 'on'):
                if mode == 'all':
                    lights_on += 1
                else:
                    self.off()
                    return
        if lights_on == len(self.hue_hub.lights):
            self.off()
        else:
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
            self.toggle_lights(mode='any')
        elif type == 'on':
            self.on()
        elif type == 'off':
            self.off()


if __name__ == "__main__":
    Lights().toggle_lights()
