import os
import pika
from dotenv import load_dotenv

load_dotenv()
host = os.getenv('RABBIT_HOST', 'localhost')
puerto = int(os.getenv('RABBIT_PORT', '5672'))
usuario = os.getenv('RABBIT_USER', 'guest')
password = os.getenv('RABBIT_PASS', 'guest')

# Conexión al broker
credentials = pika.PlainCredentials(usuario, password)
conexion = pika.BlockingConnection(pika.ConnectionParameters(
    host=host, 
    port=puerto, 
    credentials=pika.PlainCredentials(usuario, password)
))
canal = conexion.channel()

# Declarar la cola y publicar
canal.queue_declare(queue='hola_mundo')
canal.basic_publish(exchange='', routing_key='hola_mundo', body='¡Hola TP6 desde bash!')

print(" [x] Mensaje enviado al broker")
conexion.close()