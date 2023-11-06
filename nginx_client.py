import socket
import json
import hashlib
import argparse

def consistent_hash(key, nodes):
    """Generate a consistent hash for the given key."""
    hash_val = int(hashlib.md5(key.encode()).hexdigest(), 16)
    return nodes[hash_val % len(nodes)]

def send_request(server_info, method, key, value=None):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(server_info)
        request_data = json.dumps({"method": method, "key": key, "value": value})
        s.sendall(request_data.encode('utf-8'))
        response = s.recv(1024)
        print("Response:", response.decode('utf-8'))
    finally:
        s.close()
        

# Define your server nodes
servers = [("localhost", 5000), ("localhost", 5001), ("localhost", 5002)]

parser = argparse.ArgumentParser(description='Send a request to the server.')
parser.add_argument('--all_servers', type=bool, default=False, help='Boolean representing whether to send request to all servers.')
parser.add_argument('method', choices=['GET', 'PUT', 'DELETE', 'END'], help='The method to use.')
parser.add_argument('key', help='The key for the request.')
parser.add_argument('value', nargs='?', default=None, help='The value for the request (only used with PUT).')

args = parser.parse_args()



# Example usage
selected_server = consistent_hash(args.key, servers)
send_request(selected_server, args.method, args.key, args.value)
