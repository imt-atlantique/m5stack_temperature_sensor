from machine import Pin
import _onewire

def init(pin):
  Pin(pin, Pin.OPEN_DRAIN, Pin.PULL_UP)
  
def convert(pin):
  _onewire.reset(Pin(pin))
  _onewire.writebyte(Pin(pin), 0xcc)
  _onewire.writebyte(Pin(pin), 0x44)

def read(pin):
  _onewire.reset(Pin(pin))
  _onewire.writebyte(Pin(pin), 0xcc)
  _onewire.writebyte(Pin(pin), 0xbe)
  tlo = _onewire.readbyte(Pin(pin))
  thi = _onewire.readbyte(Pin(pin))
  _onewire.reset(Pin(pin))
  temp = tlo + thi * 256
  if temp > 32767:
    temp = temp - 65536
  temp = temp * 0.0625
  return(temp)
