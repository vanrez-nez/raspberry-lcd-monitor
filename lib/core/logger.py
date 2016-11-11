from termcolor import colored

class Console(object):
    @staticmethod
    def log( msg ):
        print colored( msg, 'white' )

    @staticmethod
    def critical( msg ):
        print colored( msg, 'red' )

    @staticmethod
    def error( msg ):
        print colored( msg, 'red', attrs=[ 'reverse' ] )

    @staticmethod
    def warn( msg ):
        print colored( msg, 'yellow' )

    @staticmethod
    def info( msg ):
       print colored( msg, 'green' )
        
