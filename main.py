import pycom
import time
import machine
from machine import Pin
from dth import DTH

pycom.heartbeat(False)
pycom.rgbled(0x000008) # blue

adc = machine.ADC()             # create an ADC object
apin = adc.channel(pin='P16', attn=adc.ATTN_0DB)   # create an analog pin on P16 to read load cell
weight = apin()                    # read an analog value

th = DTH(Pin('P23', mode=Pin.OPEN_DRAIN),1)
time.sleep(2)
result = th.read()
if result.is_valid():
    pycom.rgbled(0x001000) # green
    print('analog val: ')
    print(weight)
    print('Temperature: {:3.2f}'.format(result.temperature/1.0))
    print('Humidity: {:3.2f}'.format(result.humidity/1.0))

while True:
    weight = apin()                    # read an analog value
    print(weight)
