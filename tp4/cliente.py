import grpc

import temperaturas_pb2
import temperaturas_pb2_grpc

def run():
    canal = grpc.insecure_channel('localhost:50051')
    stub = temperaturas_pb2_grpc.ServicioTemperaturasStub(canal)

    ciudad = input('Ingrese el código de la ciudad: ').strip().upper()
    request = temperaturas_pb2.CodigoCiudad(codigo=ciudad)
    respuesta = stub.ObtenerUltimasTemperaturas(request)

    if not respuesta.temperaturas:
        print(f'No hay temperaturas registradas para la ciudad {ciudad}.')
        return

    print(f'Últimas 5 temperaturas de {ciudad}:')
    for temp in respuesta.temperaturas:
        print(f'- {temp.valor}°C  |  timestamp: {temp.timestamp}')

if __name__ == '__main__':
    run()
