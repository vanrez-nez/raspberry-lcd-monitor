from datetime import datetime
from threading import Thread
import time

class ActionTask():

    def __init__( self, task_function, message="Working..." ):
        self._task_function = task_function
        self._set_message( message )
        self._thread = Thread( target=self._exec_task )
        self._thread.daemon = True
        self._start_task()

    def _set_message( self, message ):
        self._message = str.center( message, 16 )

    def _exec_task( self ):
        print( 'TaskStart' )
        self._task_function()
        self._set_message( 'Done' )
        time.sleep( 0.75 )
        print( 'TaskEnded' )

    def _start_task( self ):
        if not self._thread.is_alive():
            self._thread.start()

    def is_running( self ):
        return self._thread.is_alive()

    def get_buffer( self ):
        return self._message

