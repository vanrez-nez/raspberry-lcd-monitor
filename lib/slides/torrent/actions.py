from lib.core.slide import Slide
from lib.core.input import InputKeys
from lib.core.actions_menu import ActionsMenu
from lib.core.actions_task import ActionTask
from lib.core.settings import Settings

class TorrentActions( Slide ):

    def __init__( self, client, *args, **kwargs ):
        super( TorrentActions, self ).__init__( 'torrentactions' )
        self._client = client
        self._status = ''
        self._menu = ActionsMenu( 'TORRENT ACTIONS' )
        self._menu.add_option( 'STOP ALL', self._on_stop_all )
        self._menu.add_option( 'RESUME ALL', self._on_resume_all )
        self._menu.add_option( 'LIMIT ON', self._on_limit_on )
        self._menu.add_option( 'LIMIT OFF', self._on_limit_off )
        self._update_freq = 0.15
        self._task = None
        self._settings = Settings()
        print('initializing TorrentActions slide')

    def _on_stop_all( self ):
        task_func = lambda: [ t.stop() for t in self._client.get_torrents() ]
        self._task = ActionTask( task_func )

    def _on_resume_all( self ):
        task_func = lambda: [ t.start() for t in self._client.get_torrents() ]
        self._task = ActionTask( task_func )

    def _on_limit_on( self ):
        sld = self._settings.read( ( 'torrent_client', 'speed_limit_down' ) )
        slu = self._settings.read( ( 'torrent_client', 'speed_limit_up' ) )
        task_func = lambda: self._client.set_session( 
                speed_limit_down=sld,
                speed_limit_up=slu,
                speed_limit_down_enabled=True,
                speed_limit_up_enabled=True )
        self._task = ActionTask( task_func )

    def _on_limit_off( self ):
        task_func = lambda: self._client.set_session( 
                speed_limit_down_enabled=False,
                speed_limit_up_enabled=False )
        self._task = ActionTask( task_func )

    def navigate( self, key ): 
        return self._menu.navigate( key )

    def _get_buffer( self ):
        if ( self._task and self._task.is_running() ):
            return self._task.get_buffer()
        else:
            return self._menu.get_buffer()
