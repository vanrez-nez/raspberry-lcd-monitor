import Adafruit_CharLCD as LCD
from blinker import signal
from enum import Enum

class InputKeys( Enum ):
    Select  = LCD.SELECT
    Left    = LCD.LEFT
    Right   = LCD.RIGHT
    Up      = LCD.UP
    Down    = LCD.DOWN

class InputHandler:
    signalKeyPress = signal( 'InputHandler.KeyPress' )
    _state = {}

    def update( self, alcd ):
        for key in InputKeys:            
            if alcd.is_pressed( key.value ):
                self._keyPress( key )
            else:
                self._keyUp( key )

    def isKeyDown( self, key ):
        return self._state.get( key.value, False )
 
    def _keyPress( self, key ):
        if not self.isKeyDown( key ):
            self._state[ key.value ] = True
            self.signalKeyPress.send( key )
            #print( self._state )
    
    def _keyUp( self, key ):
        if self.isKeyDown( key ):
            self._state[ key.value ] = False
            #print( self._state )
