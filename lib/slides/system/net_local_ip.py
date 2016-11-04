import datetime
import psutil
from lib.core.slide import Slide

class SystemNetLocalIp( Slide ):
    
    def __init__( self, iface='lo', *args, **kwargs ):
        super( SystemNetLocalIp, self ).__init__( 'netloip' )
        self._iface = iface
        self._ip = '127.0.0.1'
        self._curr_iface = 'lo'
        self._update_freq = 5
        print('initializing SystemNetLocalIp slide')
    
    def _update_ip( self ):
        addrs = psutil.net_if_addrs()
        self._curr_iface = self._iface if self._iface in addrs else 'lo'
        a = addrs[ self._curr_iface ]
        self._ip = a[ 0 ][ 1 ]
        
    def _get_buffer( self ):
        self._update_ip()
        return "LOCAL IP (%s)\n\x03%s" % ( self._curr_iface, self._ip )
