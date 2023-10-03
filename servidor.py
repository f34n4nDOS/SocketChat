import socket
import threading

# Configuración del servidor
host = 'xxx.xxx.x.xx'
port = 49999

# Crear un socket del servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lista de clientes conectados y sus nombres
clients = {}
client_lock = threading.Lock()



def broadcast(message, sender_name):
    with client_lock:
        for client_socket, client_name in clients.items():
            if client_name != sender_name:
                try:
                    client_socket.send(message.encode('utf-8'))
                except:
                    # Eliminar el cliente si la conexión está rota
                    del clients[client_socket]

def handle_messages(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message, client)
        except:
            index = clients.index(client)
            username = usernames[index]
            broadcast(f"El usuario: {username} se ha desconectado.".encode('utf-8'), client)
            clients.remove(client)
            usernames.remove(username)
            client.close()
            break
            
            
def handle_client(client_socket):
    client_name = client_socket.recv(1024).decode('utf-8')
    with client_lock:
        clients[client_socket] = client_name
    broadcast(f'{client_name} se ha unido al chat.\n', client_name)

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            broadcast(f'{client_name}: {message}', client_name)
        except:
            # Eliminar el cliente si la conexión está rota
            del clients[client_socket]
            break

    broadcast(f'{client_name} se ha desconectado.\n', client_name)
    with client_lock:
        del clients[client_socket]
    client_socket.close()

def main():
    print(f"Servidor de chat en funcionamiento en {host}:{port}")

    while True:
        client_socket, client_address = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()
        
        

if __name__ == "__main__":
    main()
