from itertools import cycle

class CycledList:
    
    def __init__( self ):
        self._list = []
        self._curr = 0

    def current( self ):
        return self._curr if self._curr != None else None
 
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
    
    def get_list( self ):
        return self._list[:]
