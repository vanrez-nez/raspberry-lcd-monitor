from lib.core.cycled_list import CycledList
class Screen:
   
    def __init__( self, color ):
        self._color = color
        self._initted = False
        self._slides = CycledList()
        
    def activate( self ):
        """ Triggers when ScreenManager activates this screen """
        self._slides.current().activate()

    def deactivate( self ):
        """ Triggers when ScreenManager deactivates this screen """
        self._initted = False
        self._slides.current().deactivate()     
    
    def next_slide( self ):
        """ Switch to next slide """
        self._slides.next().activate()
    
    def prev_slide( self ):
        """ Switch to previous slide """
        self._slides.prev().activate()
    
    def add_slide( self, slide ):
        """ Adds a new slide to screen """
        self._slides.insert( slide )

    def get_current_slide( self ):
        """ Returns the current slide """
        return self._slides.current()
    
    def initialize( self, alcd ):
        alcd.clear()
        alcd.set_color( self._color[0], self._color[1], self._color[2] )

    def update( self, alcd ):

        if not self._initted:
            self._initted = True
            self.initialize( alcd )
       
        if self._slides.current():
            self._slides.current().update( alcd )
