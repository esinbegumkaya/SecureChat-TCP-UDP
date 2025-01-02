import socket
import json
import time


server_address = ('', 6000)
# Dictionary to store client information (indexed by username and IP address)

clients = {}

def saveClientList(data):
    # File path to the JSON file
    file_path = 'data.json'

    # Write the variable to the JSON file
    with open(file_path, 'w') as file:
        json.dump(data, file)


print("Server is listening on", server_address)
    # Create a UDP socket for server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set socket options to allow multiple sockets to bind to the same port
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    # Bind the UDP socket to the server address and port
server_socket.bind(server_address)
while True:
    # Receive message from client
    data, client_address = server_socket.recvfrom(1024)

    # Parse JSON data
    json_data = json.loads(data.decode())
    username = json_data.get('username')
    # Store client information along with the current timestamp
    clients[username] = (client_address[0] , time.time())
    # Send the list of available users to the client

    saveClientList(clients)
    
    time.sleep(8)  # Adjust as needed for periodic announcements
