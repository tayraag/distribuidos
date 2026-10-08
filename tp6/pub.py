import os
import sys
import pika
from dotenv import load_dotenv

load_dotenv()
host = os.getenv('RABBIT_HOST', 'localhost')
puerto = int(os.getenv('RABBIT_PORT', '5672'))
usuario = os.getenv('RABBIT_USER', 'guest')
password = os.getenv('RABBIT_PASS', 'guest')

conexion = pika.BlockingConnection(pika.ConnectionParameters(
    host=host, port=puerto, credentials=pika.PlainCredentials(usuario, password)
))
canal = conexion.channel()

# Declaramos el exchange de tipo 'topic'
canal.exchange_declare(exchange='bolsa_ex', exchange_type='topic')

# Tomamos el tópico y el mensaje de los argumentos de la consola
routing_key = sys.argv[1] if len(sys.argv) > 1 else 'stock.desconocido'
mensaje = ' '.join(sys.argv[2:]) or 'Cotización vacía'

canal.basic_publish(exchange='bolsa_ex', routing_key=routing_key, body=mensaje)
print(f" [x] Evento publicado: {routing_key} -> {mensaje}")

conexion.close()