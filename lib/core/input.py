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
    signal_key_press = signal( 'InputHandler.KeyPress' )
    _state = {}

    def update( self, alcd ):
        for key in InputKeys:            
            if alcd.is_pressed( key.value ):
                self._key_press( key )
            else:
                self._key_up( key )

    def is_key_down( self, key ):
        return self._state.get( key.value, False )
 
    def _key_press( self, key ):
        if not self.is_key_down( key ):
            self._state[ key.value ] = True
            self.signal_key_press.send( key )
            #print( self._state )
    
    def _key_up( self, key ):
        if self.is_key_down( key ):
            self._state[ key.value ] = False
            #print( self._state )
