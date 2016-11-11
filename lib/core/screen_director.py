from lib.core.cycled_list import CycledList
from lib.core.input import InputKeys
from lib.core.logger import Console

class ScreenDirector:

    def __init__( self ):
        self._screens = CycledList()

    def add_screen( self, screen ):
        self._screens.insert( screen )

    def next_screen( self ):
        self._screens.current().deactivate()
        self._screens.next().activate()
        Console.info( 'Going to NextScreen' )
    
    def prev_screen( self ):
        self._screens.current().deactivate()
        self._screens.next().activate()
        Console.info( 'Going to PrevScreen' )
    
    def get_current_screen( self ):
        return self._screens.current()

    def on_key_press( self, key ):
        current_screen = self._screens.current()
        # Check if current screen is overriding input events
        if current_screen and not current_screen.navigate( key ):

            #If not then continue with normal navigation
            if key == InputKeys.Up:
                self.next_screen()
            elif key == InputKeys.Down:
                self.prev_screen()
            elif key == InputKeys.Right:
                current_screen.next_slide()
            elif key == InputKeys.Left:
                current_screen.prev_slide()

    def update( self, alcd ):
        if self._screens.current():
            self._screens.current().update( alcd )

    def release_all( self ):
        for screen in self._screens.get_list():
            screen.release()
