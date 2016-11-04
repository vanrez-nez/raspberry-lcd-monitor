import datetime
import psutil
from lib.core.slide import Slide

class SystemNetTransfer( Slide ):
    
    def __init__( self, iface='lo', *args, **kwargs ):
        super( SystemNetTransfer, self ).__init__( 'nettransfer' )
        self._iface = iface
        print('initializing SystemNetworkTransfer slide')

    
    def _get_buffer( self ):
        net = psutil.net_io_counters()
        return "RX: \x01999 GB \nTX: \x02999 GB"
        

