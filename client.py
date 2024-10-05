import socket
import sys
import time

def client(host, port, measurement, numProb, size, serverDelay):
    #Time Measurement (Still need to implement)
    beforeTime = []
    afterTime = []
    
    # Create socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Make connect the socket + port to where the listening server
    server_address = (host, port)
    print(f'Connecting to {server_address[0]} port {server_address[1]}')
    sock.connect(server_address)

    try:
        # Send data
        message = f"s {measurement} {numProb} {size} {serverDelay}\n"

        print(f'Sending: {message}')
        sock.send(message.encode())

        # Await response
        amount_received = 0
        amount_expected = len(message)
        
        greenLight = False #Green light to send more messages
        while amount_received < amount_expected:
            data = sock.recv(1000)
            amount_received += len(data)
            print(f'Received: {data.decode()}')
            if 'Ready' in data.decode():
                greenLight = True
                print('Green light to send more messages')
                break
        
        if greenLight:
            i = 1
            while numProb >= i:
                # Start time of send
                beforeTime.append(time.perf_counter())
                message = f"m {i} {size * '1'}\n"
                print(f'Sending: {message}')
                
                sock.send(message.encode())
                i += 1
                # Wait for server response
                amount_received = 0
                amount_expected = len(message)
                while amount_received < amount_expected:
                    sequenceInBytes = (numProb.bit_length() + 7) // 8 or 1
                    data = sock.recv(max((size + 5 + sequenceInBytes), len("404 ERROR: Invalid Connection Setup Message")))
                    # Stop time of recv
                    afterTime.append(time.perf_counter())
                    amount_received += len(data)
                    print(f'Received: {data.decode()}')

                    if '404' in data.decode():
                        print('Server responded with 404 error')
                        break
                
            message = "t\n"
            print(f'Sending: {message}')
            sock.send(message.encode())
            print('Sent termination message to server')

    finally:
        print('Closing socket')
        sock.close()

    # Calculate RTT
    rtt_values = []
    for i in range(len(beforeTime)):
        rtt_values.append(afterTime[i] - beforeTime[i])   

    # Calculate TPUT
    if (measurement == "tput"):
        tput_values = []
        for i in range(len(beforeTime)):
            # Calculate num bytes used
            sequenceInBytes = (numProb.bit_length() + 7) // 8 or 1
            packetSize = size + sequenceInBytes + 4 # protocl letter, two spaces, \n
            tput_values.append(packetSize / (rtt_values[i] * 1))

        print(f"TPUT avg: {sum(tput_values) / len(tput_values):.3f} Bps")

        """ print("TPUT values:")
        for i in range(len(tput_values)):
            print(f"TPUT for message {i+1}: {tput_values[i]:.3f} Mbps") """ 
        
    else: 
        """ print("RTT values:")
        for i in range(len(rtt_values)):
            print(f"RTT for message {i+1}: {rtt_values[i]*1_000_000_000:.3f} ns") 
         """

        print(f"RTT avg: {sum(rtt_values) / len(rtt_values)*1_000_000_000:.3f} ns") 

if __name__ == '__main__':
    if len(sys.argv) != 7:
        print("Usage: python client.py <host> <port> <measurement> <numProb> <size> <serverDelay>")
        sys.exit(1)
    
    host = sys.argv[1]
    port = int(sys.argv[2])
    measurement = sys.argv[3]
    numProb = int(sys.argv[4])
    size = int(sys.argv[5])
    serverDelay = int(sys.argv[6])
    if port < 58000 or port > 58999:
        print("Port must be in the range 58000-58999")
        sys.exit(1)
    
    client(host, port, measurement, numProb, size, serverDelay)

def rtt(size):
    pass
def tput(size):
    pass
