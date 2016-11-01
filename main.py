#!usr/bin/python
import time
from Adafruit_CharLCD import Adafruit_CharLCDPlate as ALCD

from lib.core.input import InputHandler
from lib.core.input import InputKeys
from lib.core.screen_director import ScreenDirector
from lib.screens.torrent.torrent import TorrentScreen
from lib.screens.system.system import SystemScreen

lcd = ALCD()
inputHandler = InputHandler()
director = ScreenDirector()
director.addScreen( SystemScreen() )
director.addScreen( TorrentScreen() )

def navigate( key ):
    if key == InputKeys.Up:
        director.getCurrentScreen().nextSlide()
    elif key == InputKeys.Down:
        director.getCurrentScreen().prevSlide()
    elif key == InputKeys.Right:
        director.nextScreen()
    elif key == InputKeys.Left:
        director.prevScreen()

inputHandler.signalKeyPress.connect( navigate )

while True:
    inputHandler.update( alcd = lcd )

