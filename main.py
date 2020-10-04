from machine import PWM
import time

pwm = PWM(0, frequency=5000)  # use PWM timer 0, with a frequency of 5KHz
# create pwm channel on pin P21 with a duty cycle of 50%
pwm_c = pwm.channel(0, pin='P21', duty_cycle=0.5)
time.sleep(2)
pwm_c.duty_cycle(0.3) # change the duty cycle to 30%
