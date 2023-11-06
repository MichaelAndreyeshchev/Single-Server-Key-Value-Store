import threading
import socket
import json
import argparse
from uhashring import HashRing
import hashlib

server_nodes = {
    "server_1": {"host": '127.0.0.1', "port": 65432},
    "server_2": {"host": '127.0.0.1', "port": 65433},
    "server_3": {"host": '127.0.0.1', "port": 65434},
}


hash_ring = HashRing(nodes = server_nodes, vnodes = 10)

def send_request(server_node_info, method, key, value=None):
    try:
        request = {"method": method, "key": key, "value": value}
        request_json = json.dumps(request)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((server_node_info["host"], server_node_info["port"]))
            s.sendall(request_json.encode('utf-8'))
            response_data = s.recv(1024)
            s.close()
            print(response_data.decode('utf-8'))

    except Exception as e:
        print("Connection to server from client has stopped!")

def send_request_to_all(method, key, value=None):
    for name, info in server_nodes.items():
        try:
            request = {"method": method, "key": key, "value": value}
            request_json = json.dumps(request)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((info["host"], info["port"]))
                s.sendall(request_json.encode('utf-8'))
                response_data = s.recv(1024)
                print(response_data.decode('utf-8'))

        except Exception as e:
            print("Connection to server from client has stopped!")
            

parser = argparse.ArgumentParser(description='Send a request to the server.')
parser.add_argument('--all_servers', type=bool, default=False, help='Boolean representing whether to send request to all servers.')
parser.add_argument('method', choices=['GET', 'PUT', 'DELETE', 'END'], help='The method to use.')
parser.add_argument('key', help='The key for the request.')
parser.add_argument('value', nargs='?', default=None, help='The value for the request (only used with PUT).')

args = parser.parse_args()


source_server_node = hash_ring.get_node(hashlib.sha256(args.key.encode()).hexdigest())
server_node_info = server_nodes[source_server_node]

if args.all_servers:
    send_request_to_all(args.method, args.key, args.value)
else:
    send_request(server_node_info, args.method, args.key, args.value)
