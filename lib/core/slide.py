from datetime import datetime

class Slide( object ):

    _REFRESH_MS = 500

    def __init__( self, name ):
        self._buffer = ''
        self._name = name
        self._dirty = False
        self._last_update = datetime.now()

    def get_dt( self ):
        seconds = ( datetime.now() - self._last_update ).total_seconds()
        return seconds * 1000

    def activate( self ):
        self._dirty = True
        self._last_update = datetime.now()
        print( 'Activating Slide %s' % self._name )
    
    def deactivate( self ):
        print( 'Deactivating Slide %s' % self._name )

    def _get_buffer( self ):
        return ''
    
    def update( self, alcd ):

        if self.get_dt() > self._REFRESH_MS:
            new_buffer = self._get_buffer()
            self._dirty = new_buffer != self._buffer
            self._buffer = new_buffer

        if self._dirty:
            print('Updating')
            alcd.clear()
            alcd.message( self._buffer )
            self._dirty = False
            self._last_update = datetime.now()
