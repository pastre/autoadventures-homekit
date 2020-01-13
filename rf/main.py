from RPi import GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
gpioPin = 27
GPIO.setup([gpioPin, 11], GPIO.IN)
last = 0
while True:
	try:
		sleep(0.01)

		r1 = GPIO.input(gpioPin)
#	r2= GPIO.input(11)
#	if r1 == last: continue
#	last = r1
		print("Trocou! Agora eh ", last)
	except:
		GPIO.cleanup()
		exit()
#	if r1 == 1 : print("ZEROU BRO")
#	print("Read", r1, r2, "from pin 11 gpio 17")



