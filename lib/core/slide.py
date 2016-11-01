class Slide( object ):

    def __init__( self, name ):
        self._name = name

    def activate( self ):
        print( 'Activating Slide %s' % self._name )
    
    def deactivate( self ):
        print( 'Deactivating Slide %s' % self._name )
    
    def update( self, alcd ):
        return
