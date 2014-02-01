import pygame

class XBoxController(object):

    buttons = [
        "up", "down", "left", "right", "start", "select",
        "lc", "rc", "lb", "rb", "guide", "a", "b", "x", "y"
    ]
    analog = ["lsx", "lsy", "rsx", "rsy", "lt", "rt"]

    def __init__(self):
        pygame.joystick.init()
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
        self.num_buttons = self.joystick.get_numbuttons()
        self.num_axis = self.joystick.get_numaxes()
        self.state = self.current_state()
        self.callbacks = {}

    def current_state(self):
        state = {"buttons": {}, "analog": {}}
        for i in range(self.num_buttons):
            state["buttons"][self.buttons[i]] = self.joystick.get_button(i) == 1
        for i in range(self.num_axis):
            state["analog"][self.analog[i]] = self.joystick.get_axis(i)
        return state

    def add_callback(self, name, cb):
        self.callbacks.setdefault(name, []).append(cb)

    def add_callbacks(self, names, cb):
        for name in names:
            self.add_callback(name, cb)

    def remove_cb(self, name, cb):
        self.callbacks.get(name, []).remove(cb)

    def call_callbacks(self, old, new):
        old_buttons, new_buttons = old["buttons"], new["buttons"]
        if old_buttons.keys() != new_buttons.keys():
            raise ValueError("different keys")
        for key in old_buttons.keys():
            old_val = old_buttons[key]
            new_val = new_buttons[key]
            if old_val != new_val:
                pressed = new_val
                cb_key = "{}_{}".format(key, "prs" if pressed else "rel")
                if cb_key in self.callbacks:
                    for cb in self.callbacks[cb_key]:
                        cb(key, pressed)

        for stick in ["ls", "rs"]:
            if stick in self.callbacks:
                for cb in self.callbacks[stick]:
                    cb(stick, new["analog"][stick + "x"], new["analog"][stick + "y"])
        for trigger in ["lt", "rt"]:
            if trigger in self.callbacks:
                for cb in self.callbacks[trigger]:
                    cb(trigger, new["analog"][trigger])

    def loop(self):
        new_state = self.current_state()
        self.call_callbacks(self.state, new_state)
        self.state = new_state