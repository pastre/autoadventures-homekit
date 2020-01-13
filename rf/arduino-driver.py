import serial
from threading import Thread
from multiprocessing import Process, Queue
from time import sleep


port = "/dev/ttyACM0"
baud = 9600

ser = serial.Serial(port, baud)
ser.baudrate = baud

messages = Queue()

def parse_message(message):
	try:
		message = message.decode('utf-8')
		toRecebendo, ending = message.split(' - ')
		value = toRecebendo.split(' ')[-1]
		if int(ending) == 0: return
		print(value, toRecebendo.split(' ' )[-1], ending)
	except Exception as e:
		pass
#		print("Deu ruim!", e)
def read_serial(callback):
	while True:
		message = ser.readline()
		callback(message)


def setup(callback):
	Thread(target = read_serial, args = (callback, ) ).start()

setup(parse_message)

while True:
	sleep(1)
