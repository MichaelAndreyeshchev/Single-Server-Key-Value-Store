import multiprocessing
import requests
import time
import random
import multiprocessing
import requests
import time
import random
import socket
import json
# import argparse
# import time
from uhashring import HashRing
# import matplotlib.pyplot as plt
# import numpy as np
import hashlib
from hashring import HashRing
#BASE_URLS = ['http://127.0.0.1:65432', 'http://127.0.0.1:65433', 'http://127.0.0.1:65434']
#BASE_URLS = ['http://127.0.0.1:8080', 'http://127.0.0.1:8081']
BASE_URLS = ['http://127.0.0.1:65432']
ring = HashRing(BASE_URLS)

def kv_store_client(operation, key, value=None):
    # Determine which server to use based on the key
    server_url = ring.get_node(key)
    start_time = time.time()
    try:
        request = {"method": operation, "key": key, "value": value}
        request_json = json.dumps(request)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect((server_url[7:-6], int(server_url[-5:])))
        s.sendall(request_json.encode('utf-8'))
        response_data = s.recv(1024)

    except Exception as e:
        print(f'Error performing {operation} on {key}: {e}')
        return None

    finally:
        if s:
            s.close()

    end_time = time.time()
    return end_time - start_time
  

def worker(num_operations, latencies_queue, operation, process_index):
    for i in range(num_operations):
        key = f'key{process_index}_{i}'
        value = f'value{process_index}_{i}' if operation == 'set' else None
        latency = kv_store_client(operation, key, value)
        if latency is not None:
            latencies_queue.put(latency)

def benchmark(num_operations, num_processes):
    manager = multiprocessing.Manager()
    latencies_queue = manager.Queue()

    set_processes = [
        multiprocessing.Process(target=worker, args=(num_operations, latencies_queue, 'set', i))
        for i in range(num_processes)
    ]
    get_processes = [
        multiprocessing.Process(target=worker, args=(num_operations, latencies_queue, 'get', i))
        for i in range(num_processes)
    ]
    start_time = time.time()

    for p in set_processes:
        p.start()
    for p in set_processes:
        p.join()

    for p in get_processes:
        p.start()
    for p in get_processes:
        p.join()

    total_time = time.time() - start_time
    total_operations = num_operations * num_processes * 2  # Each process does num_operations SET and GET
    total_latencies = []

    while not latencies_queue.empty():
        total_latencies.append(latencies_queue.get())

    average_latency = sum(total_latencies) / len(total_latencies)
    print(f'Total Latency: {sum(total_latencies):.2f} second')
    print(f'Length of latencies: {len(total_latencies):.0f} latencies')
    throughput = total_operations / total_time
    print(f'Total Operation: {total_operations:.0f} operations')
    print(f'Average Latency: {average_latency:.5f} seconds per operation')
    print(f'Throughput: {throughput:.2f} operations per second')
    print(f'Total Benchmark Time: {total_time:.2f} seconds')

if __name__ == '__main__':
    num_operations_per_process = 350
    num_processes = 15
    benchmark(num_operations_per_process, num_processes)




# import threading
# import socket
# import json
# import argparse
# import time
# from uhashring import HashRing
# import matplotlib.pyplot as plt
# import numpy as np
# import hashlib


# print_lock = threading.Lock()
# operation_lock = threading.Lock()

# def send_request(server_node_info, method, key, value=None):
#     try:
#         request = {"method": method, "key": key, "value": value}
#         request_json = json.dumps(request)

#         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#         s.connect((server_node_info["host"], server_node_info["port"]))
#         s.sendall(request_json.encode('utf-8'))
#         response_data = s.recv(1024)

#     except Exception as e:
#         with print_lock:
#             print(f'Error performing {method} on {key}: {e}')

#     finally:
#         if s:
#             s.close()


# def perform_tests(server_nodes, hash_ring, num_requests, method, value=None):
#     for i in range(num_requests):
#         key = f"{i*2} key"
#         source_server_node = hash_ring.get_node(hashlib.sha256(key.encode()).hexdigest()) # implemented a custom hashing function to perform similar hashing to nginx
#         server_node_info = server_nodes[source_server_node]
#         send_request(server_node_info, method, key, value)


# def calculate_metrics(start_time, num_requests_per_thread):
#     latency = time.time()-start_time
#     throughput = num_requests_per_thread / latency

#     return latency, throughput

# def threaded_test(server_nodes, hash_ring, num_threads, num_requests_per_thread, method, value=None):
#     threads = []
#     all_latencies = []

#     start_time = time.time()

#     for _ in range(num_threads):
#         thread = threading.Thread(target=perform_tests, args=(server_nodes, hash_ring, num_requests_per_thread, method, value,))
#         threads.append(thread)
#         thread.start()

#     for thread in threads:
#         thread.join()

#     return calculate_metrics(start_time, num_requests_per_thread)

# def init_server_nodes(num_servers):
#     server_nodes = {}
#     for i in range(num_servers):
#         server_nodes[f"server_{i+1}"] = {"host": '127.0.0.1', "port": 65432 + i}
#     return server_nodes

# parser = argparse.ArgumentParser(description='Send a request to the server.')
# parser.add_argument('--num_servers', type=int, default=3, help='Number of servers to use for testing.')
# parser.add_argument('--num_threads', type=int, default=10, help='Number of threads to use for testing.')
# parser.add_argument('--num_requests', type=int, default=100, help='Number of requests per thread.')
# parser.add_argument('method', choices=['GET', 'PUT', 'DELETE'], help='The method to use.')
# parser.add_argument('--value', default=None, help='The value for the request (only used with PUT).')

# args = parser.parse_args()

# server_throughputs = []
# server_latencies = []

# for num_servers in range(1, int(args.num_servers) + 1):
#     throughputs = []
#     latencies = []

#     server_nodes = init_server_nodes(num_servers)
#     hash_ring = HashRing(nodes=server_nodes, vnodes = 10)

#     for i in range(10, args.num_requests, 10):
#         average_latency, throughput = threaded_test(server_nodes, hash_ring, args.num_threads, i, args.method, args.value)
#         throughputs.append(throughput)
#         latencies.append(average_latency)
#         print(f"Average Latency: {average_latency:.4f} seconds")
#         print(f"Throughput: {throughput:.2f} requests per second")

#     server_throughputs.append(throughputs)
#     server_latencies.append(latencies)

# colors = ["red", "green", "blue", "yellow", "pink", "cyan"]
# plt.figure(figsize=(10, 6))
# for i in range(int(args.num_servers)):
#     #z = np.polyfit(server_throughputs[i], server_latencies[i], 2) 
#     #p = np.poly1d(z)
#     #plt.plot(server_throughputs[i], p(server_throughputs[i]), color=colors[i], linestyle="--", label=f"{i+1} Servers")
#     plt.plot(server_throughputs[i], server_latencies[i], color = colors[i], marker="o", label=f"{i+1} Servers")

# plt.ylabel("Latency (seconds)")
# plt.xlabel("Throughput (operations / seconds)")
# plt.title(f"Latency vs. Throughput for {args.method} operations")
# plt.grid("True")
# plt.legend()
# plt.show()
