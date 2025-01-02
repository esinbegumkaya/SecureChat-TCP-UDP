import socket
import json
import time


# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Server address and port
serverUDPaddress = ('', 6000)

# Client username
client_id = input("Write your username:")

# Storeing your username in a json format
username = {'username': client_id}
file_path = 'username.json'

# Write the variable to the JSON file
with open(file_path, 'w') as file:
    json.dump(username,file)

username = json.dumps({'username': client_id})


print(f"Welcome {client_id}")
print("connecting to server")

while True:
    # Send periodic announcements to the server
    client_socket.sendto(username.encode(), serverUDPaddress)


    # Wait for a while before sending the next announcement
    time.sleep(8)  # Adjust as needed for periodic announcements