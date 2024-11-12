from .response_handler import response

# Receive the client's request, decode it and send appropriate response
def handle_client(client_socket, base_directory):
    try:
        request = client_socket.recv(1024).decode()
        if request:
            res = response(request, base_directory)
            # Send the response, encoding it to bytes if necessary
            client_socket.send(res.encode() if isinstance(res, str) else res)
    except Exception as e:
        print("Error handling client:", e)
    finally:
        client_socket.close()