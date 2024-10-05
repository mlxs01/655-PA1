import socket
import sys
import time

def checker(message):
    # Splits the message into tokens based on spaces
    tokens = message.split(' ')

    # Prints the last character of the last token
    print(tokens[-1][-1])

    # Checks if the message has 5 tokens and ends with a newline character
    if len(tokens) == 5 and tokens[-1][-1] == '\n':
        return True
    else:
        return False

def parser(message):
    # Splits the message into tokens and returns specific parts
    tokens = message.split(' ')
    return tokens[1], int(tokens[2]), int(tokens[3]), int(tokens[4])

def probChecker(message, p):
    # Splits the message into tokens
    tokens = message.split(' ')
    print(f"{tokens[0]} {tokens[1]} {tokens[2]} \n")

    # Checks if the message has 3 tokens, starts with "m", has the correct probability number, and ends with a newline
    if len(tokens) == 3 and tokens[0] == "m" and int(tokens[1]) == p and tokens[2][-1] == '\n':
        print("probChecker is true")
        return True
    else:
        return False

def delayTime(nanosec):
    # Introduces a delay of nanoseconds by using a busy wait loop
    start_time = time.perf_counter()
    end_time = start_time + nanosec / 1_000_000_000
    while time.perf_counter() < end_time:
        pass
    return

def server(port):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the given port on localhost
    server_address = ('localhost', port)
    print(f'Starting up on {server_address[0]} port {server_address[1]}')
    sock.bind(server_address)

    # Listen for incoming connections (1 at a time)
    sock.listen(1)

    # Global variables for tracking measurement parameters
    measurementType = ""
    numProb = -1
    messageSize = -1
    serverDelay = -1
    currentProb = 1

    while True:
        # Wait for a connection
        print('Waiting for a connection')
        connection, client_address = sock.accept()
        try:
            print(f'Connection from {client_address}')

            # Receive and process data from the client
            while True:
                data = connection.recv(1000)  # Receive up to 1000 bytes of data
                print(f'Received: {data.decode()}')

                if data:
                    # If connection setup message is valid
                    if checker(data.decode()):
                        connection.send("200 OK: Ready".encode())
                        
                        # Parse the connection setup message
                        measurementType, numProb, messageSize, serverDelay = parser(data.decode())
                        print(f'Measurement: {measurementType}, Number of Probabilities: {numProb}, Message Size: {messageSize}, Server Delay: {serverDelay}')
                        
                        # Handle the messages for each probability
                        while currentProb <= numProb:
                            # Calculate the size of the sequence number in bytes and total packet size
                            sequenceInBytes = (numProb.bit_length() + 7) // 8 or 1
                            packetSize = messageSize + sequenceInBytes + 4
                            
                            # Receive the message
                            data = connection.recv(packetSize + 1)
                            message = data.decode()

                            print("message:", message)
                            print("currentProb:", currentProb)
                            print("numProb:", numProb)

                            # Check if the message is valid for the current probability
                            if probChecker(message, currentProb):
                                # Apply delay before sending the response
                                delayTime(serverDelay)
                                currentProb += 1
                                print(f'Sending: {message}')
                                connection.send(message.encode())  # Send back the same message
                            else:
                                connection.send("404 ERROR: Invalid Measurement Message".encode())
                                break
                        
                        # Handle termination message
                        data = connection.recv(4096)
                        print(f'Received: {data.decode()}')
                        if data.decode() == 't\n':
                            print('Received termination message from client')
                            connection.send("200 OK: Closing Connection".encode())
                            break
                        else:
                            connection.send("404 ERROR: Invalid Connection Termination Message".encode())
                            break

                    else:
                        # Send error if connection setup message is invalid
                        connection.send("404 ERROR: Invalid Connection Setup Message".encode())
                        break

                else:
                    # No more data from the client
                    print(f'No more data from {client_address}')
                    break
                
        finally:
            # Close the connection after processing
            connection.close()
            break

if __name__ == '__main__':
    # Ensure the script is run with a valid port argument
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        sys.exit(1)
    
    port = int(sys.argv[1])
    
    # Ensure the port is within the valid range
    if port < 58000 or port > 58999:
        print("Port must be in the range 58000-58999")
        sys.exit(1)
    
    # Start the server with the specified port
    server(port)
