import serial
from threading import Thread
from multiprocessing import Process, Queue
from time import sleep


port = "/dev/ttyACM0"
baud = 9600

ser = serial.Serial(port, baud)
ser.baudrate = baud

def read_serial():
	while True:
		try:
			message = ser.read()
			m1 = message.decode('utf-8')
			print("Got a message!", m1)
		except UnicodeDecodeError as e:
			print('-------------------------------------------', e)
			input()
			exit()
read_serial()
