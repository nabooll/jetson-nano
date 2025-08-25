from bottle import route, run, template, request        #make sure bottle is installed

import Jetson.GPIO as GPIO

import time

# pi 26 = Jetson 12
# pi 24 = Jetson 15
# pi 12 = Jetson 168
# pi 13 = Jetson 38

GPIO.setmode(GPIO.BCM)                                  #GPIO BCM pin layout
channels = [26, 24, 12, 13]
GPIO.setup(channels, GPIO.OUT)

dir1 = 26                                               #direction 1 pin

dir2 = 24                                               #direction 2 pin

pwm1 = 12                                               #pwm 1 pin

pwm2 = 13                                               #pwm 2 pin

#the above pins are reserved by the HAT

frequency = 20000                                       #pwm frequency

duty = 0                                                #pwm duty cycle 0 to 100

specialdelay = 2                                        #delay time for special moves

GPIO.setup(dir1, GPIO.OUT)                              #set pins as GPIO outputs

GPIO.setup(dir2, GPIO.OUT)

GPIO.setup(pwm1, GPIO.OUT)

GPIO.setup(pwm2, GPIO.OUT)

pwmout1 = GPIO.PWM(pwm1, frequency)                     #set pwm1 as pwm output

pwmout2 = GPIO.PWM(pwm2, frequency)                     #set pwm2 as pwm output

pwmout1.start(duty)                                     #initializing pwm

pwmout2.start(duty)

@route('/')                                             #root page on browser

def index():

        return template('main.tpl')

@route('/1')                                            #speed level 1 button

def index():

        global duty

        duty = 5

        pwmout1.ChangeDutyCycle(duty)

        pwmout2.ChangeDutyCycle(duty)

        return template('main.tpl')                     #return to main page after button pressed

@route('/2')                                            #speed level 2 button

def index():

        global duty

        duty = 10

        pwmout1.ChangeDutyCycle(duty)

        pwmout2.ChangeDutyCycle(duty)

        return template('main.tpl')

@route('/3')                                            #speed level 3 button

def index():

        global duty

        duty = 15

        pwmout1.ChangeDutyCycle(duty)

        pwmout2.ChangeDutyCycle(duty)

        return template('main.tpl')

@route('/4')                                            #speed level 4 button

def index():

        global duty

        duty = 20

        pwmout1.ChangeDutyCycle(duty)

        pwmout2.ChangeDutyCycle(duty)

        return template('main.tpl')

@route('/5')                                            #speed level 5 button

def index():

        global duty

        duty = 25

        pwmout1.ChangeDutyCycle(duty)

        pwmout2.ChangeDutyCycle(duty)

        return template('main.tpl')

@route('/forward')                                      #forward button

def index():

        pwmout1.ChangeDutyCycle(duty)

        pwmout2.ChangeDutyCycle(duty)

        GPIO.output(dir1, 1)

        GPIO.output(dir2, 1)

        return template('main.tpl')

@route('/left')                                         #rotate left button

def index():

        pwmout1.ChangeDutyCycle(duty)

        pwmout2.ChangeDutyCycle(duty)

        GPIO.output(dir1, 0)

        GPIO.output(dir2, 1)

        return template('main.tpl')

@route('/right')                                        #rotate right button

def index():

        pwmout1.ChangeDutyCycle(duty)

        pwmout2.ChangeDutyCycle(duty)

        GPIO.output(dir1, 1)

        GPIO.output(dir2, 0)

        return template('main.tpl')

@route('/reverse')                                      #reverse button

def index():

        pwmout1.ChangeDutyCycle(duty)

        pwmout2.ChangeDutyCycle(duty)

        GPIO.output(dir1, 0)

        GPIO.output(dir2, 0)

        return template('main.tpl')

@route('/stop')                                         #stop button

def index():

        pwmout1.ChangeDutyCycle(0)

        pwmout2.ChangeDutyCycle(0)

        return template('main.tpl')

@route('/tornado')                                      #tornado move

def index():

        pwmout1.ChangeDutyCycle(100)

        pwmout2.ChangeDutyCycle(100)

        GPIO.output(dir1, 1)

        GPIO.output(dir2, 0)

        time.sleep(specialdelay)                        #you may tweak time of spinning from top of page

        GPIO.output(dir1, 0)

        GPIO.output(dir2, 1)

        time.sleep(specialdelay)

        pwmout1.ChangeDutyCycle(0)

        pwmout2.ChangeDutyCycle(0)

        return template('main.tpl')

@route('/ramp')                                         #ramp special move

def index():

        pwmout1.ChangeDutyCycle(duty)                   #back up with set speed level

        pwmout2.ChangeDutyCycle(duty)

        GPIO.output(dir1, 0)

        GPIO.output(dir2, 0)

        time.sleep(specialdelay)

        GPIO.output(dir1, 1)

        GPIO.output(dir2, 1)

        pwmout1.ChangeDutyCycle(100)                    #forward with full speed

        pwmout2.ChangeDutyCycle(100)

        time.sleep(specialdelay)

        pwmout1.ChangeDutyCycle(0)

        pwmout2.ChangeDutyCycle(0)

        return template('main.tpl')

try:

        run(host='192.168.1.35', port=80)               #be sure to put your pi's ip address here

finally:

        GPIO.cleanup()                                  #clear all GPIO's before terminating
