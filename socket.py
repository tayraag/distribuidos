import socket
import threading

def reenviar(origen, destino, direccion_log):
    total_bytes = 0
    try:
        # Bucle para copiar bytes de un socket a otro
        while True:
            data = origen.recv(4096)
            if not data:
                break # Si no hay datos, se cortó la conexión
            destino.sendall(data)
            total_bytes += len(data)
    except:
        pass
    finally:
        # El TP pide que el proxy registre (log) cuántos bytes reenvía
        print(f"[{direccion_log}] Transferencia finalizada. Total reenviado: {total_bytes} bytes")
        origen.close()
        destino.close()

def iniciar_proxy():
    # Configuración estática para esta primera prueba
    puerto_escucha = 8080
    backend_host = '127.0.0.1'
    backend_port = 5001

    # 1. Socket del proxy (actúa como Servidor para el cliente)
    proxy_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    proxy_sock.bind(('0.0.0.0', puerto_escucha))
    proxy_sock.listen(5)
    
    print(f"Proxy TCP escuchando en puerto {puerto_escucha}...")
    print(f"Redirigiendo tráfico hacia el backend en {backend_host}:{backend_port}")

    while True:
        # Esperamos que un cliente se conecte al 8080
        client_sock, addr = proxy_sock.accept()
        print(f"\n¡Nuevo cliente conectado desde {addr}!")

        # 2. Socket hacia el backend (actúa como Cliente para tu servidorTCP)
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server_sock.connect((backend_host, backend_port))
        except Exception as e:
            print("El backend está caído. Cerrando conexión con el cliente.")
            client_sock.close()
            continue

        # Creamos dos hilos para copiar los bytes en ambos sentidos simultáneamente
        hilo_c2s = threading.Thread(target=reenviar, args=(client_sock, server_sock, "Cliente -> Servidor"))
        hilo_s2c = threading.Thread(target=reenviar, args=(server_sock, client_sock, "Servidor -> Cliente"))

        hilo_c2s.start()
        hilo_s2c.start()

if __name__ == '__main__':
    iniciar_proxy()