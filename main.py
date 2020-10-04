from machine import PWM
from machine import Pin
import time

p_out = Pin('P22', mode=Pin.OUT)
p_out.value(0)

pwm = PWM(0, frequency=5000)  # use PWM timer 0, with a frequency of 5KHz
# create pwm channel on pin P21 with a duty cycle of 50%
pwm_c = pwm.channel(0, pin='P21', duty_cycle=0.2)
time.sleep(3)
pwm_c.duty_cycle(0.5) # change the duty cycle to 50%
time.sleep(3)
pwm_c.duty_cycle(0.3) # change the duty cycle to 30%
time.sleep(3)
pwm_c.duty_cycle(0.0) # change the duty cycle to 30%

p_out = Pin('P21', mode=Pin.OUT)
p_out.value(0)

pwm = PWM(0, frequency=5000)  # use PWM timer 0, with a frequency of 5KHz
# create pwm channel on pin P21 with a duty cycle of 50%
pwm_c = pwm.channel(0, pin='P22', duty_cycle=0.2)
time.sleep(3)
pwm_c.duty_cycle(0.5) # change the duty cycle to 50%
time.sleep(3)
pwm_c.duty_cycle(0.3) # change the duty cycle to 30%
time.sleep(3)
pwm_c.duty_cycle(0.0) # change the duty cycle to 30%
