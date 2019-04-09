# rs-simple.py
# radio stuff - simple
# This is a stripped down version of python3 script that uses kivy that gets basic
# current radio settings from rigctld that is running on a computer on the LAN
# This is currently running on a raspberry pi 3 with the 7 inch touch screen
# rigctrld is also running on the same pi...but can be anywhere on the local network
# Ver 1.0
# K7UL@arrl.net

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock

import time
import socket


# set to IP address of computer that is running rigctrld
# rigctrld default port is 4532

IP = '127.0.0.1'
PORT = 4532



class BasicClock(ButtonBehavior, Label):
    def update(self, *args):
        self.text = time.asctime()
    def on_press(self):
        pass 

# network communication with rigctrld to radio
class RadioFreq(ButtonBehavior, Label):
    def on_press(self):
        pass
    def update(self, *args):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((IP, PORT))
        s.sendall('f')
        s.shutdown(socket.SHUT_WR)
        while 1:
            data = s.recv(1024)
            if data == "":
                break
            self.text = data
        s.close()
    def send(self, *args):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((IP, PORT))
        s.sendall(self.text)
        s.shutdown(socket.SHUT_WR)
        while 1:
            data = s.recv(1024)
            if data == "":
                break
        s.close()
        

# updates the band label
class BandInfo(ButtonBehavior, Label):
    def on_press(self):
        sm.current = '02'
    def update(self, *args):
        self.text = 'Out of band'
        if rf.text < 0:
            rf.text = 0
        x = int(rf.text)/10
        if x >= 13570 and x <= 13780:
            self.text = '2200 Meters'
        if x >= 47200 and x <= 47900:
            self.text = '630 Meters'
# cutting off some zeros now for my benefit 
# y is a lower detailed version of x
        y = x/1000
        if y >= 180 and y <= 200:
            self.text = '160 Meters'
        if y >= 350 and y <= 400:
            self.text = '80 Meters'
            if y < 360:
                self.text = '80 Meters CW'
        if x == 533200:
            self.text = '60 Meters Channel 1'
        if x == 534800:
            self.text = '60 Meters Channel 2'
        if x == 535850:
            self.text = '60 Meters Channel 3'
        if x == 537300:
            self.text = '60 Meters Channel 4'
        if x == 540500:
            self.text = '60 Meters Channel 5'
        if y >= 700 and y <= 730:
            self.text = '40 Meters'
            if x < 712500:
                self.text = '40 Meters CW'
        if y >= 1010 and y <= 1015:
            self.text = '30 Meters CW'
        if y >= 1400 and y <= 1435:
            self.text = '20 Meters Extra Class'
            if x < 1402500:
                self.text = '20 Meters CW Extra Class'
            if y < 1415:
                self.text = '20 Meters CW'
            if x > 1417500:
                self.text = '20 Meters Advanced Class'
            if x > 1425500:
                self.text = '20 Meters General Class'
        if x >= 1806800 and x <= 1816800:
            self.text = '17 Meters'
            if x < 1811000:
                self.text = '17 Meters CW'
        if y >= 2100 and y <= 2145:
            self.text = '15 Meters Extra Class'
            if y < 2120:
                self.text = '15 Meters CW'
            if x < 2102500:
                self.text = '15 CW Extra Class'
            if x >= 2122500:
                self.text = '15 Meters Advanced Class'
            if x >= 2127500:
                self.text = '15 Meters General Class'
        if y >= 2489 and y <= 2499:
            self.text = '12 Meters'
            if y < 2493:
                self.text = '12 Meters CW'
        if y >= 2800 and y <= 2970:
            self.text = '10 Meters Extra Class'
            if y < 2830:
                self.text = '10 Meters CW'
            if y >= 2830 and  y < 2850:
                self.text = '10 Meters Novice/Tech Voice'
        if y >= 5000 and y <= 5400:
            self.text = '6 Meters'
            if y < 5010:
                self.text = '6 Meters CW'
        if y >= 14400 and y <= 14800:
            self.text = '2 Meters'
            if y < 14410:
                self.text = '2 Meters CW'
        if y >= 21900 and y <= 22500:
            self.text = '1.25 Meters'
        if y >= 42000 and y <= 45000:
            self.text = '70 Centameters'
            
    



# The labels are set to act as buttons, here is the framework to add more
# fucntions to the existing labels
def callback(instance):
    print('button  <%s>' % instance.text)
    sm.current = '00'


# global declarations 

band = BandInfo(
                font_size='30sp',
                pos=(0,100))
rf = RadioFreq(
               font_size='120sp',
               pos=(0,120))
bc = BasicClock(font_size='30sp')
sm = ScreenManager()

# main program and screen creation
class Overall(App):
    def build(self):
        
        screen = Screen(name='00')
        layout = FloatLayout(size=(800,400))
        layout.add_widget(rf)
        layout.add_widget(band)
        layout.add_widget(bc)
        screen.add_widget(layout)
        sm.add_widget(screen)
        
# This is were the refresh rate is set....
# I leave this setting at 1 for 1 second but I have set it at .1 for a real fast update rate.
# Not sure how fast it will go on a raspberry pi 3

        Clock.schedule_interval(self.update, 1)
        return sm

# timer     
    def update(self, *args):
        bc.update()
        rf.update()
        band.update()


    
if __name__ == "__main__":
    Overall().run()
    
    