from lib.core.slide import Slide
from lib.core.input import InputKeys
from lib.core.actions_menu import ActionsMenu

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
        print('initializing TorrentJobs slide')
    
    def _on_stop_all( self ):
        pass

    def _on_resume_all( self ):
        pass

    def _on_limit_on( self ):
        pass

    def _on_limit_off( self ):
        pass

    def navigate( self, key ): 
        return self._menu.navigate( key )

    def _get_buffer( self ):
        if self._status:
            return "%s\n" % self._status
        else:
            return self._menu.get_buffer()
