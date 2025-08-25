import Jetson.GPIO as GPIO
import time

PIN_PWM = 33
FREKUENSI = 1000
NILAI_PWM = 128

GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN_PWM, GPIO.OUT)

pwm = GPIO.PWM(PIN_PWM, FREKUENSI)
pwm.start(0)

try:
	print("Ctrl-C untuk berhenti")
	
	while True:
		for duty in range(0,101,1):
			pwm.ChangeDutyCycle(duty)
			#print(duty)
			time.sleep(0.02)
			
		for duty in range(100,-1,-1):
			pwm.ChangeDutyCycle(duty)
			#print(duty)
			time.sleep(0.02)
			

except KeyboardInterrupt:
	print("\nProgram Dihentikan")

finally:
	pwm.stop()
	GPIO.cleanup()
	print("PWM Stop, GPIO dibersihkan")
