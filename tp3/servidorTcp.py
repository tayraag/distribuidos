import os
import socket

def leer_configuracion():
    # Código usado en el punto 1.2
    try:
        with open('.env', 'r') as f:
            for linea in f:
                if '=' in linea:
                    clave, valor = linea.strip().split('=', 1)
                    os.environ[clave.strip()] = valor.strip()
    except:
        pass
    
    server_id = os.environ.get('SERVER_ID', '0')
    listen_port = os.environ.get('LISTEN_PORT', '5001')
    return server_id, int(listen_port)

def iniciar_servidor_tcp():
    # 1. Leemos el entorno
    server_id, listen_port = leer_configuracion()
    
    # 2. Creamos el socket TCP (SOCK_STREAM en lugar de SOCK_DGRAM)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # (Opcional) Esto evita el error "Address already in use" si cerrás y abrís rápido
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # 3. Lo vinculamos al puerto
    sock.bind(('0.0.0.0', listen_port))
    
    # 4. LISTEN: Creamos la cola para conexiones entrantes (exclusivo de TCP)
    sock.listen(5)
    print(f"Servidor TCP {server_id} escuchando conexiones en el puerto {listen_port}...")
    
    while True:
        # 5. ACCEPT: El servidor se bloquea acá hasta que un cliente haga el handshake
        conn, addr = sock.accept()
        print(f"¡Conexión establecida con {addr}!")
        
        # 6. Leemos el mensaje del flujo (stream)
        data = conn.recv(1024)
        if data:
            print(f"Servidor {server_id} recibió: '{data.decode('utf-8')}'")
        
        # 7. Cerramos la conexión individual con este cliente
        conn.close()

if __name__ == '__main__':
    iniciar_servidor_tcp()