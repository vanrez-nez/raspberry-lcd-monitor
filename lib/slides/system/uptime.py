from datetime import datetime, timedelta
import psutil
from lib.core.slide import Slide

class SystemUpTime( Slide ):
    
    def __init__( self, *args, **kwargs ):
        super( SystemUpTime, self ).__init__( 'uptime' )
        self._up_time = 0
        self._update_freq = 1
        print('initializing SystemUpTime slide') 
    
    def _update_uptime( self ):
        boot_time = datetime.fromtimestamp( psutil.boot_time() )
        elapsed = (datetime.now() - boot_time).seconds
        self._up_time = str( timedelta( 0, elapsed ) )

    def _get_buffer( self ):
        self._update_uptime()
        t_centered = self._up_time.center( 16, ' ' )
        return " TOTAL UP TIME \n%s" % ( t_centered )
        

