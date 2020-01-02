import requests

def make_lamp(ip, name):
	return {
		"ip": ip,
		"name": "Luz d" + name
	}
LAMPS = [
	make_lamp(2, "a cozinha"),
	make_lamp(3, "o banheiro"),
	make_lamp(4, "o quarto"),
	make_lamp(5, "a sala"),
]

ligados = []

def update(lampName, to):
	print("Updating", lampName)
	print("Lamps are", LAMPS)
	for lamp in LAMPS:
		if lamp['name'] == lampName:
			url = "http://192.168.5." + str(lamp['ip']) + "/update"
			if to and (not lampName in ligados):
				ligados.append(lampName)
				requests.get(url)
			elif (not to) and (lampName in ligados):
				ligados.remove(lampName)
				requests.get(url)
			print("Atualizei a", lamp['name'])
			return
	print("passou reto")
