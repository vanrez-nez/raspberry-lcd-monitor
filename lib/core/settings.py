import json
import os.path
from lib.core.logger import Console

class Settings( object ):
    
    _data = None
    _path = ''

    @staticmethod   
    def load( path ):
        Settings._data = None
        Settings._path = path
        if os.path.isfile( path ):
            try:
                with open( path ) as json_data:
                    Settings._data = json.load( json_data )
                    Console.info( 'Settings Loaded' )
            except:
                Console.error("Could't load settings from: %s" % path )
    
    def read( self, key_path, data = None ):
        try:
            data = data or Settings._data
            if type( key_path ) is list or type( key_path ) is tuple:
                key = key_path[ 0 ]
                keys_left = key_path[1:]
                if ( len( keys_left ) == 0 ):
                    return data[ key ]
                else:
                    return self.read( keys_left, data[ key ] )
            else:
                return self._data[ key_path ]
        except:
            return ""

