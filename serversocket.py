import socket
import platform
import os
import psutil
import threading

# Configuración del servidor
host = '127.0.0.1'
port = 12345

def get_system_info():
    system_info = {
        'Plataforma': platform.system(),
        'Versión del SO': platform.version(),
        'Procesador': platform.processor(),
        'Memoria RAM (GB)': round(psutil.virtual_memory().total / (1024 ** 3), 2),
        'Estado del Disco': psutil.disk_usage('/').percent,
        'Filesystem': ', '.join(partition.device for partition in psutil.disk_partitions()),
        'Promedio de Carga': ', '.join(map(str, os.getloadavg())),
        'Particiones': ', '.join(partition.device for partition in psutil.disk_partitions()),
        'Interfaces de Red': ', '.join(psutil.net_if_addrs().keys()),
        'Procesos en Ejecución': ', '.join(p.info['name'] for p in psutil.process_iter(attrs=['name']))
    }
    return system_info

def handle_client(client_socket):
    request = client_socket.recv(1024).decode('utf-8')

    if request == 'system_info':
        system_info = get_system_info()
        response = str(system_info)
        client_socket.send(response.encode('utf-8'))

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)

    print(f"Servidor en funcionamiento en {host}:{port}")

    while True:
        client_socket, client_address = server.accept()
        print(f"Conexión entrante de {client_address[0]}:{client_address[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == '__main__':
    main()
