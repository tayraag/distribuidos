import socket 

def enviar_mensajes():
	mensaje = "Hola desde el cliente UDP"

	servidores = [
		('10.0.2.1', 5001),
		('10.0.2.2', 5002),
		('10.0.2.3', 5003)
	]

	sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	for ip, puerto in servidores:
		print(f"Enviando mensaje a {ip}:{puerto}...")
		sock.sendto(mensaje.encode('utf-8'), (ip,puerto))

if __name__ == '__main__':
	enviar_mensajes()
