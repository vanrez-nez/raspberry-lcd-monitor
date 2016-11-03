import datetime
import psutil
from lib.core.utils import format_bytes

from lib.core.slide import Slide

class SystemHd( Slide ):
    
    def __init__( self, mount_point, *args, **kwargs ):
        self._mount_point = mount_point
        super( SystemHd, self ).__init__( 'hd' )
        print('initializing HardDriveSlide slide')
    
    def _get_buffer( self ):
        hd = psutil.disk_usage( self._mount_point )
        hd_total = format_bytes( hd.total )
        return "T:%s" % ( hd_total )
        

