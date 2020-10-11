from machine import PWM
from machine import Pin
from machine import deepsleep
from machine import Timer
from machine import RTC
from dth import DTH
import machine
import time
import pycom

### CONSTANTS ###
MAXTEMP = 20    # Desired inside temperature of chickencoup
DOOROPENTIME = 30 # Ammount of time it takes to open the door
DOORCLOSETIME = 30 # Ammount of time it takes to let the door close (might be different to open time)

p_in = Pin('P19', mode=Pin.IN, pull=Pin.PULL_UP)
th = DTH(Pin('P23', mode=Pin.OPEN_DRAIN),1) # Creating DHT object to get temperature and humidity
firstLed = Pin('P22', mode=Pin.OUT)
secondLed = Pin('P21', mode=Pin.OUT)
thirdLed = Pin('P20', mode=Pin.OUT)

rtc = RTC()
rtc.init((2020, 1, 1, 0, 0, 0, 0, 0))
lasttime = rtc.now()
machine.pin_sleep_wakeup(pins=(p_in);, mode=machine.WAKEUP_ANY_HIGH, enable_pull=True)

### FUNCTIONS ###
def controlClimate():   # Read temperature and humidity from DHT 22 and activate fan if temp is to high.
    result = th.read()
    if result.is_valid():
        if result.temperature > MAXTEMP:
            fanGND = Pin('P10', mode=Pin.OUT) #Declaring pin as digital output.
            fanGND.value(0) # Setting pin to zero/ GND for fan.
            pwm = PWM(0, frequency=5000)  # use PWM timer 0, with a frequency of 5KHz
            pwm_c_fan = pwm.channel(0, pin='P11', duty_cycle=1.0) # create pwm channel on pin P11 with a duty cycle of 50%

def openDoor():
    motorGND = Pin('P8', mode=Pin.OUT) # GND side for door motor
    motorGND.value(0)

    pwm = PWM(0, frequency=5000)  # use PWM timer 0, with a frequency of 5KHz
    # create pwm channel on pin P9 with a duty cycle of 100%
    pwm_c_motor = pwm.channel(0, pin='P9', duty_cycle=1.0)
    time.sleep(DOOROPENTIME)
    pwm_c_motor = pwm.channel(0, pin='P9', duty_cycle=0.0)

def closeDoor():
    motorGND = Pin('P9', mode=Pin.OUT) # GND side for door motor
    motorGND.value(0)

    pwm = PWM(0, frequency=5000)  # use PWM timer 0, with a frequency of 5KHz
    # create pwm channel on pin P8 with a duty cycle of 100%
    pwm_c_motor = pwm.channel(0, pin='P8', duty_cycle=1.0)
    time.sleep(DOORCLOSETIME)
    pwm_c_motor = pwm.channel(0, pin='P8', duty_cycle=0.0)

def setLeds(tup();): # setting leds to 0 or 1 in backwards order to read it as binary
    firstLed.value(tup[0])
    secondLed.value(tup[1])
    thirdLed.value(tup[2])

def showEggs(ammount):  # Show the ammount of eggs in binary with leds on the chickencoup
    leds = (0, 0, 0);   # create tuple to store binary ammount and pass this on to setleds()
    if ammount >= 4:
        leds[0] = 1
        ammount -= 4
        if ammount >= 2:
            leds[1] = 1
            ammount -= 2
            if ammount == 1:
                leds[2] = 1
    setLeds(leds)


def calculateEggs():    # Read out the loadcell to determine the ammount of eggs layed that day
    adc = machine.ADC() # create an ADC object
    apin = adc.channel(pin='P2', attn=adc.ATTN_0DB) # create an analog pin on P2 to read load cell
    weight = apin() # read an analog value

    if weight > 60:
        showEggs(1)
        if weight > 120:
            showEggs(2)
            if weight > 180:
                showEggs(3)
                if weight > 240:
                    showEggs(4)
    else: showEggs(0)


calculateEggs()
openDoor()

while True:
    counter = 0
    pycom.heartbeat(False)  # turning off LED from LoPy 4 to save energy
    if machine.wake_reason() == machine.PIN_WAKE:
        if p_in() == 1:# p_in(): get value, 0 or 1
            openDoor()
    if machine.wake_reason() == machine.PIN_WAKE:
        if p_in() == 0:
            closeDoor()
    if counter == 16:
        closeDoor()
    if counter == 24:
        calculateEggs()
        openDoor()
        counter = 0
    #if rtc.now() # Get get the current datetime tuple as (year, month, day, hour, minute, second, usecond, None)
    controlClimate()
    counter += 1
    #machine.deepsleep(59*60*1000) # Put the machine into deepsleep for 59 mins converted to ms
    # Possible problem with deepsleep on lopy as described in documentation. See following URL
    # https://docs.pycom.io/datasheets/development/lopy/#deep-sleep
