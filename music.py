import time
import fluidsynth
from datetime import datetime


class Note(object):
    def __init__(self, music_manager, val, octave=3):
        self.music_manager = music_manager
        self.midi_number = 22 + (octave * 12) + val
        self.active = False

    def on(self):
        self.active = True
        self.music_manager.synth.noteon(0, self.midi_number, 30)
        return self

    def off(self):
        self.active = False
        self.music_manager.synth.noteoff(0, self.midi_number)
        return self

    def set(self, onoff):
        if onoff:
            self.on()
        else:
            self.off()

    def __enter__(self):
        self.on()

    def __exit__(self, exc_type, exc_value, traceback):
        self.off()


class MusicManager(object):
    def __init__(self):
        self.synth = fluidsynth.Synth(gain=50)
        self.synth.start()
        sfid = self.synth.sfload("instrument.sf2")
        self.synth.program_select(0, sfid, 0, 0)
        self.notes = []
    
    def note(self, *args, **kwargs):
        return Note(self, *args, **kwargs)

    def end():
        self.synth.delete()

