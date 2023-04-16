import phue
import json, sys


class Lights:

    with open("config.json") as json_file:
        data = json.load(json_file)
    hue_hub = phue.Bridge(data["IP_Addresses"]["hue_hub"])

    bedroom_lights = ["Left Lamp", "Monitor", "Right Lamp"]

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

    def intensity(self, room, intensity_percent):
        """
        Sets intensity for select room lights.
        """
        print(f"Setting intensity of {room} to {intensity_percent}.")
        # self.hue_hub.set_group("My Bedroom", "on", False)

    def set_scene(self, scene):
        """
        Sets the Hue lights to the entered scene.
        """
        print(f"Setting lights to {scene}.")
        self.hue_hub.run_scene("My Bedroom", scene, 1)

    def toggle_lights(self, all_lights=True):
        """
        Turns on all lights if they are all off or turns lights off if any are on.
        Ignores lights that are not currently powered on.
        """
        lights_on, total_lights = 0, 0
        for light in self.hue_hub.lights:
            if not (light_state := self.get_light_state(light.name)):
                continue
            total_lights += 1
            # skip powered off bulbs
            if not light_state:
                continue
            checklist = [
                light_state["on"],
                light_state["hue"] > 100,
                light.name in self.bedroom_lights,
            ]
            if all(checklist):
                if all_lights:
                    lights_on += 1
                else:
                    self.off()
                    return
        print(f"{lights_on} light(s) on of {total_lights}.")
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
