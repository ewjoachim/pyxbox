import pygame

class XBoxController(object):
    """
    This manages callback on the 1st XBox 360 controller plugged.
    After the constructor, ensure the loop method is regularly called.
    It will call the callbacks you registered.

    Callbacks : 
        You can register to one or mor event by calling add_callback[s]
    """
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
        self.state = self._current_state()
        self.callbacks = {}

    def add_callback(self, event, cb):
        """
        Register the given callback so that it's called when the
        corresponding event occurs

        Buttons : 
            * Buttons event are the name of the button followed by _prs or _rel
              (for respectively the pressed or released event), or just the name
              of the button, that will be fired on both cases
            * Button names are up, down, left, right, x, y, b, a rc, lc,
              start, select and guide (the button between start and select)
            * Button callbacks should have this signature :
              callback(event_name [string], pressed [bool]) (positionnal args)
              (the arguments are useful if you assign several buttons and several
              states to a same callback, but you might as well ignore them in some
              cases)

        Analog inputs :
            * There are 4 analog inputs : the 2 sticks (ls, rs), that both have 2
              axis, and the 2 triggers (rt, lt). The name of the callback is
              the name of the input.
            * The callback is called at every frame with the analog value. You're
              responsible (for now) for interpreting the value.
            * The sticks callback signature are : 
              callback(event_name [string], x_val [-1 < float < 1], y_val [idem])
              1, 1 is upper right. 0, 0 is the center. The distance from the center
              is simply math.sqrt(x * x + y * y) and the angle is math.atan2(y, x)
            * The triggers callbacks signatures are
              callback(event_name [string], value [0 < float < 1])

        """
        self.callbacks.setdefault(event, []).append(cb)

    def add_callbacks(self, events, cb):
        """
        Add a same callback function for several event names. see add_callback.
        """
        for event in events:
            self.add_callback(event, cb)

    def remove_cb(self, event, cb, fail=False):
        """
        Remove a given callback from a given event name. Fails silently if callback is not
        present, except if fail=True
        """
        try:
            self.callbacks.get(event, []).remove(cb)
        except ValueError:
            if fail:
                raise ValueError("Callback {} not present in event {} callbacks".format(cb.__name__, event))

    def _current_state(self):
        state = {"buttons": {}, "analog": {}}
        for i in range(self.num_buttons):
            state["buttons"][self.buttons[i]] = self.joystick.get_button(i) == 1
        for i in range(self.num_axis):
            state["analog"][self.analog[i]] = self.joystick.get_axis(i)
        return state

    def _call_callback(self, event, *kwargs):
        for cb in self.callbacks.get(event, []):
            cb(event, *kwargs)

    def _call_callbacks(self, old, new):
        old_buttons, new_buttons = old["buttons"], new["buttons"]
        if old_buttons.keys() != new_buttons.keys():
            raise ValueError("different keys")
        for key in old_buttons.keys():
            old_val = old_buttons[key]
            new_val = new_buttons[key]
            if old_val != new_val:
                pressed = new_val
                event = "{}_{}".format(key, "prs" if pressed else "rel")
                self._call_callback(event, pressed)
                self._call_callback(key, pressed)
                

        for stick in ["ls", "rs"]:
            self._call_callback(stick, new["analog"][stick + "x"], new["analog"][stick + "y"])
        for trigger in ["lt", "rt"]:
            self._call_callback(trigger, new["analog"][trigger])

    def loop(self):
        new_state = self._current_state()
        self._call_callbacks(self.state, new_state)
        self.state = new_state