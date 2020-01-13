import arduino_driver as arduinoDriver

from datetime import datetime
from time import sleep, time_ns

class SwitchManager:

	def __init__(self, lamps, onSwitchChanged):
		self.lampNames = lamps
		self.onSwitchChanged = onSwitchChanged
		self.lastActive = None
		self.lastMessageTimestamp = -100000
#		self.setup()

	def setup(self):
		self.codeToLamp = {pow(2, i + 1) : j for i, j in enumerate(self.lampNames)}
		self.lampStates = {i : False for i in self.lampNames}
		arduinoDriver.setup(self.onMessage)
		print("Configured!!", self.codeToLamp, self.lampStates)

	def onActiveLamp(self, lampName):
		self.lampStates[lampName] = not self.lampStates[lampName]
		self.lastActive = lampName
		print("LampStates are", self.lampStates)
	def actOnLamp(self, activated, timeDelta):
		if self.lastMessageTimestamp == None:
			self.onActiveLamp(activated)
			return
		if self.lastActive == activated:
			if timeDelta > 100:
				print("Timedelta is", timeDelta)
				self.onActiveLamp(activated)
				return
		else:
			self.onActiveLamp(activated)

	def onMessage(self, message):
		if message == '0' : return

		activated = self.codeToLamp[int(message)]

		newTimestamp = time_ns() / 1000000
		timeDelta = newTimestamp - self.lastMessageTimestamp

		self.actOnLamp(activated, timeDelta)

#		print("Got a messsage", message, timeDelta)

		self.lastMessageTimestamp = newTimestamp


manager = SwitchManager(['a', 'b', 'c', 'd'], None)
manager.setup()
while True:
	sleep(1)

