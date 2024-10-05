import socket
import sys

def start_server(port):
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to all available network interfaces on the specified port
    server_address = ('', port)
    print(f'Starting up UDP server on all available interfaces, port {server_address[1]}')
    sock.bind(server_address)

    # Server runs indefinitely, waiting for incoming messages
    while True:
        print('\nWaiting to receive message')
        
        # Receive data from a client (up to 4096 bytes)
        data, address = sock.recvfrom(4096)
        
        # Print details about the received message and the client address
        print(f'Received {len(data)} bytes from {address}')
        print(f'Data: {data.decode()}')  # Decode the message from bytes to string
        
        if data:
            # Send the received data back to the client (echo server behavior)
            sent = sock.sendto(data, address)
            print(f'Sent {sent} bytes back to {address}')  # Print confirmation of the number of bytes sent

if __name__ == '__main__':
    # Ensure the script is run with a valid port argument
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        sys.exit(1)
    
    # Parse the port from command-line arguments
    port = int(sys.argv[1])
    
    # Check if the port is within the valid range (58000-58999)
    if port < 58000 or port > 58999:
        print("Port must be in the range 58000-58999")
        sys.exit(1)
    
    # Start the UDP server on the specified port
    start_server(port)
