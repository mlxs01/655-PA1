import socket
import sys

def client(host, port):
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Define the server address using the provided host and port
    server_address = (host, port)
    
    try:
        while True:
            # Read user input to send as a message
            message = input("Enter message: ")
            
            # Send the message to the server
            print(f'Sending "{message}"')
            sent = sock.sendto(message.encode(), server_address)  # Encode message to bytes and send to server

            # Wait and receive a response from the server
            print('Waiting to receive')
            data, server = sock.recvfrom(4096)  # Buffer size of 4096 bytes for incoming data
            print(f'Received "{data.decode()}"')  # Decode and print the received data

    finally:
        # Close the socket after communication ends
        print('Closing socket')
        sock.close()

if __name__ == '__main__':
    # Ensure the script is run with both host and port arguments
    if len(sys.argv) != 3:
        print("Usage: python client.py <host> <port>")
        sys.exit(1)
    
    # Parse the host and port from command-line arguments
    host = sys.argv[1]
    port = int(sys.argv[2])
    
    # Check if the port is within the valid range (58000-58999)
    if port < 58000 or port > 58999:
        print("Port must be in the range 58000-58999")
        sys.exit(1)
    
    # Start the client with the provided host and port
    client(host, port)
