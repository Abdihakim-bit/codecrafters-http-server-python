import socket  # noqa: F401
import threading
import os
import pathlib
import argparse

files = os.listdir()
CRLF = "\r\n"
response200 = "HTTP/1.1 200 OK"
response404 = "HTTP/1.1 404 Not Found"
contentLength = "Content-Length: "

def main():
    # Parse arguments to get the directory
    args = parse_args()
    baseDirectory = args.directory  # Get the directory passed as an argument
    # Create a socket server on the local machine to listen on port 4221.
    server_socket = socket.create_server(("localhost", 4221))
    print("Server started on port 4221, serving files from " + baseDirectory)

    try:
        while True:
            serveOn = server_socket.accept() # wait for client and store their details
            print(f"Accepted connection from {serveOn[1]}")
            client_thread = threading.Thread(target=handle_client, args=(serveOn[0], baseDirectory)) # Declare a thread invoking the handle client function
            client_thread.daemon = True # Allow the thread to be closed with the program
            client_thread.start()
    except KeyboardInterrupt:
        server_socket.close()
        print("Shutting down server")

def parse_args():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="HTTP server to serve files")
    parser.add_argument("--directory", type=str, default=str(pathlib.Path().absolute()), help="Directory to serve files from")
    return parser.parse_args()

def handle_client(client_socket, baseDirectory):
    try:
        request = client_socket.recv(1024).decode()
        if request:
            client_socket.send(response(request, baseDirectory).encode())
    except Exception as e:
        print("Error handling client: ", e)

    # Parses the user request and returns appropriate response    
def response(request, baseDirectory):
    requestParts = request.split(CRLF)
    if (" / " in requestParts[0]):
        response = response200+(CRLF*2)
    elif(" /echo/" in requestParts[0]):
        contentType = "Content-Type: text/plain"
        echoString = requestParts[0].split("/echo/")
        if (echoString[1] is not None):
            text = echoString[1].split(" ")
            response = response200+CRLF+contentType+CRLF+contentLength+str(len(text[0]))+(CRLF*2)+text[0]
    elif(" /user-agent" in requestParts[0]):
        contentType = "Content-Type: text/plain"
        userAgent = requestParts[2].split(": ") # Split the third line using ":" and store the results in userAgent
        if ("User-Agent" not in userAgent[0]):
            userAgent = requestParts[3].split(": ") # Split the fourth line instead if "User-Agent" is not in userAgent
        if (userAgent[1] is not None):
            response = response200+CRLF+contentType+CRLF+contentLength+str(len(userAgent[1]))+(CRLF*2)+userAgent[1]
    elif(" /files/" in requestParts[0]):
        contentType = "Content-Type: application/octet-stream"
        filePath = requestParts[0].split("/files/")[1].split(" ")[0]
        filePath = pathlib.Path(baseDirectory) / filePath  # Construct full path with base directory
        # Open file if the filepath exists as is without an extension
        if filePath.exists():
            with open(filePath, "r") as file:
                content = file.read()
                response = response200+CRLF+contentType+CRLF+contentLength+str(len(content))+(CRLF*2)+content
        # Call file_exists for files without an extension
        elif file_exists(filePath) != []:
            matching_files = file_exists(filePath)
            if matching_files:
                # If a matching file exists, open and read it
                with open(matching_files[0], "r") as file:
                    content = file.read()
                    response = response200+CRLF+contentType+CRLF+contentLength+str(len(content))+(CRLF*2)+content
        else:
            # If no matching file exists, return 404
            response = response404 + (CRLF*2)
    else:
        response = response404+(CRLF*2)
    return response

# Returns the absolute path of the file in a list if it exists (with any extension), else returns an empty list
def file_exists(requestURI):
    filePath = pathlib.Path(requestURI)
    # Check for files with any extension
    matching_files = list(filePath.parent.glob(filePath.name + ".*"))
    return matching_files
if __name__ == "__main__":
    main()
