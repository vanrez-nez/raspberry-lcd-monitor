import datetime
import psutil
from lib.core.slide import Slide

class SystemNetIp( Slide ):
    
    def __init__( self, iface='lo', *args, **kwargs ):
        super( SystemNetIp, self ).__init__( 'netip' )
        self._iface = iface
        print('initializing SystemIp slide')

    
    def _get_buffer( self ):
        net = psutil.net_io_counters()
        return "IP:192.168.203.23 \nIF: eth0"
        

