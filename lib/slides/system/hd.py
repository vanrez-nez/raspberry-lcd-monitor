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
        hd_free = format_bytes( hd.free, decimals=2 )
        return "HDD: %s\nDEV: %s" % ( hd_free, self._mount_point )
        

