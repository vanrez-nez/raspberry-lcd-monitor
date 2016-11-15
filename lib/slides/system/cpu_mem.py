import datetime
import psutil
from threading import Thread
from lib.core.slide import Slide
from lib.core.utils import format_bytes

class SystemCpuMem( Slide ):

    def __init__( self, *args, **kwargs ):
        super( SystemCpuMem, self ).__init__( 'cpu' )
        print('initializing SystemCPU slide')
        self._update_thread = None
        self._cpu_percent = -1
        self._mem_free = -1
        self._update_freq = 3

    def activate( self ):
        super( SystemCpuMem, self ).activate()
        if not self._update_thread:
            t = Thread( target = self._update_loop )
            t.daemon = True
            t.start()
            self._update_thread = t

    def _update_loop( self ):
        while self._active:
            # print( 'updating thread' )
            self._update_stats()
        self._update_thread = None

    def _update_stats( self ):
        interval = 0 if self._cpu_percent == -1 else 2
        self._cpu_percent = psutil.cpu_percent(interval=interval)
        self._mem_free = psutil.virtual_memory().available
    
    def _get_buffer( self ):
        # force to update if no info has been collected so far 
        if self._cpu_percent == -1:
            self._update_stats()
        cpu = self._cpu_percent
        f_mem = format_bytes( self._mem_free )
        # print( f_mem )
        return "CPU: %s%% \nMEM: %s" % ( cpu, f_mem )
