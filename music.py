import time
import fluidsynth
from datetime import datetime


class Note(object):
    """
    This is just a note. You can play it several times if you want so you can
    either create a note everytime you need one, or create just the ones you'll
    need in advance.

    Just call on() or off() to start or end. If you have a boolean you can call
    set(onoff) that will call on (True) or off (False)

    Finally, you can do things like that :

    >>> with Note(0), Note(4), Note(7):
    >>>     time.speel(1)

    It's just for fun, though.

    note_val 0 is for C, on octave 3. Each note_val up is a half-tone. You can have a note_val above
    12 or below zero, or use the octave parameter (or both)
    """
    def __init__(self, music_manager, note_val=0, octave=3, midi_val=None):
        self.music_manager = music_manager
        self.midi_number = (22 + (octave * 12) + note_val) if midi_val is None else midi_val
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
    """
    A wrapper for the FluidSynth synthetizer. Just input the intrument .sf2 filename.

    You can either use the note() method to get notes, or construct notes by giving them
    a reference to the MusicManager.
    """
    def __init__(self, instrument_filename, gain=50):
        self.synth = fluidsynth.Synth(gain=gain)
        self.synth.start()
        sfid = self.synth.sfload(instrument_filename)
        self.synth.program_select(0, sfid, 0, 0)
        self.notes = []
    
    def note(self, *args, **kwargs):
        return Note(self, *args, **kwargs)

    def end(self):
        self.synth.delete()

