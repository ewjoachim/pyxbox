import math
from time import time

from music import MusicManager, Note
from controller import XBoxController
from game import Game


def continuous_angle(new, old):
    """
    Returns an angle not bound to 0 - 2 pi but guaranteed
    that, with respect to the previous value, there will be
    the smallest possible gap.
    """
    while True:
        if abs(new - old) < math.pi:
            return new
        new += 2 * math.pi  * (-1 if (new - old) > 0 else 1)


class MusicTip(Game):
    """
    Just play the ocarina (Zelda OoT) with the controller
    """
    def prepare(self):
        self.controller = XBoxController()
        self.music = MusicManager("instrument.sf2")

        self.notes = []

        self.prev_precise_angle = 0
        self.prev_angle = None
        self.prev_dist = False

        self.angle_to_note = [0, 2, 4, 5, 7, 9, 11]


        def buttons_cb(button, pressed):
            pass

        def analog_cb(stick, x, y):
            dist = math.sqrt(x * x + y * y) > 0.7
            precise_angle = continuous_angle(math.atan2(y, x), self.prev_precise_angle)
            angle = int(math.floor(precise_angle / (2 * math.pi) * 7 + 0.5))
            if dist and (not self.prev_dist or self.prev_angle != angle):
                note_val = self.angle_to_note[angle % 7]
                octave = int(angle // 7) + 4
                self.notes.append(self.music.note(note_val, octave).on())
            elif not dist and self.prev_dist:
                while True:
                    try:
                        note = self.notes.pop()
                        note.off()
                    except IndexError:
                        break

            self.prev_precise_angle = precise_angle
            self.prev_dist = dist
            self.prev_angle = angle

        self.controller.add_callback("ls", analog_cb)

    def loop(self):
        self.controller.loop()

    def cleanup(self):
        self.music.end()


def main():
    game = MusicTip()
    game.start()

if __name__ == '__main__':
    main()