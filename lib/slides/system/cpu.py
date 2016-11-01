from lib.core.slide import Slide

class SystemCPU( Slide ):
    
    def __init__( self, *args, **kwargs ):
        super( SystemCPU, self ).__init__( 'cpu' )
        print('initializing SystemCPU slide')
    
    def update(self, alcd):
        return
