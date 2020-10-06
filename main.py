from machine import PWM
from machine import Pin
from dth import DTH
import machine
import time
import pycom

pycom.heartbeat(False)

#########LOADCELL#############
#adc = machine.ADC()             # create an ADC object
#apin = adc.channel(pin='P2', attn=adc.ATTN_0DB)   # create an analog pin on P2 to read load cell
#weight = apin()                    # read an analog value
########END of LOADCELL###########

####DHT#########
th = DTH(Pin('P23', mode=Pin.OPEN_DRAIN),1)
time.sleep(2)
result = th.read()
if result.is_valid():
    pycom.rgbled(0x001000) # green
    print('analog val: ')   # print analog value of loadcell
    print(weight)           # print analog value of loadcell
    print('Temperature: {:3.2f}'.format(result.temperature/1.0))
    print('Humidity: {:3.2f}'.format(result.humidity/1.0))
####END of DHT##########

##########MOTOR + FAN###########
motorGND = Pin('P8', mode=Pin.OUT) # GND side for motor and fan.
fanGND = Pin('P10', mode=Pin.OUT)
motorGND.value(0)
fanGND.value(0)

pwm = PWM(0, frequency=5000)  # use PWM timer 0, with a frequency of 5KHz
# create pwm channel on pin P9 with a duty cycle of 50%
pwm_c_motor = pwm.channel(0, pin='P9', duty_cycle=1.0)
time.sleep(3)

motorGND = Pin('P9', mode=Pin.OUT)
motorGND.value(0)


pwm_c = pwm.channel(0, pin='P8', duty_cycle=1.0)   # Changing PWM and GND pin of motor to turn the other way.
time.sleep(3)
###########END of MOTOR + FAN##############

#####LEDS#######
redLed = Pin('P22', mode=Pin.OUT)
yellowLed = Pin('P21', mode=Pin.OUT)
whiteLed = Pin('P20', mode=Pin.OUT)

while True:
    redLed.value(1)
    yellowLed.value(1)
    whiteLed.value(0)
    time.sleep(3)
    redLed.value(0)
    yellowLed.value(0)
    whiteLed.value(1)
    time.sleep(3)
