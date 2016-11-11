from lib.core.cycled_list import CycledList
from lib.core.input import InputKeys

class ActionsMenu():

    def __init__( self, caption ):
        self._options = CycledList()
        self._selecting = False
        self._caption = caption
        self.add_option( 'BACK', self._on_back )

    def add_option( self, caption, cb ):
        self._options.insert( { 'caption': caption, 'cb': cb } )

    def _on_back( self ):
        self._selecting = False            

    def _next( self ):
        self._options.next()

    def _prev( self ):
        self._options.prev()

    def _select( self ):
        current = self._options.current()
        if current:
            if self._selecting:
                current[ 'cb' ]()
            else:
                self._selecting = True
                self._options.first()

    def navigate( self, key ):
        if key == InputKeys.Select:
            self._select()
        elif key == InputKeys.Right:
            self._next()
        elif key == InputKeys.Left:
            self._prev()

        return self._selecting

    def _get_ribbon( self ):
        curr = self._options.current()
        opts = self._options.get_list()
        selecting = self._selecting
        res = [ '\x07' if op == curr and selecting else '\x06' for op in opts ]
        return ''.join( res ).center( 16, " " )

    def get_buffer( self ):
       curr = self._options.current()
       title = curr[ 'caption' ] if curr and self._selecting else self._caption
       title = title.center( 16, " " ) 
       options_ribbon = self._get_ribbon()
       return "%s\n%s" % ( title, options_ribbon )

