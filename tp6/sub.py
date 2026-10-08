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

canal.exchange_declare(exchange='bolsa_ex', exchange_type='topic')

# Cola temporal exclusiva para este suscriptor
resultado = canal.queue_declare(queue='', exclusive=True)
nombre_cola = resultado.method.queue

patrones = sys.argv[1:]
if not patrones:
    sys.stderr.write("Uso: %s [patrón]...\n" % sys.argv[0])
    sys.exit(1)

# Atamos la cola al exchange por cada patrón
for patron in patrones:
    canal.queue_bind(exchange='bolsa_ex', queue=nombre_cola, routing_key=patron)

print(f" [*] Esperando eventos para: {patrones}. CTRL+C para salir.")

def callback(ch, method, properties, body):
    print(f" [x] Recibido de {method.routing_key}: {body.decode()}")

canal.basic_consume(queue=nombre_cola, on_message_callback=callback, auto_ack=True)
canal.start_consuming()