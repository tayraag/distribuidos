
import sys
import time
from conexion import conectar, COLA, NOMBRE

nombre = sys.argv[1] if len(sys.argv) > 1 else NOMBRE

conexion = conectar()
canal = conexion.channel()

canal.queue_declare(queue=COLA, durable=True)

# Reparto justo de tareas
canal.basic_qos(prefetch_count=1)

def procesar(canal, metodo, propiedades, cuerpo):
    tarea = cuerpo.decode("utf-8")

    print(f"[{nombre}] Comenzando: {tarea}", flush=True)

    # Cada punto representa un segundo
    duracion = tarea.count(".")
    time.sleep(duracion)

    # Confirmar después de procesar
    canal.basic_ack(delivery_tag=metodo.delivery_tag)

    print(f"[{nombre}] Terminada: {tarea}", flush=True)

canal.basic_consume(
    queue=COLA,
    on_message_callback=procesar,
    auto_ack=False
)

print(f"[{nombre}] Esperando tareas en '{COLA}'.")

try:
    canal.start_consuming()

except KeyboardInterrupt:
    print(f"\n[{nombre}] Cerrando.")

finally:
    if conexion.is_open:
        conexion.close()
