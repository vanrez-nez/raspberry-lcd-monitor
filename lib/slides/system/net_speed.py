import time
import psutil
from threading import Thread
from datetime import datetime, timedelta
from collections import deque
from lib.core.slide import Slide
from lib.core.utils import format_bytes

class SystemNetSpeed( Slide ):

    _MAX_SAMPLES = 6
    
    def __init__( self, iface='lo', *args, **kwargs ):
        super( SystemNetSpeed, self ).__init__( 'netspeed' )
        self._iface = iface
        self._samples = deque( maxlen = self._MAX_SAMPLES )
        self._download = 0
        self._upload = 0
        self._update_thread = None
        self._update_freq = 1
        print('initializing SystemNetwork slide')
    
    def activate( self ):
        super( SystemNetSpeed, self ).activate()
        if not self._update_thread:
            t = Thread( target = self._update_loop )
            t.daemon = True
            t.start()
            self._update_thread = t 

    def _get_counters( self ):
        nics = psutil.net_io_counters( pernic = True )
        c = nics[ self._iface ] if self._iface in nics else nics[ 'lo' ]
        """c = (bytes_send, bytes_recv, ...) """
        return ( c[ 1 ], c[ 0 ] )

    def _update_loop( self ):
        while self._active:
            self._update_speed()
            time.sleep( 0.5 )
        self._update_thread = None

    def _update_speed( self ):
        self._samples.append( ( datetime.now(), self._get_counters() ) )
        
        elapsed_sec = 0.001
        prev_time = None
        pb = ( 0, 0 )
        tb = ( 0, 0 )

        # get total time/download from samples and calculate average        
        for idx, s in enumerate( list( self._samples ) ):
            if idx > 0:
                diff_d = s[1][0] - pb[0]
                diff_u = s[1][1] - pb[1]
                tb = ( tb[0] + diff_d, tb[1] + diff_u )
                pb = ( s[1][0], s[1][1] )
                elapsed_sec += ( s[ 0 ] - prev_time ).total_seconds()
                prev_time = s[ 0 ]
            else:
                pb = ( s[1][0], s[1][1] )
                prev_time = s[ 0 ]
        
        self._download = tb[0] / elapsed_sec
        self._upload = tb[1] / elapsed_sec

    def _get_buffer( self ):
        
        # format speeds and separate from suffix
        dl = format_bytes( self._download ).split( ' ' )
        ul = format_bytes( self._upload ).split( ' ' )
        
        # apply fixed blank padding to speeds
        d_speed = "%s%s" % ( dl[ 0 ].ljust( 7 ), dl[ 1 ] )
        u_speed = "%s%s" % ( ul[ 0 ].ljust( 7 ), ul[ 1 ] )

        return "D: \x01 %sps \nU: \x02 %sps" % ( d_speed, u_speed )
        

