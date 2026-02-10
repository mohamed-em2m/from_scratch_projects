import socket
import ssl
host="example.com"
port=443
context=ssl.create_default_context()
sock=socket.create_connection((host,port))
safe_sock=context.wrap_socket(sock,server_hostname=host)
request=("GET / HTTP/1.1\r\n"
         f"Host: {host}\r\n"
         "User-Agent: low-level-client/1.0\r\n"
         "Accept: */*\r\n"
         "Connection: close\r\n"
         "\r\n")
safe_sock.sendall(request.encode())
request=b""
while True:
    data=safe_sock.recv(4096)
    if not data:
        break
    request+=data
safe_sock.close()

print(request.decode(errors='ignore'))