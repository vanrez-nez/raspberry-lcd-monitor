import time
import signal
import sys
import os
import transmissionrpc
from transmissionrpc.error import TransmissionError
from termcolor import colored
from Adafruit_CharLCD import Adafruit_CharLCDPlate as ALCD

from lib.core.settings import Settings
from lib.core.logger import Console
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
from lib.slides.system.actions import SystemActions

from lib.slides.torrent.jobs import TorrentJobs
from lib.slides.torrent.actions import TorrentActions

if not os.geteuid() == 0:
    Console.warn( 'For full functionality execute this script as root.' )

# Load Settings
settings = Settings()
current_dir = os.path.dirname( os.path.realpath( __file__ ) )
settings.load( "%s/settings.json" % current_dir )

lcd = ALCD()

# Register custom glyphs
lcd.create_char( 1, [ 0, 4, 4, 4, 31, 14, 4, 0 ] ) # arrow_down
lcd.create_char( 2, [ 0, 4, 14, 31, 4, 4, 4, 0 ] ) # arrow_up
lcd.create_char( 3, [ 0, 8, 12, 14, 12, 8, 0, 0 ] ) # triangle right
lcd.create_char( 4, [ 0, 2, 6, 14, 6, 2, 0, 0 ] ) # triangle left
lcd.create_char( 5, [ 0, 1, 3, 22, 28, 8, 0, 0 ]) #check
lcd.create_char( 6, [ 0, 0, 14, 17, 17, 17, 14, 0 ] ) #unfocused
lcd.create_char( 7, [ 0, 0, 14, 31, 31, 31, 14, 0 ] ) #focused
lcd.create_char( 0, [ 0, 0, 0, 4, 14, 4, 0, 0 ] ) #cross

input_handler = InputHandler()
director = ScreenDirector()

# Add System Screen

net_iface = settings.read( ( 'system', 'network_interface' ) )
net_ipurl = settings.read( ( 'system', 'public_ip_url' ) )
hdd_devs = settings.read( ( 'system', 'hdd_devs' ) )

system_screen = Screen( color=[ 0, 1, 0 ] )
system_screen.add_slide( SystemUpTime() )
system_screen.add_slide( SystemNetLocalIp( iface=net_iface ) )
system_screen.add_slide( SystemNetPublicIp( url=net_ipurl ) )
system_screen.add_slide( SystemNetSpeed( iface=net_iface) )
system_screen.add_slide( SystemCpuMem() )
system_screen.add_slide( SystemHd( mount_point='/') )
system_screen.add_slide( SystemActions() )
director.add_screen( system_screen )

# Add Torrent Screen

torrent_addr = settings.read( ( 'torrent_client', 'address' ) )
torrent_port = settings.read( ( 'torrent_client', 'port' ) )
torrent_user = settings.read( ( 'torrent_client', 'user' ) )
torrent_pass = settings.read( ( 'torrent_client', 'password' ) )

try:
    torrent_client = transmissionrpc.Client(
        address=torrent_addr, port=torrent_port,
        user=torrent_user, password=torrent_pass
    )
    torrent_screen = Screen( color=[ 1, 1, 0 ] )
    torrent_screen.add_slide( TorrentJobs( torrent_client ) )
    torrent_screen.add_slide( TorrentActions( torrent_client ) )
    director.add_screen( torrent_screen )
except TransmissionError as err:
    Console.error( 'Failed to initialize torrent client:\n%s' % err )


# Register shutdown handler
def shutdown( signum, frame ):
    Console.critical( "Shutting down" )
    director.release_all()
    lcd.clear()
    lcd.message( 'X.X' )
    lcd.set_color( 1, 0, 0 )
    time.sleep( 0.5 )
    lcd.set_backlight( 0 )
    sys.exit( 0 )

signal.signal( signal.SIGTERM, shutdown )
signal.signal( signal.SIGINT, shutdown )

# Start Main Loop
input_handler.signal_key_press.connect( director.on_key_press )

while True:
    input_handler.update( lcd )
    director.update( lcd )
    time.sleep( 0.1 )
