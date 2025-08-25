import Jetson.GPIO as GPIO
import time

PIN_PWM = 33
FREKUENSI = 1000
NILAI_PWM = 128

GPIO.setmode(GPIO.Board)
GPIO.setup(PIN_PWM, GPIO.OUT)

pwm = GPIO.PWM(PIN_PWM, FREKUENSI)
pwm.start(0)

try:
	duty_cycle = (NILAI_PWM / 255 ) * 100
	pwm.ChangeDutyCycle(duty_cycle)
	print("Ctrl-C untuk berhenti")
	
	while True:
		time.sleep(1)

except KeyboardInterrupt:
	print("\nProgram Dihentikan")

finally:
	pwm.stop()
	GPIO.cleanup()
	print("PWM Stop, GPIO dibersihkan")
