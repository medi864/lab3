import socket
import threading
import time

tuple_space={} # Tuple space  store key-value pairs

total_clients=0

total_operations=0

read_operations=0

get_operations=0

put_operations=0

error_count=0

def handle_client(client_socket):
    global total_operations,read_operations,get_operations,put_operations,error_count
    try:
        while True:   # Receive data from  client
            data =client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            total_operations+=1    # Receive data from  client
            size_str=data[:3]
            command=data[3]
            key =data[4:].split(' ',1)[0]
            if command == 'R':
                read_operations += 1   # Try to get the value associated with the key
                value = tuple_space.get(key, '')
                if value:
                    response = f"{len(f'OK ({key}, {value}) read'):03} OK ({key}, {value}) read"
                else:
                    error_count += 1
                    response = f"{len(f'ERR {key} does not exist'):03} ERR {key} does not exist"
            elif command == 'G':
                get_operations += 1   # Try to remove the key-value pair and get the value
                value = tuple_space.pop(key, '')
                if value:
                    response = f"{len(f'OK ({key}, {value}) removed'):03} OK ({key}, {value}) removed"
                else:
                    error_count += 1
                    response = f"{len(f'ERR {key} does not exist'):03} ERR {key} does not exist"
            elif command == 'P':
                put_operations += 1
                value = data[4:].split(' ', 1)[1] if len(data.split(' ', 1)) > 1 else ''
                if key in tuple_space:
                    error_count += 1
                    response = f"{len(f'ERR {key} already exists'):03} ERR {key} already exists"
                else:
                    tuple_space[key] = value
                    response = f"{len(f'OK ({key}, {value}) added'):03} OK ({key}, {value}) added"
            client_socket.send(response.encode('utf-8'))  # Send the response back to the client
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()

def print_statistics():
    """
    Print statistics about the tuple space and operations every 10 seconds.
    """
    global total_clients, total_operations, read_operations, get_operations, put_operations, error_count
    while True:
        num_tuples = len(tuple_space)
        if num_tuples > 0:
            total_size = sum(len(k) + len(v) for k, v in tuple_space.items())
            avg_size = total_size / num_tuples
            avg_key_size = sum(len(k) for k in tuple_space.keys()) / num_tuples
            avg_value_size = sum(len(v) for v in tuple_space.values()) / num_tuples
        else:
            avg_size = 0
            avg_key_size = 0
            avg_value_size = 0
        print(f"Number of tuples: {num_tuples}, Average tuple size: {avg_size}, "
              f"Average key size: {avg_key_size}, Average value size: {avg_value_size}, "
              f"Total clients: {total_clients}, Total operations: {total_operations}, "
              f"Read operations: {read_operations}, Get operations: {get_operations}, "
              f"Put operations: {put_operations}, Error count: {error_count}")
        time.sleep(10)
def start_server(port):
    """
    Start the server and listen for incoming client connections.
    :param port: The port number on which the server will listen
    """
    global total_clients
    # Create  TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to  specified address and port
    server_socket.bind(('localhost', port))
    # Start listening for incoming connections
    server_socket.listen(5)
    print(f"Server listening on port {port}")
    while True:
        # Accept  new client connection
        client_socket, client_address = server_socket.accept()
        total_clients += 1
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()
