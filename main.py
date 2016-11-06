#!usr/bin/python
import time
import atexit
import transmissionrpc
from Adafruit_CharLCD import Adafruit_CharLCDPlate as ALCD

from lib.core.input import InputHandler
from lib.core.input import InputKeys
from lib.core.screen import Screen
from lib.core.screen_director import ScreenDirector

from lib.slides.system.cpu_mem import SystemCpuMem
from lib.slides.system.hd import SystemHd
from lib.slides.system.net_speed import SystemNetSpeed
from lib.slides.system.net_local_ip import SystemNetLocalIp
from lib.slides.system.net_public_ip import SystemNetPublicIp
from lib.slides.system.net_transfer import SystemNetTransfer
from lib.slides.system.uptime import SystemUpTime

from lib.slides.torrent.jobs import TorrentJobs

lcd = ALCD()

# Register custom glyphs
lcd.create_char( 1, [ 0, 4, 4, 4, 31, 14, 4, 0 ] ) # arrow_down
lcd.create_char( 2, [ 0, 4, 14, 31, 4, 4, 4, 0 ] ) # arrow_up
lcd.create_char( 3, [ 8, 12, 14, 15, 14, 12, 8, 0 ] ) # triangle right
lcd.create_char( 4, [ 0, 1, 3, 22, 28, 8, 0, 0 ]) #check

input_handler = InputHandler()
director = ScreenDirector()

""" Add System Screen """
system_screen = Screen( color=[1.0, 0.0, .0] )
system_screen.add_slide( SystemUpTime() )
system_screen.add_slide( SystemNetLocalIp( iface='usb0' ) )
system_screen.add_slide( SystemNetPublicIp( url='https://api.ipify.org' ) )
system_screen.add_slide( SystemNetSpeed( iface='usb0') )
system_screen.add_slide( SystemCpuMem() )
system_screen.add_slide( SystemHd( mount_point='/') )
director.add_screen( system_screen )

""" Add Torrent Screen """
torrent_client = transmissionrpc.Client('127.0.0.1', port=9091)
torrent_screen = Screen( color=[1.0, 1.0, 0.0] )
torrent_screen.add_slide( TorrentJobs( torrent_client ) )
director.add_screen( torrent_screen )

@atexit.register
def shutdown():
    print( "Shutting down" )
    director.release_all()
    lcd.set_backlight( 0.5 )

def navigate( key ):
    if key == InputKeys.Up:
        director.get_current_screen().next_slide()
    elif key == InputKeys.Down:
        director.get_current_screen().prev_slide()
    elif key == InputKeys.Right:
        director.next_screen()
    elif key == InputKeys.Left:
        director.prev_screen()

input_handler.signal_key_press.connect( navigate )

while True:
    input_handler.update( lcd )
    director.update( lcd )
    time.sleep( 0.1 )
