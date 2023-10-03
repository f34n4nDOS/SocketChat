import tkinter as tk
import socket

# Configuración del cliente
host = '127.0.0.1'
port = 12345

def get_server_response(request):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        client_socket.send(request.encode('utf-8'))
        response = client_socket.recv(4096).decode('utf-8')
    return response

def show_system_info():
    response = get_server_response('system_info')
    result_text.delete('1.0', tk.END)  # Limpiar el texto anterior
    result_text.insert(tk.END, response)

# Crear la ventana principal
root = tk.Tk()
root.title('Consulta de Características del Sistema')

# Botón para obtener información del sistema
info_button = tk.Button(root, text='Obtener Información del Sistema', command=show_system_info)
info_button.pack()

# Área de texto para mostrar resultados
result_text = tk.Text(root, wrap=tk.WORD)
result_text.pack()

root.mainloop()
