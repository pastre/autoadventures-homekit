import logging
import signal
import random

from pyhap.accessory import Accessory, Bridge
from pyhap.accessory_driver import AccessoryDriver
import pyhap.loader as loader
import communication as com
from time import sleep
from switch_interface import set_message_delegate, start_switch_service

logging.basicConfig(level=logging.INFO, format="[%(module)s] %(message)s")

lampNames = [
	"Luz da cozinha",
	"Luz da sala",
	"Luz do banheiro",
	"Luz do quarto"
]

class Lamp(Accessory):
	def __init__(self, driver, displayName):
		super().__init__(driver, displayName)
		self.displayName = displayName
		serv_light = self.add_preload_service('Lightbulb')
		self.char_on = serv_light.configure_char('On', setter_callback=self.setBulb)
		
	def setBulb(self, value):
		print('value is', value)
		com.update(self.displayName, value == 1)
		print(self.char_on)
	
	def flipBulb(self):
		v  = int(not bool(self.char_on.value))
		print("Flipei", self.displayName, v)
		self.char_on.set_value(value = v)
		self.setBulb(v)
		

def get_bridge(driver):
    bridge = Bridge(driver, 'Bridge')
    for lName in lampNames:
        lamp = Lamp(driver, lName)
        bridge.add_accessory(lamp)
    return bridge


# Start the accessory on port 51826
driver = AccessoryDriver(port=51826)
myBridge = get_bridge(driver)
driver.add_accessory(accessory=myBridge)
signal.signal(signal.SIGTERM, driver.signal_handler)

def message_delegate(message):
	asStr = str(message, 'utf-8')
	for _, accessory in myBridge.accessories.items():
		if accessory.display_name == asStr:
			accessory.flipBulb()


#set_message_delegate(message_delegate)
#start_switch_service()

# Start it!
driver.start()

while True:
	sleep(1)
