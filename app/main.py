import socket  # noqa: F401
import re

CRLF = "\r\n"

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    server_socket = socket.create_server(("localhost", 4221))
    serveOn = server_socket.accept() # wait for client and store their details
    if serveOn is not None:
        request = serveOn[0].recv(1024).decode()
        serveOn[0].send(response(request).encode())

    # Parses the user request and returns appropriate response    
def response(request):
    requestParts = request.split(CRLF)
    if (" / " in requestParts[0]):
        response = "HTTP/1.1 200 OK"+(CRLF*2)
    elif(" /echo/" in requestParts[0]):
        echoString = requestParts[0].split("/echo/")
        if (echoString[1] is not None):
            text = echoString[1].split(" ")
            response = "HTTP/1.1 200 OK"+CRLF+"Content-Type: text/plain"+CRLF+"Content-Length: "+str(len(text[0]))+""+(CRLF*2)+text[0]
    elif(" /user-agent" in requestParts[0]):
        userAgent = requestParts[2].split(": ")
        if ("User-Agent" not in userAgent[0]):
            userAgent = requestParts[3].split(": ")
        if (userAgent[1] is not None):
            print("", userAgent[1])
            response = "HTTP/1.1 200 OK"+CRLF+"Content-Type: text/plain"+CRLF+"Content-Length: "+str(len(userAgent[1]))+""+(CRLF*2)+userAgent[1]
    else:
        response = "HTTP/1.1 404 Not Found"+(CRLF*2)
    return response
if __name__ == "__main__":
    main()
