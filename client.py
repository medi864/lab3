import socket
import sys

def send_request(client_socket, request):
    """
    Send a request to the server and receive the response.
    :param client_socket: The socket object for the server connection
    :param request: The request string to be sent
    :return: The response string received from the server
    """
    # Format the request with the message size
    size_str = f"{len(request):03}"
    full_request = size_str + request
    # Send the request to the server
    client_socket.send(full_request.encode('utf-8'))
    # Receive the response from the server
    response = client_socket.recv(1024).decode('utf-8')
    return response
