import json
import socket
from .data_types import HTTPRequest
from .data_types import HTTPResponse


class server:
    def __init__(self, port):
        self.socket = socket.socket()
        self.socket.bind(("", port))

    def listen(self):
        self.socket.listen()

    def run(self):
        self.listen()
        while True:
            connection, addr = self.socket.accept()
            first_chunk = connection.recv(4096)
            encoded_req_header, encoded_req_body = first_chunk.split(b"\r\n\r\n", 1)

            req_header = encoded_req_header.decode()

            req_headers = self.header_parser(req_header)

            content_length = int(req_headers["content-length"])

            while len(encoded_req_body) < content_length:
                chunk = connection.recv(
                    min(4096, content_length - len(encoded_req_body))
                )
                if not chunk:
                    break
                encoded_req_body += chunk

            request_body = encoded_req_body.decode()
            print("recived request from ip address", addr, "with request", request_body)
            message = {"name": "mohamed emam", "job": "ai engineer"}
            headers = {"Content-Type": "application/json"}
            response = HTTPResponse(
                body=message, status_code=200, reason="", headers=headers
            ).to_bytes()
            self.return_response(connection, response)
            connection.close()

    @staticmethod
    def return_response(connection, response):
        total_sent = 0
        while total_sent < len(response):
            sent = connection.send(response[total_sent:])
            if sent == 0:
                print(f"Failed response on user")
                break
            total_sent += sent
        return total_sent

    @staticmethod
    def header_parser(header: str):
        splited_header = header.split("\r\n")
        dict_header = {}
        for info in splited_header:
            if ":" in info:
                splited_header_info = info.lower().split(":")
                header_key = splited_header_info[0].strip().lower()
                header_value = splited_header_info[1].strip()
                dict_header[header_key] = header_value
            else:
                splited_header_info = info.lower().split()

                dict_header["method"] = splited_header_info[0]
                dict_header["path"] = splited_header_info[1]
                dict_header["protocol"] = splited_header_info[2]

        return dict_header


app = server(port=3002)
app.run()
