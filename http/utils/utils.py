import json
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