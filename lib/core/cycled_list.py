from itertools import cycle

class CycledList:
    
    def __init__( self ):
        self._list = []
        self._curr = 0

    def current( self ):
        return self._curr if self._curr != None else None
 
    def _step( self, s ):
        idx = self._list.index( self._curr )
        next_idx = ( idx + s ) % len( self._list )
        return self._list[ next_idx ]

    def peek_next( self ):
        return self._step( 1 )

    def peek_prev( self ):
        return self._step( -1 )

    def next( self ):
        self._curr = self._step( 1 )
        return self.current()

    def prev( self ):
        self._curr = self._step( -1 )
        return self.current()

    def insert( self, item ):
        
        if self._list.count( item ) > 0:
            self._list.remove( item )
        
        self._list.insert( 0, item )
        
        if not self._curr:
            self._curr = item
    
    def get_list( self ):
        return self._list[:]
