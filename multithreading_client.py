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

def thread_task():
    # These are example requests; adjust as needed
    send_request("PUT", "key1", "value1")
    send_request("GET", "key1")
    send_request("DELETE", "key1")

# Create and start multiple threads
threads = [threading.Thread(target=thread_task) for _ in range(10)]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()