import pathlib
import gzip
from utils import file_exists

CRLF = "\r\n"
response200 = "HTTP/1.1 200 OK"
response201 = "HTTP/1.1 201 Created"
response404 = "HTTP/1.1 404 Not Found"
contentLength = "Content-Length: "

def response(request, base_directory):
    supported_encoding = ["gzip"]
    request_parts = request.split(CRLF)
    content_encoding = ""
    
    for line in request_parts:
        if "accept-encoding" in line.lower() and "gzip" in line.lower():
            content_encoding = "Content-Encoding: gzip" + CRLF
            
    if " / " in request_parts[0]:
        return response200 + (CRLF * 2)
    elif " /echo/" in request_parts[0]:
        return handle_echo(request_parts, content_encoding)
    elif " /user-agent" in request_parts[0]:
        return handle_user_agent(request_parts)
    elif " /files/" in request_parts[0]:
        return handle_file_request(request_parts, base_directory, content_encoding)
    return response404 + (CRLF * 2)

def handle_echo(request_parts, content_encoding):
    content_type = "Content-Type: text/plain"
    echo_string = request_parts[0].split("/echo/")[1].split(" ")[0]
    content = gzip.compress(echo_string.encode()) if content_encoding else echo_string
    return response200 + CRLF + content_encoding + content_type + CRLF + contentLength + str(len(content)) + (CRLF * 2) + content

def handle_user_agent(request_parts):
    content_type = "Content-Type: text/plain"
    user_agent = next(line for line in request_parts if "user-agent:" in line.lower()).split(": ")[1]
    return response200 + CRLF + content_type + CRLF + contentLength + str(len(user_agent)) + (CRLF * 2) + user_agent

def handle_file_request(request_parts, base_directory, content_encoding):
    content_type = "Content-Type: application/octet-stream"
    file_path = pathlib.Path(base_directory) / request_parts[0].split("/files/")[1].split(" ")[0]
    
    if "POST" in request_parts[0]:
        with open(file_path, "w") as file:
            file.write(request_parts[-1])
        return response201 + (CRLF * 2)
    elif file_path.exists():
        with open(file_path, "r") as file:
            content = file.read()
            return response200 + CRLF + content_type + CRLF + contentLength + str(len(content)) + (CRLF * 2) + content
    else:
        matching_files = file_exists(file_path)
        if matching_files:
            with open(matching_files[0], "r") as file:
                content = file.read()
                return response200 + CRLF + content_type + CRLF + contentLength + str(len(content)) + (CRLF * 2) + content
        return response404 + (CRLF * 2)
