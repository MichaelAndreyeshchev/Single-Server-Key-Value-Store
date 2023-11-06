import os
import json
import time
import pickle
import socket
import logging
import threading
import argparse
from datetime import datetime 
from flask import Flask, request, jsonify

#logging.basicConfig(filename='server.log', level=logging.INFO)
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
thread_lock = threading.Lock()

hash_table = {}


class LoggingFilter(logging.Filter):
    def filter(self, res):
        return "werkzeug" not in res.name

        
class MultiThreadedServer:
    def __init__(self, host, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen()
        self.running = True

        logging.basicConfig(filename='server.log', level=logging.INFO)
        self.logger = logging.getLogger('ServerLogger')
        self.load_disk_data()

    def persistance_mechanism(self):
        while self.running:
            time.sleep(5)
            with thread_lock:
                with open("key_val_storage.pkl", "wb") as file:
                    pickle.dump(hash_table, file)

    def load_disk_data(self):
        global hash_table

        if os.path.exists("key_val_storage.pkl") and os.path.getsize("key_val_storage.pkl") > 0:
            with open("key_val_storage.pkl", "rb") as file:
                    hash_table = pickle.load(file)

    def process_request(self, client_socket, client_address):
        request_data = client_socket.recv(1024)
        request_str = request_data.decode("utf-8")
        
        if not request_str:
            return
        
        request_json = json.loads(request_str)
        
        method = request_json.get("method")
        key = request_json.get("key")
        value = request_json.get("value")

        current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if method == "GET":
            with thread_lock:
                value = hash_table.get(key, None)

            response = {"GET result": value} if value else {"GET error": f"{key} does not exist!"}
            self.logger.info(f'Current Timestamp: {current_timestamp}, GET request -- Key: {key}, Result: {response}')
        
        elif method == "PUT":
            with thread_lock:
                hash_table[key] = value

            response = {"PUT result": f"key: {key}, value: {value} has been inserted!"} if value else {"PUT error": f"{key} does not exist!"}
            self.logger.info(f'Current Timestamp: {current_timestamp}, PUT request -- Key: {key}, Value: {value}, Result: {response}')

        elif method == "DELETE":
            with thread_lock:
                value = hash_table.pop(key, None)

            response = {"DELETE result": f"{key} has been deleted!"} if value else {"DELETE error": f"{key} does not exist!"}
            self.logger.info(f'Current Timestamp: {current_timestamp}, DELETE request -- Key: {key}, Result: {response}')

        elif method == "END":
            response = {"END result": "Server has been closed!"}
            self.running = False


        client_socket.send(json.dumps(response).encode('utf-8'))
        client_socket.close()

    def handle_client(self, client_socket, client_address):
        try:
            self.process_request(client_socket, client_address)
        finally:
            client_socket.close()

    def serve_forever(self):
        print(f'Server started on {self.server_socket.getsockname()}')
        while self.running:
            try:
                client_socket, client_address = self.server_socket.accept()
                print(f'Connection from {client_address}')
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_address)
                )
                client_thread.start()
            
            except KeyboardInterrupt:
                self.server_socket.close()
                print("Server has been closed!")
                break 

        self.server_socket.close()
        print("Server has been closed!")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send a request to the server.')
    parser.add_argument('port', help='The port for the server.')

    args = parser.parse_args()

    server = MultiThreadedServer('0.0.0.0', int(args.port))
    persistance_mechanism_thread = threading.Thread(target = server.persistance_mechanism)
    persistance_mechanism_thread.daemon = True
    persistance_mechanism_thread.start()
    server.serve_forever()


# import os
# import json
# import time
# import pickle
# import socket
# import logging
# import argparse
# import threading
# from datetime import datetime 
# from uhashring import HashRing
# from flask import Flask, request, jsonify

# #logging.basicConfig(filename='server.log', level=logging.INFO)
# app = Flask(__name__)
# app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
# thread_lock = threading.Lock()

# hash_table = {}

# server_nodes = {
#    "server_1": {"host": '127.0.0.1', "port": 65432},
#    "server_2": {"host": '127.0.0.1', "port": 65433},
#    "server_3": {"host": '127.0.0.1', "port": 65434},
# }

# hash_ring = HashRing(nodes = server_nodes, vnodes = 10)

# class LoggingFilter(logging.Filter):
#     def filter(self, res):
#         return "werkzeug" not in res.name

        
# class MultiThreadedServer:
#     def __init__(self, host, port):
#         self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#         self.server_socket.bind((host, port))
#         self.server_socket.listen()
#         self.running = True
#         self.port = port
#         self.host = host

