import grpc
from concurrent import futures

import temperaturas_pb2
import temperaturas_pb2_grpc

# Datos de ejemplo por ciudad
TEMPERATURAS = {
    "CBA": [22.1, 23.4, 21.9, 20.5, 19.7],
    "MDZ": [18.0, 17.6, 17.9, 18.5, 19.2],
    "ROS": [24.1, 24.7, 25.2, 25.8, 26.0],
}

class ServicioTemperaturasImpl(temperaturas_pb2_grpc.ServicioTemperaturasServicer):
    def ObtenerUltimasTemperaturas(self, request, context):
        codigo = request.codigo.strip().upper()
        valores = TEMPERATURAS.get(codigo, [])

        # En la práctica, se devolverían las últimas 5 temperaturas.
        # Como hay un diccionario fijo, tomamos el máximo de 5.
        temperaturas = [
            temperaturas_pb2.Temperatura(
                valor=valor,
                timestamp=1700000000 + i
            )
            for i, valor in enumerate(valores[:5])
        ]

        return temperaturas_pb2.RespuestaTemperaturas(temperaturas=temperaturas)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    temperaturas_pb2_grpc.add_ServicioTemperaturasServicer_to_server(
        ServicioTemperaturasImpl(),
        server,
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor escuchando en el puerto 50051...")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
