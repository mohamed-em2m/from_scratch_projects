import socket
import json

port=3001

sock=socket.socket()
sock.bind(("",port))
sock.listen()

while True:
    connection,addr = sock.accept()
    request_length = 0
    first_chunk = connection.recv(4096)
    encoded_req_header , encoded_req_body = first_chunk.split(b"\r\n\r\n",1)
    req_header = encoded_req_header.decode()
    req_header_info = req_header.split("\r\n")
    content_length = [word.lower().replace("content-length:","").strip() for word in req_header_info if word.lower().startswith("content-length")][0]
    content_length = int(content_length)
    
    while len(encoded_req_body) < content_length:
            chunk = connection.recv(min(4096 , content_length - len(encoded_req_body) ))
            if not chunk:
                break
            encoded_req_body += chunk
            
    request_body = encoded_req_body.decode()
    print("recived request from ip address",addr,"with request",request_body)
    
    response_body = json.dumps({"message":"hello emam greet you"}).encode()
    response_header = ("HTTP/1.1 200 OK\r\n"
              "Content-Type: application/json\r\n"
              f"Content-Length: {len(response_body)}\r\n"
              "\r\n"
              ).encode()
    response = response_header + response_body
    
    total_sent = 0

    while total_sent < len(response):
        sent = connection.send(response[total_sent:])
        if sent == 0 :    
           print(f"Failed response on user {addr}")
        total_sent += sent

    connection.close() 
    print("server responsed on",addr,"with response size",total_sent)
