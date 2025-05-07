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
def main():
    """
    Main function to handle client operations.
    """
    if len(sys.argv) != 4:
        print("Usage: python client.py <server_host> <server_port> <request_file>")
        sys.exit(1)
    # Get the server host from command line arguments
    server_host = sys.argv[1]
    # Get the server port from command line arguments
    server_port = int(sys.argv[2])
    # Get the request file path from command line arguments
    request_file = sys.argv[3]
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to the server
    client_socket.connect((server_host, server_port))