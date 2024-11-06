import socket  # noqa: F401


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221))
    serveOn = server_socket.accept() # wait for client and store their details
    response = "HTTP/1.1 200 OK\r\n\r\n"
    if serveOn is not None:
        print("",serveOn[1])
        serveOn[0].send(response.encode())

if __name__ == "__main__":
    main()
