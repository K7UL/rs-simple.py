rs-simple.py

This displays current frequency information of an amateur radio on a
rasperry pi.

This is a python3 script that uses kivy as a screen manager.
It requires that kivy is installed, along with hamlib.
Both of these are on github.


This was written to run on a raspberry pi 3 with the 7 inch touch
screen.  It polls rigctrld once a second to get the current frequency
of the radio and displays it on the screen.  Some simple band info is
also displayed on a few bands.

This is a simplified version of a larger script that is being
developed.


73