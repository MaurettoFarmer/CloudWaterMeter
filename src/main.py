from network import Sigfox
from IO_Manager import IO_Manager
from machine import Timer
import time
import socket
import time
import network
import pycom

#pycom.heartbeat(False)
ioman   = IO_Manager()
sigfox  = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ1)
chrono  = Timer.Chrono()
chrono.start()

while True:
  try:
    time.sleep(618-chrono.read())
    chrono.reset()
    s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)
    s.setblocking(True)
    s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)
    pycom.rgbled(0x002000)
    s.send(ioman.values())
    pycom.rgbled(0)
    s.close()
  except:
    print("Caught exception")
    pycom.rgbled(0x200000)
