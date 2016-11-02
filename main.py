#!usr/bin/python
import time
import atexit
from Adafruit_CharLCD import Adafruit_CharLCDPlate as ALCD

from lib.core.input import InputHandler
from lib.core.input import InputKeys
from lib.core.screen import Screen
from lib.core.screen_director import ScreenDirector
from lib.slides.torrent.jobs import TorrentJobs
from lib.slides.system.cpu import SystemCPU

lcd = ALCD()
input_handler = InputHandler()
director = ScreenDirector()

""" Add System Screen """
system_screen = Screen( color=[1.0, 0.0, 0.0] )
system_screen.add_slide( SystemCPU() )
director.add_screen( system_screen )

""" Add Torrent Screen """
torrent_screen = Screen( color=[1.0, 1.0, 0.0] )
torrent_screen.add_slide( TorrentJobs() )
director.add_screen( torrent_screen )

@atexit.register
def shutdown():
    print( "Shutting down" )
    lcd.set_backlight( 0 )

def navigate( key ):
    if key == InputKeys.Up:
        director.get_current_screen().next_slide()
    elif key == InputKeys.Down:
        director.get_current_screen().prev_slide()
    elif key == InputKeys.Right:
        director.next_screen()
    elif key == InputKeys.Left:
        director.prev_screen()

input_handler.signal_key_press.connect( navigate )

while True:
    input_handler.update( lcd )
    director.update( lcd )

