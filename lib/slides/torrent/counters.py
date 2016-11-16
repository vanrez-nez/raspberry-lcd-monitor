from lib.core.slide import Slide
from lib.core.utils import format_bytes

class TorrentCounters( Slide ):

    def __init__( self, client, *args, **kwargs ):
        super( TorrentCounters, self ).__init__( 'torrentcounters' )
        self._client = client
        self._total_rx = 0
        self._total_tx = 0
        self._update_freq = 5
        print('initializing TorrentCounters slide')
    
    def _update_usage( self ):
        stats = self._client.session_stats().cumulative_stats
        self._total_rx = stats[ 'downloadedBytes' ]
        self._total_tx = stats[ 'uploadedBytes' ]

    def _get_buffer( self ):
        self._update_usage()
        
        rx = format_bytes( self._total_rx ).split( ' ' )
        tx = format_bytes( self._total_tx ).split( ' ' )

        r_format = "%s%s" % ( rx[ 0 ].ljust( 7 ), rx[ 1 ] )
        t_format = "%s%s" % ( tx[ 0 ].ljust( 7 ), tx[ 1 ] )

        return 'DL: \x01 %s \nUL: \x05 %s' % ( r_format, t_format )

