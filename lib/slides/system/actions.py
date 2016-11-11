import subprocess

from lib.core.slide import Slide
from lib.core.actions_menu import ActionsMenu
from lib.core.logger import Console
from lib.core.settings import Settings

class SystemActions( Slide ):
    
    _PROC_NAME = 'python lcd-monitor.py'

    def __init__( self, *args, **kwargs ):
        super( SystemActions, self ).__init__( 'sysactions' )
        self._menu = ActionsMenu( 'SYSTEM ACTIONS')
        # HALT, RESTART, SSH ON, SSH OFF, FTP ON, FTP OFF,
        # RENEW IP, LOOP MODE ON, LOOP MODE OFF
        self._menu.add_option( caption="SET STATIC IP", cb=self._on_static_ip )
        self._menu.add_option( caption="START SSH", cb=self._on_ssh_on )
        self._menu.add_option( caption="STOP SSH", cb=self._on_ssh_off )
        self._menu.add_option( caption="SHUTDOWN", cb=self._on_shutdown )
        self._menu.add_option( caption="RESTART", cb=self._on_restart )
        self._update_freq = 0.15
        self._settings = Settings()
        print( self._settings.read( 'network_interface' ) )

    def _exec( self, cmd ):
        pipe = subprocess.PIPE
        p = subprocess.Popen( "/bin/bash", stdin=pipe, stdout=pipe, shell=True )
        p.communicate( cmd )

    def _on_static_ip( self, cmd ):
        Console.info( 'Setting static IP' )

    def _on_dynamic_ip( self, cmd ):
        Console.info( 'Setting dynamic IP' )

    def _on_ssh_on( self, cmd ):
        Console.info( 'Turning SSH ON' )
        self._exec( "update-rc.d ssh enable && invoke-rc.d ssh start" )

    def _on_ssh_off( self, cmd ):
        Console.info( 'Turning SSH OFF' )
        self._exec( "update-rc.d ssh disable" )

    def _on_shutdown( self ):
        Console.critical( 'Shutting down' )
        self._exec( "pkill -f '%s'; sleep 1; shutdown -h now" % self._PROC_NAME )

    def _on_restart( self ):
        Console.critical( 'Rebooting' )
        self._exec( "pkill -f '%s'; sleep 1; shutdown -r now" % self._PROC_NAME )


    def navigate( self, key ):
        return self._menu.navigate( key )
    
    def _get_buffer( self ):
        return self._menu.get_buffer()

