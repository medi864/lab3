import socket
import threading
import time

tuple_space={}

total_clients=0
total_operations=0
read_operations=0
get_operations=0
put_operations=0
error_count=0

def handle_client(client_socket):
    global tatol_operations,read_operations,get_operations,put_operations,error_count
    try:
        while True:
            data =client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            total_operations+=1
            size_str=data[:3]
            command=data[3]
            key =data[4:].split(' ',1)[0]
            if command == 'R':
                read_operations += 1
                value = tuple_space.get(key, '')
                if value:
                    response = f"{len(f'OK ({key}, {value}) read'):03} OK ({key}, {value}) read"
                else:
                    error_count += 1
                    response = f"{len(f'ERR {key} does not exist'):03} ERR {key} does not exist"
            elif command == 'G':
                get_operations += 1
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
            client_socket.send(response.encode('utf-8'))
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()


