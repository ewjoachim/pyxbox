import math

from music import MusicManager, Note
from controller import XBoxController
from game import Game


class Ocarina(Game):
    """
    Just play the ocarina (Zelda OoT) with the controller
    """
    def prepare(self):
        self.controller = XBoxController()
        self.music = MusicManager("instrument.sf2")
        self.notes = {
            "rs": self.music.note(4),
            "a": self.music.note(7), 
            "b": self.music.note(11), 
            "x": self.music.note(13),
            "y": self.music.note(16),
        }

        def buttons_cb(button, pressed):
            self.notes[button].set(pressed)

        def analog_cb(stick, x, y):
            note = self.notes[stick]
            stick_on = math.sqrt(x * x + y * y) > 0.2
            if note.active != stick_on:
                note.set(stick_on)

        self.controller.add_callbacks(
            ["x", "y", "a", "b"], buttons_cb)
        self.controller.add_callback("rs", analog_cb)

    def loop(self):
        self.controller.loop()

    def cleanup(self):
        self.music.end()


def main():
    game = Ocarina()
    game.start()

if __name__ == '__main__':
    main()