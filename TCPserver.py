import socket
import json
import time
import os
from cryptography.fernet import Fernet
import base64

chatResponder = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('', 6001)  # Use port 6001 for chat
chatResponder.bind(server_address)
chatResponder.listen(1)  # Listen for incoming connections (backlog of 1)

print("TCPserver is listening...")


def save_chat_log(username, message):
    folder = 'logs'
    if not os.path.exists(folder):
        os.makedirs(folder)
    file_path = os.path.join(folder, f'{username}.txt')
    with open(file_path, 'a') as file:
        file.write(f'{time.ctime()} | {username}: {message}\n')


while True:
    # Accept incoming connection
    client_socket, client_address = chatResponder.accept()
    returnIP = client_address[0]
    json_payload = json.loads(client_socket.recv(1024).decode())
    username = json_payload['user']
    if json_payload.get('key') == 0:
        print(f"{username}: {json_payload.get('unencrypted_message')}")
        save_chat_log(username, json_payload.get('unencrypted_message'))
        client_socket.close()
    else:
        secretkey = int(input("enter your key: "))
        key = (5 ^ secretkey) % 23
        client_socket.send(str(key).encode())
        finalkey = (int(json_payload['key']) ^ secretkey) % 23
        integer_bytes = int.to_bytes(finalkey, length=32, byteorder='big')
        fernet_key = base64.urlsafe_b64encode(integer_bytes)
        f = Fernet(fernet_key)
        received_data = client_socket.recv(2048)
        if received_data:
            json_payload = json.loads(received_data.decode())
            message = json_payload.get("encrypted_message")
            if message:
                decrypted_message = f.decrypt(base64.b64decode(message)).decode()
                print(f"{username}: {decrypted_message}")
                save_chat_log(username, decrypted_message)
        client_socket.close()
