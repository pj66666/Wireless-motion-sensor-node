
import time
import Adafruit_PCA9685
pwm = Adafruit_PCA9685.PCA9685()

servo_min = 150
servo_max = 600

def set_servo_angle(channel,angle):
    angle=4096*((angle*11)+500)/20000
    pwm.set_pwm(channel,0,int(angle))

pwm.set_pwm_freq(50)


set_servo_angle(6,90)
time.sleep(2)

# set_servo_angle(0,90)
# time.sleep(2)

# set_servo_angle(15,90)
# time.sleep(2)