#         logging.basicConfig(filename='server.log', level=logging.INFO)
#         self.logger = logging.getLogger('ServerLogger')
#         self.load_disk_data()

#     def forward_request(self, server_node_info, request_data):
#         try:
#             with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as fwd_socket:
#                 fwd_socket.connect((server_node_info["host"], server_node_info["port"]))
#                 fwd_socket.sendall(request_data.encode('utf-8'))
#                 response = fwd_socket.recv(1024)
#                 return response
            
#         except Exception as e:
#             print(f"Error forwarding request: {e}")
#             return json.dumps({'error': 'Error forwarding request'}).encode('utf-8')

#     def persistance_mechanism(self):
#         while self.running:
#             time.sleep(5)
#             with thread_lock:
#                 with open("key_val_storage.pkl", "wb") as file:
#                     pickle.dump(hash_table, file)

#     def load_disk_data(self):
#         global hash_table

#         if os.path.exists("key_val_storage.pkl") and os.path.getsize("key_val_storage.pkl") > 0:
#             with open("key_val_storage.pkl", "rb") as file:
#                 hash_table = pickle.load(file)

#     def process_request(self, client_socket, client_address):
#         try:
#             request_data = client_socket.recv(1024)
#             request_str = request_data.decode("utf-8")
            
#             if not request_str:
#                 return
            
#             request_json = json.loads(request_str)
            
#             method = request_json.get("method")
#             key = request_json.get("key")
#             value = request_json.get("value")

#             source_server_node = hash_ring.get_node(key)

#             if server_nodes[source_server_node]["host"] != socket.gethostbyname('localhost') or server_nodes[source_server_node]["port"] != self.port:
#                 response = self.forward_request(server_nodes[source_server_node], request_str)

#             else:
#                 current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#                 if method == "GET":
#                     with thread_lock:
#                         value = hash_table.get(key, None)

#                     response = {"GET result": value} if value else {"GET error": f"{key} does not exist!"}
#                     self.logger.info(f'Current Timestamp: {current_timestamp}, Server: {source_server_node}, GET request -- Key: {key}, Result: {response}')
                
#                 elif method == "PUT":
#                     with thread_lock:
#                         hash_table[key] = value

#                     response = {"PUT result": f"key: {key}, value: {value} has been inserted!"} if value else {"PUT error": f"{key} does not exist!"}
#                     self.logger.info(f'Current Timestamp: {current_timestamp}, Server: {source_server_node}, PUT request -- Key: {key}, Value: {value}, Result: {response}')

#                 elif method == "DELETE":
#                     with thread_lock:
#                         value = hash_table.pop(key, None)

#                     response = {"DELETE result": f"{key} has been deleted!"} if value else {"DELETE error": f"{key} does not exist!"}
#                     self.logger.info(f'Current Timestamp: {current_timestamp}, Server: {source_server_node}, DELETE request -- Key: {key}, Result: {response}')

#                 elif method == "END":
#                     with thread_lock:
#                         response = {f"END result: {source_server_node} has been closed!"}
#                         self.running = False

#                     self.server_socket.close()

#                 response = json.dumps(response).encode('utf-8')


#             client_socket.send(response)

#         except Exception as e:
#             response = json.dumps({'error': str(e)}).encode('utf-8')
#             client_socket.send(response)

#         if method == "END":
#             os._exit(0)

#     def handle_client(self, client_socket, client_address):
#         try:
#             self.process_request(client_socket, client_address)
#         finally:
#             client_socket.close()

#     def serve_forever(self):
#         print(f'Server started on {self.server_socket.getsockname()}')
#         while self.running:
#             try:
#                 client_socket, client_address = self.server_socket.accept()
#                 print(f'Connection from {client_address}')
#                 client_thread = threading.Thread(
#                     target=self.handle_client,
#                     args=(client_socket, client_address)
#                 )
#                 client_thread.start()
            
#             except KeyboardInterrupt:
#                 self.running = False
#                 self.server_socket.close()
#                 print("Server has been closed!")
#                 break 

#         self.server_socket.close()
#         print("Server has been closed!")

# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description='Multi-threaded Server with Consistent Hashing')
#     parser.add_argument('node', help='Enter server node name to start!')
#     args = parser.parse_args()

#     if args.node not in server_nodes:
#         raise ValueError("Server ode name must be one of {}".format(' , '.join(server_nodes.keys())))

#     port = server_nodes[args.node]["port"]
#     server = MultiThreadedServer('0.0.0.0', port)
#     persistence_thread = threading.Thread(target=server.persistance_mechanism)
#     persistence_thread.daemon = True
#     persistence_thread.start()
#     server.serve_forever()