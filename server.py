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
        self.host = host
        self.port = port
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
        response = {}

        if method == "GET":
            with thread_lock:
                value = hash_table.get(key, None)

            response = {f"GET result on server {self.host}:{self.port}": value} if value else {"GET error": f"{key} does not exist!"}
            self.logger.info(f'Current Timestamp: {current_timestamp}, GET request -- Key: {key}, Result: {response}')
        
        elif method == "PUT":
            with thread_lock:
                hash_table[key] = value

            response = {f"PUT result on server {self.host}:{self.port}": f"key: {key}, value: {value} has been inserted!"} if value else {"PUT error": f"{key} does not exist!"}
            self.logger.info(f'Current Timestamp: {current_timestamp}, PUT request -- Key: {key}, Value: {value}, Result: {response}')

        elif method == "DELETE":
            with thread_lock:
                value = hash_table.pop(key, None)

            response = {f"DELETE result on server {self.host}:{self.port}": f"{key} has been deleted!"} if value else {"DELETE error": f"{key} does not exist!"}
            self.logger.info(f'Current Timestamp: {current_timestamp}, DELETE request -- Key: {key}, Result: {response}')

        elif method == "END":
            response = {f"END result on server {self.host}:{self.port}": "Server has been closed!"}
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
# import threading
# import argparse
# from datetime import datetime 
# from flask import Flask, request, jsonify
# import asyncio
# import aiofiles



# #logging.basicConfig(filename='server.log', level=logging.INFO)
# app = Flask(__name__)
# app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
# thread_lock = threading.Lock()

# hash_table = {}


# class LoggingFilter(logging.Filter):
#     def filter(self, res):
#         return "werkzeug" not in res.name

        
# class MultiThreadedServer:
#     def __init__(self, host, port):
#         #self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         #self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#         #self.server_socket.bind((host, port))
#         #self.server_socket.listen()
#         self.host = host
#         self.port = port
#         self.running = True

#         logging.basicConfig(filename='server.log', level=logging.INFO)
#         self.logger = logging.getLogger('ServerLogger')
#         asyncio.run(self.load_disk_data())

#     async def persistance_mechanism(self):
#         while self.running:
#             await asyncio.sleep(5)
#             with thread_lock:
#                 async with aiofiles.open("key_val_storage.pkl", "wb") as file:
#                     await file.write(pickle.dumps(hash_table))

#     async def load_disk_data(self):
#         if os.path.exists("key_val_storage.pkl") and os.path.getsize("key_val_storage.pkl") > 0:
#             async with aiofiles.open("key_val_storage.pkl", "rb") as file:
#                 global hash_table
#                 hash_table = pickle.loads(await file.read())

#     def process_request(self, request_str):
#         if not request_str:
#             return ''
        
#         request_json = json.loads(request_str)
        
#         method = request_json.get("method")
#         key = request_json.get("key")
#         value = request_json.get("value")

#         current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         response = {}

#         if method == "GET":
#             with thread_lock:
#                 value = hash_table.get(key, None)

#             response = {f"GET result on server {self.host}:{self.port}": value} if value else {"GET error": f"{key} does not exist!"}
#             self.logger.info(f'Current Timestamp: {current_timestamp}, GET request -- Key: {key}, Result: {response}')
        
#         elif method == "PUT":
#             with thread_lock:
#                 hash_table[key] = value

#             response = {f"PUT result on server {self.host}:{self.port}": f"key: {key}, value: {value} has been inserted!"} if value else {"PUT error": f"{key} does not exist!"}
#             self.logger.info(f'Current Timestamp: {current_timestamp}, PUT request -- Key: {key}, Value: {value}, Result: {response}')

#         elif method == "DELETE":
#             with thread_lock:
#                 value = hash_table.pop(key, None)

#             response = {f"DELETE result on server {self.host}:{self.port}": f"{key} has been deleted!"} if value else {"DELETE error": f"{key} does not exist!"}
#             self.logger.info(f'Current Timestamp: {current_timestamp}, DELETE request -- Key: {key}, Result: {response}')

#         elif method == "END":
#             response = {f"END result on server {self.host}:{self.port}": "Server has been closed!"}
#             self.running = False


#         return json.dumps(response)

#     async def handle_client(self, reader, writer):
#         data = await reader.read(1024)  # Asynchronous read
#         message = data.decode()
#         addr = writer.get_extra_info('peername')

#         self.logger.info("Received %r from %r" % (message, addr))

#         response = self.process_request(message)

#         writer.write(response.encode())  # Asynchronous write
#         await writer.drain()  # Ensure data is sent
#         writer.close()

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
#                 self.server_socket.close()
#                 print("Server has been closed!")
#                 break 

#         self.server_socket.close()
#         print("Server has been closed!")

#     async def run_server(self):
#         server = await asyncio.start_server(
#             self.handle_client, self.host, self.port)

#         addr = server.sockets[0].getsockname()
#         self.logger.info(f'Serving on {addr}')

#         async with server:
#             await server.serve_forever()

# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description='Send a request to the server.')
#     parser.add_argument('port', help='The port for the server.')

#     args = parser.parse_args()

#     server = MultiThreadedServer('0.0.0.0', int(args.port))
#     #persistance_mechanism_thread = threading.Thread(target = server.persistance_mechanism)
#     #persistance_mechanism_thread.daemon = True
#     #persistance_mechanism_thread.start()
#     #server.serve_forever()
#     print("Test")
#     asyncio.run(server.run_server())