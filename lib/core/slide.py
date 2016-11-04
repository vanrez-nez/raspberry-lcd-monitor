from datetime import datetime

class Slide( object ):

    _DEFAULT_UPDATE_SEC = 2

    def __init__( self, name ):
        self._update_freq = self._DEFAULT_UPDATE_SEC
        self._name = name
        self._active = False
        self._reset()

    def get_dt( self ):
        return ( datetime.now() - self._last_update ).total_seconds()

    def _reset( self ):
        self._back_buffer = ''
        self._front_buffer = ''
        self._last_update = datetime.now()
        self._buffer_dirty = True
        self._clear_dirty = True

    def activate( self ):
        self._active = True
        self._reset()
        self._update_buffer()
        print( 'Activating Slide %s' % self._name )
    
    def deactivate( self ):
        self._active = False
        print( 'Deactivating Slide %s' % self._name )

    def _get_buffer( self ):
        return ''

    def _pad( self, buff ):
        lines = buff.split( '\n' )
        return '\n'.join( [ s.ljust( 16 ) for s in lines ] )

    def _get_buff_diff( self ):
        diff = []
        col = 0
        row = 0
        fb = self._pad( self._front_buffer )
        bb = self._pad( self._back_buffer )

        for idx, char in enumerate( bb ):
            if char == '\n':
                col = 0
                row += 1
            else:
                if len( fb ) - 1 < idx or char != fb[ idx ]:
                    diff.append( (col, row, char ) )
                col += 1
        
        return diff

    def _swap_buffer( self, alcd ):
        # print('swaping buffers', self._back_buffer, self._front_buffer)
        buff_diff = self._get_buff_diff()
        # print('diff', buff_diff )
        if len( buff_diff ) > 5:
            # heavy buffer
            alcd.set_cursor( 0, 0 )
            alcd.message( self._pad( self._back_buffer ) )
        else:
            # light buffer
            self._write_chars( alcd, buff_diff )
        self._front_buffer = self._back_buffer 
    
    def _write_chars( self, alcd, diff_chars ):
        for char in diff_chars:
            alcd.set_cursor( char[0], char[1] )
            alcd.write8( ord( char[2] ), True )

    def _update_buffer( self ):
        new_buffer = self._get_buffer()
        self._buffer_dirty = new_buffer != self._back_buffer
        self._back_buffer = new_buffer

    def update( self, alcd ):

        if self.get_dt() > self._update_freq:
            self._update_buffer()

        if self._clear_dirty:
            self._clear_dirty = False
            alcd.clear()

        if self._buffer_dirty:
            #print('Updating')
            self._swap_buffer( alcd )
            self._buffer_dirty = False
            self._last_update = datetime.now()
