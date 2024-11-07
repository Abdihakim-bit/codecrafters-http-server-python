import socket  # noqa: F401
import threading

CRLF = "\r\n"
response200 = "HTTP/1.1 200 OK"
response404 = "HTTP/1.1 404 Not Found"
contentTypeTxt = "Content-Type: text/plain"
contentLength = "Content-Length: "

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Create a socket server on the local machine to listen on port 4221.
    server_socket = socket.create_server(("localhost", 4221))
    try:
        while True:
            serveOn = server_socket.accept() # wait for client and store their details
            client_thread = threading.Thread(target=handle_client, args=(serveOn[0],)) # Declare a thread invoking the handle client function
            client_thread.daemon = True # Allow the thread to be closed with the program
            client_thread.start()
    except KeyboardInterrupt:
        server_socket.close()
        print("Shutting down server")

def handle_client(client_socket):
    try:
        request = client_socket.recv(1024).decode()
        if request:
            client_socket.send(response(request).encode())
    except Exception as e:
        print("Error handling client: ", e)

    # Parses the user request and returns appropriate response    
def response(request):
    requestParts = request.split(CRLF)
    if (" / " in requestParts[0]):
        response = response200+(CRLF*2)
    elif(" /echo/" in requestParts[0]):
        echoString = requestParts[0].split("/echo/")
        if (echoString[1] is not None):
            text = echoString[1].split(" ")
            response = response200+CRLF+contentTypeTxt+CRLF+contentLength+str(len(text[0]))+""+(CRLF*2)+text[0]
    elif(" /user-agent" in requestParts[0]):
        userAgent = requestParts[2].split(": ") # Split the third line using ":" and store the results in userAgent
        if ("User-Agent" not in userAgent[0]):
            userAgent = requestParts[3].split(": ") # Split the fourth line instead if "User-Agent" is not in userAgent
        if (userAgent[1] is not None):
            print("", userAgent[1])
            response = response200+CRLF+contentTypeTxt+CRLF+contentLength+str(len(userAgent[1]))+""+(CRLF*2)+userAgent[1]
    else:
        response = response404+(CRLF*2)
    return response
if __name__ == "__main__":
    main()
