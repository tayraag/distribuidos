import os
from dotenv import load_dotenv

def leer_configuracion():
    # Carga las variables de entorno desde el archivo .env
    load_dotenv()
    
    # Leemos las variables. Si no existen, usamos el segundo parámetro como default razonable.
    server_id = os.getenv('SERVER_ID', '0')
    listen_port = os.getenv('LISTEN_PORT', '5001')
    
    # Imprimimos por salida estándar como pide el TP
    print(f"servidor {server_id}, puerto {listen_port}")
    
    return server_id, int(listen_port)

if __name__ == '__main__':
    leer_configuracion()
