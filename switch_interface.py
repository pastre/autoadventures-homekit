import socket
from threading import Thread

MESSAGE_DELEGATE = None
HOST = '192.168.100.2'  # Endereco IP do Servidor
PORT = 5000           # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)

def handle_conn(conn):
	msg = conn.recv(1024)
	MESSAGE_DELEGATE(msg)
	
def set_message_delegate(to):
	global MESSAGE_DELEGATE
	MESSAGE_DELEGATE = to

def _start():
	tcp.bind(dest)
	tcp.listen(1)
	print("Listening for connections...")
	while True:
		conn, _ = tcp.accept()
		print("Handling connection")
		Thread(target = handle_conn, args = (conn, )).start()

def start_switch_service() :
	Thread(target = _start).start()
