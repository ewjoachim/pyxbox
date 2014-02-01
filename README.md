pyXBox - Ocarina
================

This is just a Proof of Concept for playing some music with a controller.
The code is split in several part to help extendablity for more complex interaction.

The Sample allows playing an ocarina with the same buttons as Zelda Ocarina of Time had
(right stick, xa, b, x, y). It shows both how to use the buttons and the analog sticks, 
plus how to make a note and to stop it.

I'm aiming at trying to find the right correspondances between the pad and the notes
to allow fiddling with music in a fun and easy way.

Dependencies
------------

 * [FluidSynth][1] (apt(itude) / brew / whatever)
 * [PyFluidSynth][2] (pip)
 * [Pygame][3] (pip)

Python dependecies are in `requirements.txt` you're welcome to try to do

    pip install -r requirements.txt

(untested, though). 

You will also need an instrument (sf2 file).
I personnaly used [this][0] one ([license][4])

How to run
----------

    python game.py

With an xbox controller plugged (for osx, I'm using [this][5] driver).
Buttons are left stick, x, y, b, a.

I remember Zelda had a lot of modifiers when playing the ocarina (sharp/flat, ...)
I'm planning to add a few things, but this is just a proof of concept.

Additionnaly, I'll try to make a new interaction not based on 1 button = 1 note. I 
have a few ideas on the subjet, but suggestions are welcome.

Disclamer
---------

This is my first project hosted on GitHub. I may have forgotten to include a few things.
Please ask !

Contact
-------

[@Ewjoachim][6]

License
-------

WTFPL (see LICENCE file).


[0]: http://zenvoid.org/audio/acoustic_grand_piano_ydp_20080910.sf2
[1]: http://sourceforge.net/apps/trac/fluidsynth/
[2]: https://code.google.com/p/pyfluidsynth/
[3]: http://www.pygame.org/
[4]: http://zenvoid.org/audio/acoustic_grand_piano_ydp_20080910.txt
[5]: http://tattiebogle.net/index.php/ProjectRoot/Xbox360Controller/OsxDriver
[6]: https://twitter.com/Ewjoachim