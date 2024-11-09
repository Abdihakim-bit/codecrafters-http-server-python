import socket  # noqa: F401
import threading
import pathlib
import sys
import gzip

currentPath = pathlib.Path().absolute()
CRLF = "\r\n"
response200 = "HTTP/1.1 200 OK"
response201 = "HTTP/1.1 201 Created"
response404 = "HTTP/1.1 404 Not Found"
contentLength = "Content-Length: "

def main():
    try:
        baseDirectory = sys.argv[2]  # Get the directory passed as an argument
    except:
        baseDirectory = str(currentPath)
    server_socket = socket.create_server(("localhost", 4221)) # Create a socket server on the local machine to listen on port 4221.
    print("Server started on port 4221, serving files from " + baseDirectory)
    while True:
        serveOn = server_socket.accept() # wait for client and store their details
        print(f"Accepted connection from {serveOn[1]}")
        client_thread = threading.Thread(target=handle_client, args=(serveOn[0], baseDirectory)) # Declare a thread invoking the handle client function
        client_thread.daemon = True # Allow the thread to be closed with the program
        client_thread.start()

def handle_client(client_socket, baseDirectory):
    try:
        request = client_socket.recv(1024).decode()
        if request:
            res = response(request, baseDirectory)
            if (isinstance(res, bytes)):
                client_socket.send(res)
            else: client_socket.send(res.encode())
    except Exception as e:
        print("Error handling client: ", e)

    # Parses the user request and returns appropriate response    
def response(request, baseDirectory):
    supportedEncoding = ["gzip"]
    contentEncoding = ""
    requestParts = request.split(CRLF)
    for requestLine in requestParts:
        if ("accept-encoding" and "gzip" in requestLine.lower()):
            contentEncoding = "Content-Encoding: " + supportedEncoding[0] + CRLF
    if (" / " in requestParts[0]):
        response = response200+(CRLF*2)
    elif(" /echo/" in requestParts[0]):
        contentType = "Content-Type: text/plain"
        echoString = requestParts[0].split("/echo/")
        if (echoString[1] is not None):
            text = echoString[1].split(" ")
            if (contentEncoding != ""):
                text[0] = gzip.compress(text[0].encode())
                response = (response200+CRLF+contentEncoding+contentType+CRLF+contentLength+str(len(text[0]))+(CRLF*2)).encode()+text[0]
            else: response = response200+CRLF+contentEncoding+contentType+CRLF+contentLength+str(len(text[0]))+(CRLF*2)+text[0]
    elif(" /user-agent" in requestParts[0]):
        contentType = "Content-Type: text/plain"
        x = 1
        while ("user-agent:" not in requestParts[x].lower()):
            x += 1
        userAgent = requestParts[x].split(": ") # Split the request part containing "User-Agent" using ":" and store the results in userAgent
        response = response200+CRLF+contentType+CRLF+contentLength+str(len(userAgent[1]))+(CRLF*2)+userAgent[1]
    elif(" /files/" in requestParts[0]):
        contentType = "Content-Type: application/octet-stream"
        filePath = requestParts[0].split("/files/")[1].split(" ")[0]
        filePath = pathlib.Path(baseDirectory) / filePath  # Construct full path with base directory
        # Write to file if request uses "POST" header 
        if("POST" in requestParts[0]):
            with open(filePath, "w") as file:
                content = file.write(str(requestParts[len(requestParts)-1]))
                response = response201+(CRLF*2)
        # Open file if the filepath exists as is without an extension
        elif filePath.exists():
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
