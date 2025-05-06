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
            print("nihao")
    finally:
        client_socket.close()