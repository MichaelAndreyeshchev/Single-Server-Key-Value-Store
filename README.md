# Multi-Threaded Key-Value Store Server

This project implements a multi-threaded key-value store server along with client scripts to interact with more than one server. The servers utilize sockets for communication, and handles concurrent requests using threading. They supports GET, PUT, and DELETE operations on a hash table. Additionally, it provides a persistence mechanism to save the hash table data to disk and load it back upon server startup.  Moreover, consistent hashing is employd to evenly distribute the load across multiple KV stores, ensuring a more fault-tolerant system.

## Server Script (`server.py`)

### Dependencies

- Python 3
- Flask

### Features

1. **Multi-Threading**: The server handles multiple client connections concurrently using threads.
2. **Simple Key-Value Store**: Supports basic operations (GET, PUT, DELETE) on a hash table.
3. **Concurrent Requests**: Handles multiple concurrent requests -- as can be tested in multithreading_client.py
4. **Persistence**: Utilizes a persistence mechanism to save the hash table to a file and load it back on server startup.
5. **Error Handeling**: Handles errors gracefully by throwing a message describing the errors.
6. **Logging**: Logs the requests and results of GET, PUT, and DELETE operations.

### Classes and Methods

- **`LoggingFilter`**: A filter for logging, filters out Flask's default logger.
- **`MultiThreadedServer`**: The main server class with the following methods:
  - `__init__(self, host, port)`: Initializes the server socket and starts listening for connections.
  - `persistance_mechanism(self)`: Saves the hash table to disk every 5 seconds.
  - `load_disk_data(self)`: Loads the hash table data from disk if available.
  - `process_request(self, client_socket, client_address)`: Processes client requests (i.e. GET, PUT, or DEL).
  - `handle_client(self, client_socket, client_address)`: Handles individual client connections.
  - `serve_forever(self)`: The main loop that accepts new client connections and spawns threads to handle them.

## Client Script for Multi-Threaded Key-Value Store Server

The `client.py` script is a client-side script to interact with multiple multi-threaded key-value store servers. It can send requests for inserting, fetching, or deleting key-value pairs to the servers. It also supports a request to end the server process.  The `client.py` script uses command line arguments to specify the request to be sent to the servers. The arguments are parsed using the `argparse` module.

## Testing and Measurement Client Script for Multi-Threaded Key-Value Store Server

The `testing_and_measurement.py` script is a client-side script to interact with multiple multi-threaded key-value store server. It can send requests for inserting, fetching, or deleting key-value pairs to the server. The code outputs latency vs. throughput plots and allows you to input using the `argparse` module the number of servers `num_servers`, the number of threads `num_threads`, and the number of requests `num_requests`

### Prerequisites

- Ensure you have Python 3.x installed on your machine.
- The server should be running before executing the client scripts.

### Getting Started

First, clone the repository or download the `client.py` script to your local machine.

## Multi-threaded Client for Key-Value Store Server

This repository contains a multi-threaded client script, `multithreading_client.py`, which can be used to interact with a key-value store server. The client script allows sending `PUT`, `GET`, and `DELETE` requests to the server, to either store, retrieve, or delete key-value pairs, respectively.

### Dependencies

- Python 3.x
- Ensure the server is running before executing this client script.

### Docker Usage

1. **Start the Server:**
```bash
git clone https://github.com/MichaelAndreyeshchev/Single-Server-Key-Value-Store.git key_value_store
cd key_value_store
docker build -t key_value_store . 
docker run -p 127.0.0.1:65432:65432 key_value_store # the server is now running
```
2. **Running the Multi-Threaded Client:**
```bash
python multithreading_client.py # End the server by running "python client.py END end" twice
```
**OR**
3. **Running the Command-line Client:**
```bash
python client.py PUT key1 value1
python client.py GET key1
python client.py DELETE key1
python client.py END end # Ends the server and clients! You will have to call this twice to fully do this
```

### Regular Usage

1. **Start the Server(s):**
```bash
git clone https://github.com/MichaelAndreyeshchev/Single-Server-Key-Value-Store.git
cd Single-Server-Key-Value-Store
py -3 server.py [PORT_NUMBER]
```
2. **Running the Multi-Threaded Client:**
```bash
py -3 multithreading_client.py # End the server and client by clicking ctr-C in the running server code and then rerunning the py -3 client_multi_threaded.py to fully terminate the server and client
```
**OR**
3. **Running the Command-line Client:**
```bash
py -3 client.py PUT key1 value1
py -3 client.py GET key1
py -3 client.py DELETE key1
py -3 client.py --all_servers True END end # Ends all servers and clients! You will have to call this twice to fully do this
```
**OR**
3. **Running the Command-line Testing and Measurement Client (to output latency vs. throughput values):**
```bash
py -3 testing_and_measurement.py PUT --value some_value # NOTE: You must wait a few minutes after this command completes before trying additional commands because the connection precesses must be put of out of waiting state
py -3 testing_and_measurement.py GET # NOTE: You must wait a few minutes after this command completes before trying additional commands because the connection precesses must be put of out of waiting state
py -3 testing_and_measurement.py DELETE # NOTE: You must wait a few minutes after this command completes before trying additional commands because the connection precesses must be put of out of waiting state
py -3 client.py --all_servers True END end # Ends all servers and clients! You will have to call this twice to fully do this
```