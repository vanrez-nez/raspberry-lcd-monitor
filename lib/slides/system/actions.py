import subprocess

from lib.core.slide import Slide
from lib.core.actions_menu import ActionsMenu
from lib.core.actions_task import ActionTask
from lib.core.logger import Console
from lib.core.settings import Settings

class SystemActions( Slide ):
    
    _PROC_NAME = 'python lcd-monitor.py'

    def __init__( self, *args, **kwargs ):
        super( SystemActions, self ).__init__( 'sysactions' )
        self._menu = ActionsMenu( 'SYSTEM ACTIONS')
        self._menu.add_option( caption="SET STATIC IP", cb=self._on_static_ip )
        self._menu.add_option( caption="SET DYNAMIC IP", cb=self._on_dynamic_ip )
        self._menu.add_option( caption="START SSH", cb=self._on_ssh_on )
        self._menu.add_option( caption="STOP SSH", cb=self._on_ssh_off )
        self._menu.add_option( caption="SHUTDOWN", cb=self._on_shutdown )
        self._menu.add_option( caption="RESTART", cb=self._on_restart )
        self._update_freq = 0.15
        self._settings = Settings()
        self._task = None

    def _exec( self, cmd ):
        pipe = subprocess.PIPE
        p = subprocess.Popen( "/bin/bash", stdin=pipe, stdout=pipe, shell=True )
        p.communicate( cmd )

    def _get_settings( self ):
        return {
            'dev': self._settings.read( ('system', 'network_interface' ) ),
            'addr': self._settings.read( ('system', 'static_ip' ) )
        }

    def _get_lambda_exec( self, cmd ):
        return lambda: self._exec( cmd )

    def _on_static_ip( self ):
        Console.info( 'Setting static IP' )
        cmd = ''.join( (
            'ip link set dev {s[dev]} down',
            '&& ip addr flush dev {s[dev]}',
            '&& ip addr add {s[addr]} dev {s[dev]}',
            '&& ip link set dev {s[dev]} up'
        ) ).format( s=self._get_settings() )

        print( cmd )

        task_func = self._get_lambda_exec( cmd )
        self._task = ActionTask( task_func )

    def _on_dynamic_ip( self ):
        Console.info( 'Setting dynamic IP' )
        cmd = ''.join( (
            'ip link set dev {s[dev]} down',
            '&& ip addr flush dev {s[dev]}',
            '&& ip link set dev {s[dev]} up',
            '&& dhclient {s[dev]}'
        ) ).format( s=self._get_settings() )

        task_func = self._get_lambda_exec( cmd )
        self._task = ActionTask( task_func )

    def _on_ssh_on( self ):
        Console.info( 'Turning SSH ON' )
        task_func = self._get_lambda_exec( "update-rc.d ssh enable && invoke-rc.d ssh start" )
        self._task = ActionTask( task_func )

    def _on_ssh_off( self ):
        Console.info( 'Turning SSH OFF' )
        task_func = self._get_lambda_exec( "update-rc.d ssh disable" )
        self._task = ActionTask( task_func )

    def _on_shutdown( self ):
        Console.critical( 'Shutting down' )
        task_func = self._get_lambda_exec( "pkill -f '%s'; sleep 1; shutdown -h now" % self._PROC_NAME )
        self._task = ActionTask( task_func )

    def _on_restart( self ):
        Console.critical( 'Rebooting' )
        self._exec( "pkill -f '%s'; sleep 1; shutdown -r now" % self._PROC_NAME )

    def navigate( self, key ):
        return self._menu.navigate( key )
    
    def _get_buffer( self ):
        if ( self._task and self._task.is_running() ):
            return self._task.get_buffer()
        else:
            return self._menu.get_buffer()

