from machine import PWM
from machine import Pin
from machine import deepsleep
from machine import RTC
from dth import DTH
#from hx711 import HX711
import machine
import time
import pycom
#import sys

### CONSTANTS ###
MAXTEMP = 20    # Desired inside temperature of chickencoup
DOOROPENTIME = 30 # Ammount of time it takes to open the door
DOORCLOSETIME = 30 # Ammount of time it takes to let the door close (might be different to open time)

p_in = Pin('P19', mode=Pin.IN, pull=Pin.PULL_UP) # Input for door switch
th = DTH(Pin('P23', mode=Pin.OPEN_DRAIN),1) # Creating DHT object to get temperature and humidity
firstLed = Pin('P22', mode=Pin.OUT) # Leds to show ammount of eggs in binary (firstLed is the left most led (MSB))
secondLed = Pin('P21', mode=Pin.OUT) # secondLed and thridLed are to the right of firstLed
thirdLed = Pin('P20', mode=Pin.OUT)

rtc = RTC() # init with default time and date
lasttime = rtc.now() # Variable to store the last time an action was performed to calculate the time difference
#machine.pin_sleep_wakeup(pins=p_in, mode=machine.WAKEUP_ANY_HIGH, enable_pull=True) # Enabeling the swith to wake up the lopy from deepsleep

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
    motorGND = Pin('P8', mode=Pin.OUT) # Enable of LN298 is connected to 3V3 so we have to switch the input pins to turn the motor the other way
    motorGND.value(0)                  # The DC motor needs GND on 1 pin and a PWM signal on the other pin (we use pin 8 as GND now)

    pwm = PWM(0, frequency=5000)  # use PWM timer 0, with a frequency of 5KHz
    pwm_c_motor = pwm.channel(0, pin='P9', duty_cycle=1.0) # create pwm channel on pin P9 with a duty cycle of 100%
    time.sleep(DOOROPENTIME) # Let the motor run until the door is completely open
    pwm_c_motor = pwm.channel(0, pin='P9', duty_cycle=0.0) # Stop the door when opened

def closeDoor():
    motorGND = Pin('P9', mode=Pin.OUT) # To close the door we switch the motors GND and PWN pins.
    motorGND.value(0) # Now we set P9 as GND and P8 as PWM pin

    pwm_c_motor = pwm.channel(0, pin='P8', duty_cycle=1.0) # create pwm channel on pin P8 with a duty cycle of 100%
    time.sleep(DOORCLOSETIME) # Waiting until the door is fully closed (might be faster then opening the door)
    pwm_c_motor = pwm.channel(0, pin='P8', duty_cycle=0.0) # stopping the motor when door is closed

def setLeds(binaryTuple): # setting leds to 0 or 1 using a tupple containing the binary values with the MSB first and LSB last
    firstLed.value(tup[0]) # Getting the MSB or first value of the tuple
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

# def cleanAndExit(): # Part of the hx711 library wich doesn't work in micropython
#     print("Cleaning...")
#
#     if not EMULATE_HX711:
#         GPIO.cleanup()
#
#     print("Bye!")
#     sys.exit()

## Function doesn't work because used library is python not micropython ##
# def calculateEggs():    # Read out the loadcell to determine the ammount of eggs layed that day
#
#     EMULATE_HX711=False
#
#     referenceUnit = 1
#
#     hx = HX711(4, 5)
#     hx.set_reading_format("MSB", "MSB")
#
#     # HOW TO CALCULATE THE REFFERENCE UNIT
#     # To set the reference unit to 1. Put 1kg on your sensor or anything you have and know exactly how much it weights.
#     # In this case, 92 is 1 gram because, with 1 as a reference unit I got numbers near 0 without any weight
#     # and I got numbers around 184000 when I added 2kg. So, according to the rule of thirds:
#     # If 2000 grams is 184000 then 1000 grams is 184000 / 2000 = 92.
#     #hx.set_reference_unit(113)
#     hx.set_reference_unit(referenceUnit)
#
#     hx.reset()
#
#     hx.tare()
#     try:
#         # Prints the weight. Comment if you're debbuging the MSB and LSB issue.
#         weight = hx.get_weight(4)
#
#         hx.power_down()
#         hx.power_up()
#         time.sleep(0.1)
#
#     except (KeyboardInterrupt, SystemExit):
#         cleanAndExit()
#     eggs = int(weight/60)
#     showEggs(eggs)


openDoor() # chickencoup has to be powered on at the time you want the door to open
           # 16 hours later the door wil close and from that point forward the door will open and close at the same time every day

while True:
    counter = 0 # counts hours to know when to open and close the door and count the eggs
    pycom.heartbeat(False)  # turning off LED from LoPy 4 to save energy
    if machine.wake_reason() == machine.PIN_WAKE: # Checking if lopy was woken up by using switch to open the door
        if p_in() == 1:# p_in(): get value, 0 or 1 (check if switch is toggled to open or close the door)
            openDoor()
        if p_in() == 0:
            closeDoor()

    if counter == 16: # after 16 hours the door closes
        closeDoor()
    if counter == 24: # After 24 hours the door opens again and the ammount of eggs is calculated and shown
        #calculateEggs()
        openDoor()
        counter = 0
    controlClimate()
    counter += 1
    # !Only uncomment the next line when testing phase is complete (when lopy is in deepsleep you can't upload your code to the device)
    #machine.deepsleep(59*60*1000) # Put the machine into deepsleep for 59 mins converted to ms
    # Possible problem with deepsleep on lopy as described in documentation. See following URL
    # https://docs.pycom.io/datasheets/development/lopy/#deep-sleep
