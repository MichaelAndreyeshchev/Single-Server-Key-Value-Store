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
            print(response_data.decode('utf-8'))

    except Exception as e:
        print("Connection to server from client has stopped!")

def thread_task():
    source_server_node = hash_ring.get_node(hashlib.sha256("key1".encode()).hexdigest())
    server_node_info = server_nodes[source_server_node]
    
    # These are example requests; adjust as needed
    send_request(server_node_info, "PUT", "key1", "value1")
    send_request(server_node_info, "GET", "key1")
    send_request(server_node_info, "DELETE", "key1")

# Create and start multiple threads
threads = [threading.Thread(target=thread_task) for _ in range(10)]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()