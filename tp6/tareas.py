
import sys
import pika
from conexion import conectar, COLA, NOMBRE

conexion = conectar()
canal = conexion.channel()

canal.queue_declare(queue=COLA, durable=True)
canal.confirm_delivery()

cantidad = int(sys.argv[1]) if len(sys.argv) > 1 else 10

try:
    for i in range(1, cantidad + 1):
        puntos = "." * ((i % 3) + 1)
        mensaje = f"{NOMBRE}: Tarea {i} {puntos}"

        canal.basic_publish(
            exchange="",
            routing_key=COLA,
            body=mensaje.encode("utf-8"),
            properties=pika.BasicProperties(
                delivery_mode=2
            ),
            mandatory=True
        )

        print(f"[x] Enviada: {mensaje}")

finally:
    conexion.close()
