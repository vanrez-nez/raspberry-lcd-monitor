import urllib2
import datetime
import psutil
from lib.core.slide import Slide

class SystemNetPublicIp( Slide ):
    
    def __init__( self, url, *args, **kwargs ):
        super( SystemNetPublicIp, self ).__init__( 'netpubip' )
        self._service_url = url 
        self._ip = '127.0.0.1'
        self._update_freq = 15
        print('initializing SystemNetPublicIp slide')
    
    def _update_ip( self ):
        try:
            self._ip = urllib2.urlopen( self._service_url ).read()
        except Exception:
            self._ip = '0.0.0.0'
        
    def _get_buffer( self ):
        self._update_ip()
        return "PUBLIC IP\n\x03%s" % ( self._ip )
