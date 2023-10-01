# Multi-Threaded Key-Value Store Server

This project implements a simple multi-threaded key-value store server along with client scripts to interact with the server. The server utilizes sockets for communication, and handles concurrent requests using threading. It supports GET, PUT, and DELETE operations on a hash table. Additionally, it provides a persistence mechanism to save the hash table data to disk and load it back upon server startup.

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

The `client.py` script is a simple client-side script to interact with the multi-threaded key-value store server. It can send requests for inserting, fetching, or deleting key-value pairs to the server. It also supports a request to end the server process.  The `client.py` script uses command line arguments to specify the request to be sent to the server. The arguments are parsed using the `argparse` module.

### Prerequisites

- Ensure you have Python 3.x installed on your machine.
- The server should be running before executing this client script.

### Getting Started

First, clone the repository or download the `client.py` script to your local machine.

## Multi-threaded Client for Key-Value Store Server

This repository contains a multi-threaded client script, `multithreading_client.py`, which can be used to interact with a key-value store server. The client script allows sending `PUT`, `GET`, and `DELETE` requests to the server, to either store, retrieve, or delete key-value pairs, respectively.

### Dependencies

- Python 3.x
- Ensure the server is running before executing this client script.


### Usage

1. **Start the Server:**
```bash
py -3 server.py
```
2. **Running the Multi-Threaded Client:**
```bash
py -3 client_multi_threaded.py # End the server and client by clicking ctr-C in the running server code and then rerunning the py -3 client_multi_threaded.py to fully terminate the server and client
```
**OR**
2. **Running the Command-line Client:**
```bash
py -3 client.py PUT key1 value1
py -3 client.py GET key1
py -3 client.py DELETE key1
py -3 client.py END end # Ends the server and clients! You will have to call this twice to fully do this
```