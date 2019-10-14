"""An example of how to setup and start an Accessory.

This is:
1. Create the Accessory object you want.
2. Add it to an AccessoryDriver, which will advertise it on the local network,
    setup a server to answer client queries, etc.
"""
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
    """Call this method to get a Bridge instead of a standalone accessory."""
    bridge = Bridge(driver, 'Bridge')
    # temp_sensor = TemperatureSensor(driver, 'Sensor 2')
    # temp_sensor2 = TemperatureSensor(driver, 'Sensor 1')
    # bridge.add_accessory(temp_sensor)
    # bridge.add_accessory(temp_sensor2)
    for lName in lampNames:
        lamp = Lamp(driver, lName)
        bridge.add_accessory(lamp)
    return bridge


def get_accessory(driver):
    """Call this method to get a standalone Accessory."""
    return TemperatureSensor(driver, 'MyTempSensor')


# Start the accessory on port 51826
driver = AccessoryDriver(port=51826)

# Change `get_accessory` to `get_bridge` if you want to run a Bridge.
driver.add_accessory(accessory=get_bridge(driver))

# We want SIGTERM (terminate) to be handled by the driver itself,
# so that it can gracefully stop the accessory, server and advertising.
signal.signal(signal.SIGTERM, driver.signal_handler)

# Start it!
driver.start()
