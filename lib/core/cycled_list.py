from itertools import cycle

class CycledList:
    
    def __init__( self ):
        self._list = []
        self._curr = None

    def current( self ):
        if self._curr != None and self._list.count( self._curr ) > 0:
            idx = self._list.index( self._curr )
            return self._list[ idx ]
        else:
            return None
 
    def step( self, s ):
        idx = self._list.index( self._curr )
        next_idx = ( idx + s ) % len( self._list )
        self._curr = self._list[ next_idx ]
        print( self._curr )

    def next( self ):
        self.step( 1 )
        return self.current()

    def prev( self ):
        self.step( -1 )
        return self.current()

    def insert( self, item ):
        
        if self._list.count( item ) > 0:
            self._list.remove( item )
        
        self._list.insert( 0, item )
        
        if not self._curr:
            self._curr = item
