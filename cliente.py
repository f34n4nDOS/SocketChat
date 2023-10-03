import tkinter as tk
import socket
import threading

# Configuración del cliente
host = 'xxx.xxx.x.xx'
port = 49999

# Crear un socket del cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

# Ventana principal
root = tk.Tk()
root.title('Chat App')

# Campo para ingresar el nombre del cliente
name_label = tk.Label(root, text='Nombre:')
name_label.pack()
name_entry = tk.Entry(root)
name_entry.pack()

# Campo para ingresar mensajes
message_label = tk.Label(root, text='Mensaje:')
message_label.pack()
message_entry = tk.Entry(root)
message_entry.pack()

# Ventana de chat
chat_text = tk.Text(root)
chat_text.pack()

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            chat_text.insert(tk.END, message + '\n')
            chat_text.see(tk.END)
        except:
            break

def send_message(event=None):
    message = message_entry.get()
    if message:
        client_socket.send(message.encode('utf-8'))
        message_entry.delete(0, tk.END)

def join_chat(event=None):
    name = name_entry.get()
    if name:
        client_socket.send(name.encode('utf-8'))
        name_entry.config(state=tk.DISABLED)
        join_button.config(state=tk.DISABLED)
        message_entry.config(state=tk.NORMAL)
        send_button.config(state=tk.NORMAL)
        receive_thread = threading.Thread(target=receive_messages)
        receive_thread.start()

join_button = tk.Button(root, text='Unirse al chat', command=join_chat)
join_button.pack()

send_button = tk.Button(root, text='Enviar', command=send_message, state=tk.DISABLED)
send_button.pack()

message_entry.bind('<Return>', send_message)

root.mainloop()
