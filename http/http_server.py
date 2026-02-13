import json
import socket
class server:
    def __init__(self,port):
        self.socket = socket.socket()
        self.socket.bind(("", port))    
        
    def listen(self):
        self.socket.listen()
        
    def run(self):
        self.listen()
        while True:
            connection,addr = self.socket.accept()
            first_chunk = connection.recv(4096)
            encoded_req_header , encoded_req_body = first_chunk.split(b"\r\n\r\n",1)

            req_header = encoded_req_header.decode()
            
            req_headers = self.header_parser(req_header)
            
            content_length = int(req_headers["content-length"])
            
            while len(encoded_req_body) < content_length:
                    chunk = connection.recv(min(4096 , content_length - len(encoded_req_body) ))
                    if not chunk:
                        break
                    encoded_req_body += chunk
                    
            request_body = encoded_req_body.decode()
            print("recived request from ip address",addr,"with request",request_body)
            message={"name":"mohamed emam","job":"ai engineer"}
            response = self.create_response_encoded(message,"application/json")
            self.return_response(connection,response)
            connection.close() 

    @staticmethod
    def create_response_encoded(message,content_type):
        if isinstance(message,dict):
            response_body = json.dumps(message)
        elif isinstance(message,str):
            response_body = message
        response_body = response_body.encode()
        response_header = ( "HTTP/1.1 200 OK\r\n"
                            f"Content-Type: {content_type}\r\n"
                            f"Content-Length: {len(response_body)}\r\n"
                            "\r\n"
                            ).encode()
        response = response_header + response_body
        return response
    
    @staticmethod
    def return_response(connection,response):
        total_sent = 0
        while total_sent < len(response):
            sent = connection.send(response[total_sent:])
            if sent == 0:
                print(f"Failed response on user")
                break
            total_sent += sent
        return total_sent
    
    @staticmethod
    def header_parser(header:str):
        splited_header = header.split("\r\n")
        dict_header={}
        for info in splited_header :
            if ":" in info:
                splited_header_info = info.lower().split(":")
                header_key = splited_header_info[0].strip().lower()
                header_value = splited_header_info[1].strip()
                dict_header[header_key] = header_value
            else:
                splited_header_info = info.lower().split()
                
                dict_header["method"] =  splited_header_info[0]
                dict_header["path"] = splited_header_info[1]
                dict_header["protocol"] = splited_header_info[2]
    
        return dict_header
    
app=server(port=3002)
app.run()

#curl http://127.0.0.1:3002 -d '{"mohamed":"emam"}' -H "Content-Type: application/json"