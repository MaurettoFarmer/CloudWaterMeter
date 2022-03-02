from machine import Pin
import time
import struct


RAIN_PIN        = 'P11'   # Rain switch
HL_01_PIN       = 'P8'    # Hall sensor 1
HL_02_PIN       = 'P9'    # Hall sensor 2
HL_03_PIN       = 'P10'   # Hall sensor 3
CH_01_PIN       = 'P4'    # Timer channel 1
CH_02_PIN       = 'P14'   # Timer channel 2
CH_03_PIN       = 'P13'   # Timer channel 3
CH_04_PIN       = 'P15'   # Timer channel 4
CH_05_PIN       = 'P16'   # Timer channel 5
CH_06_PIN       = 'P17'   # Timer channel 6
CH_07_PIN       = 'P18'   # Timer channel 7
CH_08_PIN       = 'P19'   # Timer channel 8
CH_09_PIN       = 'P20'   # Timer channel 9
CH_10_PIN       = 'P21'   # Timer channel 10
CH_11_PIN       = 'P22'   # Timer channel 11
CH_12_PIN       = 'P23'   # Timer channel 12
HALL_MODE       = 0
CHANNEL_MODE    = 1


class IO_Manager:

  def __init__(self, debounce=50):
    self.rain  = Pin(RAIN_PIN, mode=Pin.OUT)

    self.hlist = [  self.inputPin(HL_01_PIN, 5000, HALL_MODE)
                  , self.inputPin(HL_02_PIN, 5000, HALL_MODE)
                  , self.inputPin(HL_03_PIN, 5000, HALL_MODE)]

    self.clist = [  self.inputPin(CH_01_PIN, debounce, CHANNEL_MODE)
                  , self.inputPin(CH_02_PIN, debounce, CHANNEL_MODE)
                  , self.inputPin(CH_03_PIN, debounce, CHANNEL_MODE)
                  , self.inputPin(CH_04_PIN, debounce, CHANNEL_MODE)
                  , self.inputPin(CH_05_PIN, debounce, CHANNEL_MODE)
                  , self.inputPin(CH_06_PIN, debounce, CHANNEL_MODE)
                  , self.inputPin(CH_07_PIN, debounce, CHANNEL_MODE)
                  , self.inputPin(CH_08_PIN, debounce, CHANNEL_MODE)
                  , self.inputPin(CH_09_PIN, debounce, CHANNEL_MODE)
                  , self.inputPin(CH_10_PIN, debounce, CHANNEL_MODE)
                  , self.inputPin(CH_11_PIN, debounce, CHANNEL_MODE)
                  , self.inputPin(CH_12_PIN, debounce, CHANNEL_MODE)]

  def values(self):
    tot = 0
    for x in range(0, len(self.clist)):
      if self.clist[x].value() > 0:
        tot|=1<<x
    return bytes(struct.pack('>hhhh',tot,self.hlist[0].value()*10,self.hlist[1].value()*10,self.hlist[2].value()*10))

  def enableTimer(self):
    self.rain.value(True)

  def disableTimer(self):
    self.rain.value(False)

  class inputPin:

    def __init__(self, id, debounce, in_mode):
      self.pin              = Pin(id, mode=Pin.IN)
      self.mode             = in_mode
      self.counter          = 0
      self.now              = 0
      self.last             = 0
      self.debounce         = debounce
      self.lastDebounceTime = 0
      self.pin.callback(Pin.IRQ_FALLING|Pin.IRQ_RISING, self.cllbck)
      #self.pin.callback(Pin.IRQ_FALLING, self.cllbck)

    def value(self):
        retval = self.counter
        self.counter += int(not self.pin.value()) * self.mode - retval
        return retval

    def reset(self):
      self.counter = 0

    def cllbck(self, cllbck_pin):
      time_now = time.ticks_ms()
      if (time_now - self.lastDebounceTime) >= self.debounce:
        self.now = not cllbck_pin.value()
        self.counter += self.now
        print(cllbck_pin.id())
        print(self.now)
        self.lastDebounceTime = time_now
