import socket
import os

def iniciar_servidor():
	server_id=os.environ.get('SERVER_ID','0')
	listen_port=int(os.environ.get('LISTEN_PORT','5001'))

	sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

	sock.bind(('0.0.0.0', listen_port))
	print(f"servidor {server_id} escuchando en el puerto {listen_port}...")

	while True:
		data, addr = sock.recvfrom(1024)
		mensaje = data.decode('utf-8')
		print(f"Servidor {server_id} recibio: '{mensaje}' desde {addr}")

if __name__ == '__main__':
	iniciar_servidor()
