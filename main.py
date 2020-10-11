from machine import PWM
from machine import Pin
from machine import deepsleep
from machine import Timer
from dth import DTH
import machine
import time
import pycom

### CONSTANTS ###
MAXTEMP = 20    # Desired inside temperature of chickencoup
DOOROPENTIME = 30 # Ammount of time it takes to open the door
DOORCLOSETIME = 30 # Ammount of time it takes to let the door close (might be different to open time)

th = DTH(Pin('P23', mode=Pin.OPEN_DRAIN),1) # Creating DHT object to get temperature and humidity
firstLed = Pin('P22', mode=Pin.OUT)
secondLed = Pin('P21', mode=Pin.OUT)
thirdLed = Pin('P20', mode=Pin.OUT)

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

def setLeds(valThree, valTwo, valOne): # setting leds to 0 or 1 in backwards order to read it as binary
    firstLed.value(valOne)
    secondLed.value(valTwo)
    thirdLed.value(valThree)

def showEggs(ammount):  # Show the ammount of eggs in binary with leds on the chickencoup
    if ammount == 0:
        setLeds(0, 0, 0)
        if ammount == 1 :
            setLeds(0, 0, 1)
            if ammount == 2:
                setLeds(0, 1, 0)
                if ammount == 3:
                    setLeds(0, 1, 1)
                    if ammount == 4:
                        setLeds(1, 0, 0)


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

class Clock:

    def _init_(self):
        self.hours = 0
        self.__alarm = Timer.Alarm(self._hours_handler, 1, periodic=True)

    def _hours_handler(self, alarm):
        self.hours += 1
        print("%02d hours have passed" % self.hours)
        if self.hours == 11:
            closeDoor()

clock = Clock()

pycom.heartbeat(False)  # turning off LED from LoPy 4 to save energy
controlClimate()
while True:
    controlClimate()
    (wake_reason, gpio_list) = machine.wake_reason()
    print("Device running for: " + str(time.ticks_ms()) + "ms")
    print("Remaining sleep time: " + str(machine.remaining_sleep_time()) + "ms" )
    if wake_reason == machine.PWRON_WAKE:
        print("Woke up by reset button")
    elif wake_reason == machine.PIN_WAKE:
        print("Woke up by external pin (external interrupt)")
        print(*gpio_list, sep=", ")
    elif wake_reason == machine.RTC_WAKE:
        print("Woke up by RTC (timer ran out)")
    elif wake_reason == machine.ULP_WAKE:
        print("Woke up by ULP (capacitive touch)")
    machine.pin_sleep_wakeup(('P3', 'P4'), mode=machine.WAKEUP_ANY_HIGH, enable_pull=True)
    #machine.deepsleep(3600000,'P10', enable_pull == True):

pycom.heartbeat(False)  # turning off LED from LoPy 4 to save energy
controlClimate()
#while True:    # TODO: Make a loop to controlClimate every hour using deepsleep in between and calculateEggs + openDoor every morning at 7AM. Close door at 8 PM
#    controlClimate()
#    machine.deepsleep(3600000)
openDoor()
#calculateEggs()
closeDoor()
