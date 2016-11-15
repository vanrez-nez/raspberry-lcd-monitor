import urllib2
import psutil
import time
from threading import Thread
from datetime import datetime, timedelta
from lib.core.slide import Slide

class SystemNetPublicIp( Slide ):

    _REQUEST_FREQ = 60
    
    def __init__( self, url, *args, **kwargs ):
        super( SystemNetPublicIp, self ).__init__( 'netpubip' )
        self._service_url = url 
        self._ip = '127.0.0.1'
        self._update_thread = None
        print('initializing SystemNetPublicIp slide')
    
    def activate( self ):
        super( SystemNetPublicIp, self ).activate()
        if not self._update_thread:
            t = Thread( target = self._update_ip )
            t.daemon = True
            t.start()
            self._update_thread = t

    def _update_ip( self ):
        while self._active:
            try:
                self._ip = urllib2.urlopen( self._service_url ).read()
            except Exception:
                self._ip = '0.0.0.0'
            time.sleep( self._REQUEST_FREQ )
        
    def _get_buffer( self ):
        return "PUBLIC IP\n\x03%s" % ( self._ip )
