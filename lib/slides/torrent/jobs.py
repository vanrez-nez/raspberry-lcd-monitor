from lib.core.slide import Slide

class TorrentJobs( Slide ):
    def __init__( self, client, *args, **kwargs ):
        super( TorrentJobs, self ).__init__( 'torrentjobs' )
        self._downloading = 0
        self._queued = 0
        self._done = 0
        self._client = client
        print('initializing TorrentJobs slide')
    
    def _update_jobs( self ):
        torrents = self._client.get_torrents()
        self._downloading = sum( 1 for t in torrents if t.status == 'downloading' )
        self._queue = sum( 1 for t in torrents if t.status == 'download pending' )
        self._done = sum( 1 for t in torrents if t.progress == 100 )

    def _get_buffer( self ):
        self._update_jobs()
        return 'JOBS: \x01 %d/%d \nDONE: \x05 %d' % (self._downloading, self._queue, self._done)

