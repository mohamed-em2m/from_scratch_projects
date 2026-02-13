import socket
import ssl

host = "example.com"
port = 443

sock = socket.create_connection((host, port))

context = ssl.create_default_context()
safe_sock = context.wrap_socket(sock, server_hostname=host)

request = (
    "GET / HTTP/1.1\r\n"
    f"Host: {host}\r\n"
    "User-Agent: low-level-client/1.0\r\n"
    "Accept: */*\r\n"
    "Connection: close\r\n"
    "\r\n"
)

safe_sock.sendall(request.encode())

request = b""

while True:
    data = safe_sock.recv(4096)

    if not data:
        break

    request += data

safe_sock.close()


def decode_chunked(body):
    decode = ""
    i = 0
    while True:
        j = body.find("\r\n", i)
        chunk_size_hex = body[i:j].strip()
        chunk_size = int(chunk_size_hex, 16)
        if chunk_size == 0:
            break
        i = j + 2
        decode += body[i : i + chunk_size]
        i += chunk_size + 2
    return decode


headers, body = request.decode(errors="ignore").split("\r\n\r\n", 1)

if "transfer-encoding: chunked" in headers.lower():
    body = decode_chunked(body)

print("body", body)
