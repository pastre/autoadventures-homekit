import logging
import signal
import random

from pyhap.accessory import Accessory, Bridge
from pyhap.accessory_driver import AccessoryDriver
import pyhap.loader as loader
import communication as com

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
		com.update(self.displayName)


def get_bridge(driver):
    bridge = Bridge(driver, 'Bridge')
    for lName in lampNames:
        lamp = Lamp(driver, lName)
        bridge.add_accessory(lamp)
    return bridge


# Start the accessory on port 51826
driver = AccessoryDriver(port=51826)
driver.add_accessory(accessory=get_bridge(driver))
signal.signal(signal.SIGTERM, driver.signal_handler)

# Start it!
driver.start()
