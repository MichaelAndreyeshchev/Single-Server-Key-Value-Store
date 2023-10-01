import argparse
import threading
import socket
import json

def send_request(method, key, value=None):
    try:
        request = {"method": method, "key": key, "value": value}
        request_json = json.dumps(request)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('127.0.0.1', 65432))
            s.sendall(request_json.encode('utf-8'))
            response_data = s.recv(1024)
            print(response_data.decode('utf-8'))

    except Exception as e:
        print("Connection to server from client has stopped!")

parser = argparse.ArgumentParser(description='Send a request to the server.')
parser.add_argument('method', choices=['GET', 'PUT', 'DELETE', 'END'], help='The method to use.')
parser.add_argument('key', help='The key for the request.')
parser.add_argument('value', nargs='?', default=None, help='The value for the request (only used with PUT).')

args = parser.parse_args()

send_request(args.method, args.key, args.value)