import time
from datetime import datetime
import Adafruit_CharLCD as LCD
from blinker import signal
from enum import Enum

# time before going idle if no buttons pushed 
IDLE_TIME_SEC = 4

# scan frequency to detect activity
IDLE_UPDATE_FREQ_SEC = 0.5

# scan frequency while active
ACTIVE_UPDATE_FREQ_SEC = 0.05

class InputKeys( Enum ):
    Select  = LCD.SELECT
    Left    = LCD.LEFT
    Right   = LCD.RIGHT
    Up      = LCD.UP
    Down    = LCD.DOWN

class InputHandler:
    signal_key_press = signal( 'InputHandler.KeyPress' )
    _state = {}
    _last_update = datetime.now()
    _last_key_update = datetime.now()
    _update_freq = IDLE_UPDATE_FREQ_SEC
    
    def _get_dt( self ):
        return ( datetime.now() - self._last_update ).total_seconds()

    def _get_dt_key( self ):
        return ( datetime.now() - self._last_key_update ).total_seconds()

    def update( self, alcd ):

        # if no key was pressed for more than IDLE time 
        if ( self._get_dt_key() > IDLE_TIME_SEC ):
            # set update freq to IDLE
            self._update_freq = IDLE_UPDATE_FREQ_SEC       

        # if time elapsed greater than update freq
        if ( self._get_dt() > self._update_freq ):
            self._last_update = datetime.now()
            for key in InputKeys:            
                if alcd.is_pressed( key.value ):
                    self._last_key_update = datetime.now()
                    self._update_freq = ACTIVE_UPDATE_FREQ_SEC
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
