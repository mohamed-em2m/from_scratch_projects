import ssl
import json
import socket

host = "generativelanguage.googleapis.com"
port = 443
API_KEY = "Your Token"

body = """{
    "model": "gemini-3-flash-preview",
    "messages": [
      {
        "role": "user",
        "content": "Explain to me how AI works"
      }
    ]
  }""".encode()

sock = socket.socket()

sock.connect((host, port))

requester = ssl.create_default_context().wrap_socket(sock, server_hostname=host)

request = (
    "POST /v1beta/openai/chat/completions HTTP/1.1\r\n"
    f"Host: {host}\r\n"
    f"Authorization: Bearer {API_KEY}\r\n"
    "Content-Type: application/json\r\n"
    f"Content-Length: {len(body)}\r\n"
    "Connection: close\r\n"
    "\r\n"
)

requester.sendall(request.encode() + body)

response = b""

while True:
    chunk = requester.recv(4096)
    if not chunk:
        break
    response += chunk

header, body = response.split(b"\r\n\r\n", 1)
readed_body = b""
start_index = 0
split_char_length = 2
while start_index < len(body):
    split_index = body.find(b"\r\n", start_index)
    chunk_length = int(body[start_index:split_index].strip(), 16)
    if not chunk_length:
        break
    start_index = split_index + split_char_length
    end_data = start_index + chunk_length
    readed_body += body[start_index:end_data]
    start_index += split_char_length + chunk_length

print("body:", json.loads(readed_body.decode("utf-8")))
