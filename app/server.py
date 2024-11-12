import socket
import threading
from .client_handler import handle_client

def start_server(base_directory):
    server_socket = socket.create_server(("localhost", 4221))
    print(f"Server started on port 4221, serving files from {base_directory}")
    
    # Continuously accept and handle incoming client connections by creating a thread for each user
    while True:
        client_socket, address = server_socket.accept()
        print(f"Accepted connection from {address}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket, base_directory))
        client_thread.daemon = True
        client_thread.start()