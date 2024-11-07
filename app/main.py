import socket  # noqa: F401
import threading
import os
import pathlib

files = os.listdir()
CRLF = "\r\n"
response200 = "HTTP/1.1 200 OK"
response404 = "HTTP/1.1 404 Not Found"
contentLength = "Content-Length: "

def main():
    # Create a socket server on the local machine to listen on port 4221.
    server_socket = socket.create_server(("localhost", 4221))
    print("Server started on port 4221")
    try:
        while True:
            serveOn = server_socket.accept() # wait for client and store their details
            print(f"Accepted connection from {serveOn[1]}")
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
        contentType = "Content-Type: text/plain"
        echoString = requestParts[0].split("/echo/")
        if (echoString[1] is not None):
            text = echoString[1].split(" ")
            response = response200+CRLF+contentType+CRLF+contentLength+str(len(text[0]))+""+(CRLF*2)+text[0]
    elif(" /user-agent" in requestParts[0]):
        contentType = "Content-Type: text/plain"
        userAgent = requestParts[2].split(": ") # Split the third line using ":" and store the results in userAgent
        if ("User-Agent" not in userAgent[0]):
            userAgent = requestParts[3].split(": ") # Split the fourth line instead if "User-Agent" is not in userAgent
        if (userAgent[1] is not None):
            response = response200+CRLF+contentType+CRLF+contentLength+str(len(userAgent[1]))+""+(CRLF*2)+userAgent[1]
    elif(" /files/" in requestParts[0]):
        contentType = "Content-Type: application/octet-stream"
        filePath = requestParts[0].split("/files/")[1].split(" ")[0].split("/")
        path = str(pathlib.Path().absolute())
        directory = ""
        for index , dir in enumerate(filePath):
            if (index != len(filePath)-1 and dir_exists(directory)):
                path = path + "\\" + dir
            elif (index == len(filePath)-1 and file_exists(path + "\\" + dir) != []):
                file = open(file_exists(path + "\\" + dir)[0], "r")
                content = file.read()
                file.close()
                response = response200+CRLF+contentType+CRLF+contentLength+str(len(content))+""+(CRLF*2)+content
            elif (index == len(filePath)-1 and file_exists(path) == []):
                response = response404+(CRLF*2)
            elif (index != len(filePath)-1 and not dir_exists(directory)):
                response = response404+(CRLF*2)
                break
    else:
        response = response404+(CRLF*2)
    return response
# returns True if directory exists, else False
def dir_exists(directory):
    try:
        if (os.listdir(directory)): return True
    except Exception:
        return False
# returns the absolute path of the file in a list if it exists, else returns an empty list
def file_exists(requestURI):
    filePath = pathlib.Path(requestURI)
    return (list(filePath.parent.glob(filePath.name + ".*")))
if __name__ == "__main__":
    main()
