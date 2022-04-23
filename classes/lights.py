from phue import Bridge
import json, sys


class Lights:

    with open("config.json") as json_file:
        data = json.load(json_file)
    hue_hub = Bridge(data["IP_Addresses"]["hue_hub"])

    def get_light_state(self, light_name):
        """
        Returns a dict with the most useful light state data or False if the light was unreachable.
        """
        data = self.hue_hub.get_light(light_name)
        bulb_state = {
            "on": data["state"]["on"],
            "hue": data["state"]["hue"],
            "saturation": data["state"]["sat"],
            "brightness": data["state"]["bri"],
            "reachable": data["state"]["reachable"],
            "type": data["type"],
        }
        if not bulb_state["reachable"]:
            return False
        return bulb_state

    def on(self):
        """
        Sets all lights to on.
        """
        print("Turning Lights on.")
        self.hue_hub.run_scene("My Bedroom", "Normal", 1)

    def off(self):
        """
        Sets all lights to off.
        """
        print("Turning Lights off.")
        self.hue_hub.set_group("My Bedroom", "on", False)

    def set_scene(self, scene):
        """
        Sets the Hue lights to the entered scene.
        """
        print(f"Setting lights to {scene}.")
        self.hue_hub.run_scene("My Bedroom", scene, 1)

    def toggle_lights(self, all=True):
        """
        Turns on all lights if they are all off or turns lights off if any are on.
        """
        lights_on = 0
        total_lights = 0
        for lights in self.hue_hub.lights:
            total_lights += 1
            bulb = self.get_light_state(lights.name)
            if not bulb:
                return False
            if bulb["on"] and bulb["hue"] > 100:
                if all:
                    lights_on += 1
                else:
                    self.off()
                    return
        if lights_on == total_lights:
            self.off()
            return False
        else:
            self.on()
            return True

    def run(self):
        """
        Runs in CLI mode.
        """
        try:
            type = sys.argv[1].lower()
        except IndexError:
            type = "toggle"
        if type == "toggle":
            self.toggle_lights(mode="any")
        elif type == "on":
            self.on()
        elif type == "off":
            self.off()


if __name__ == "__main__":
    Lights().toggle_lights()
