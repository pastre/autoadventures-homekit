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
		return message.replace('\r\n', '')
		toRecebendo, ending = message.split(' - ')
		value = toRecebendo.split(' ')[-1]
		print("Parsed", value, toRecebendo.split(' ' )[-1], ending)
		if int(ending) == 0: return
		return ending
	except Exception as e:
		print("Deu ruim!", e, message)
def read_serial(callback):
	while True:
#		message = ser.readline()
		message = ser.read()
		parsedValue = parse_message(message)
		if parsedValue == None: return
		callback(parsedValue)


def setup(callback):
	Thread(target = read_serial, args = (callback, ) ).start()

#setup(parse_message)

#while True:
#	sleep(1)
