import os
import pika
from dotenv import load_dotenv

load_dotenv()
host = os.getenv('RABBIT_HOST', 'localhost')
puerto = int(os.getenv('RABBIT_PORT', '5672'))
usuario = os.getenv('RABBIT_USER', 'guest')
password = os.getenv('RABBIT_PASS', 'guest')

credentials = pika.PlainCredentials(usuario, password)
conexion = pika.BlockingConnection(pika.ConnectionParameters(host=host, credentials=credentials))
canal = conexion.channel()

canal.queue_declare(queue='hola_mundo')

def callback(ch, method, properties, body):
    print(f" [x] Mensaje procesado: {body.decode()}")

canal.basic_consume(queue='hola_mundo', on_message_callback=callback, auto_ack=True)

print(' [*] Esperando mensajes en la cola. Presioná CTRL+C para salir.')
canal.start_consuming()

conexion = pika.BlockingConnection(pika.ConnectionParameters(
    host=host, 
    port=puerto, 
    credentials=pika.PlainCredentials(usuario, password)
))