import datetime
import psutil
from lib.core.slide import Slide

class SystemCpuMem( Slide ):
    
    def __init__( self, *args, **kwargs ):
        super( SystemCpuMem, self ).__init__( 'cpu' )
        print('initializing SystemCPU slide')
    
    def _get_buffer( self ):
        cpu = psutil.cpu_percent(interval=2)
        mem = psutil.virtual_memory()
        f_mem = mem.available / 1024 / 1024
        return "CPU: %s%% \nMEM: %sMB free" % ( cpu, f_mem )
        

