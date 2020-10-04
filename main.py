from machine import Pin
import time

redLed = Pin('P3', mode=Pin.OUT)
yellowLed = Pin('P4', mode=Pin.OUT)
whiteLed = Pin('P5', mode=Pin.OUT)

while True:
    redLed.value(1)
    yellowLed.value(1)
    whiteLed.value(0)
    time.sleep(3)
    redLed.value(0)
    yellowLed.value(0)
    whiteLed.value(1)
    time.sleep(3)
