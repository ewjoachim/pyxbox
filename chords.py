import math
from time import time

from music import MusicManager, Note
from controller import XBoxController
from game import Game


class Chords(Game):
    """
    Playing chords
    """
    def prepare(self):
        self.controller = XBoxController()
        self.music = MusicManager("instrument.sf2")

        self.notes = []
        self.chords_notes = []

        self.last_pressed = None

        self.prev_angle = None
        self.prev_dist = False

        self.angle_to_note = [0, 2, 4, 5, 7, 9, 11, 12]

        self.chords = {"a":[4, 7, 12], "b":[3, 7, 12], "x":[5, 9, 12], "y":[5, 8, 12]}

        self.sharp = False
        self.flat = False

        def stop_all(notes_list):
            while True:
                try:
                    note = notes_list.pop()
                    note.off()
                except IndexError:
                    break

        def buttons_cb(button, pressed):
            if pressed:
                if self.last_pressed:
                    for chord_val in self.chords[button]:
                        self.chords_notes.append(self.music.note(midi_val=self.last_pressed.midi_number + chord_val).on())
            else:
                stop_all(self.chords_notes)

        def trigger_cb(trigger, value):
            if trigger == "lt":
                self.flat = value > 0.5
            else:
                self.sharp = value > 0.5

        def sticks_cb(stick, x, y):
            dist = math.sqrt(x * x + y * y) > 0.7
            angle = math.atan2(y, x)
            angle = int(math.floor(angle / (2 * math.pi) * 8 + 0.5) % 8)
            if dist and (not self.prev_dist or self.prev_angle != angle):
                note_val = self.angle_to_note[angle] + int(self.sharp) - int(self.flat)
                note = self.music.note(note_val).on()
                self.notes.append(note)
                self.last_pressed = note
            elif not dist and self.prev_dist:
                stop_all(self.notes)

            self.prev_dist = dist
            self.prev_angle = angle

        self.controller.add_callback("ls", sticks_cb)
        self.controller.add_callbacks(("lt", "rt"), trigger_cb)
        self.controller.add_callbacks(("a", "b", "x", "y"), buttons_cb)

    def loop(self):
        self.controller.loop()

    def cleanup(self):
        self.music.end()


def main():
    game = Chords()
    game.start()

if __name__ == '__main__':
    main()