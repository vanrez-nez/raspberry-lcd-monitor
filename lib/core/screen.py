import abc

class Screen( object ):
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def onActivate():
        """ Triggers when ScreenManager activates this screen """
        return

    @abc.abstractmethod
    def onDeactivate():
        """ Triggers when ScreenManager deactivates this screen """
        return

    @abc.abstractmethod
    def nextSlide():
        """ Triggers when ScreenManager asks to switch to next slide """
        return
    
    @abc.abstractmethod
    def prevSlide():
        """ Triggers when ScreenManager asks to switch to previous Slide """
        return
