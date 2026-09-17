import socket
import threading
import itertools

backends = [
    ('10.0.2.2', 5002), # sdist1
    ('10.0.2.3', 5003)  # sdist2
]
balanceador = itertools.cycle(backends) # Algoritmo Round-Robin

def reenviar(origen, destino, log_tag):
    total = 0
    try:
        while True:
            data = origen.recv(4096)
            if not data: 
                break
            destino.sendall(data)
            total += len(data)
    except:
        pass
    print(f"[{log_tag}] Transferidos: {total} bytes")
    origen.close()
    destino.close()

def iniciar_proxy():
    puerto = 8080
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', puerto))
    s.listen(5)
    print(f"Proxy Balanceador escuchando en el puerto {puerto}...")

    while True:
        c_sock, addr = s.accept()
        
        # Round-Robin: Pedimos el siguiente servidor de la lista
        b_ip, b_port = next(balanceador)
        print(f"\nNuevo cliente {addr}. Redirigiendo a backend {b_ip}:{b_port}")
        
        b_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            b_sock.connect((b_ip, b_port))
            # Hilos para copiar bytes en ambos sentidos
            threading.Thread(target=reenviar, args=(c_sock, b_sock, "C->S")).start()
            threading.Thread(target=reenviar, args=(b_sock, c_sock, "S->C")).start()
        except:
            print("Error: Backend caído.")
            c_sock.close()

if __name__ == '__main__':
    iniciar_proxy()