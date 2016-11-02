from lib.core.slide import Slide

class TorrentJobs( Slide ):
    def __init__( self, *args, **kwargs ):
        super( TorrentJobs, self ).__init__( 'torrent_jobs' )
        print('initializing TorrentJobs slide')

    def update( self, alcd ):
        return

