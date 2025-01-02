import socket
import json
import time
import os
from cryptography.fernet import Fernet
import base64

with open('username.json', 'r') as file:
    user = json.load(file)
    username = user['username']

def display_available_users():
    global data
    file_path = 'data.json'
    # Read the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    current_time = time.time()
    available_users = "Available users:\n"
    for username, client_info in data.items():
        last_seen = client_info[1]  # Get the last seen timestamp from the client info tuple
        if current_time - last_seen < 10:
            status = "(Online)"
        elif current_time - last_seen >= 10:
            status = "(Away)"
        elif current_time - last_seen >= 900:
            del data[username]
        available_users += f"{username} {status}\n"
    print(available_users)

def save_chat_log(username, message, client):
    folder = 'logs'
    if not os.path.exists(folder):
        os.makedirs(folder)
    file_path = os.path.join(folder, f'{client}.txt')
    with open(file_path, 'a') as file:
        file.write(f'{time.ctime()} | {username}: {message}\n')

def history(client):
    folder = 'logs'
    if not os.path.exists(folder):
        print("no chat logs available")
        return
    file_path = os.path.join(folder, f'{client}.txt')
    if not os.path.exists(file_path):
        print(f"no chat history with {client}")
        return
    with open(file_path,'r') as file:
        print(file.read())

def chat():
    chatInitiator = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_ID = input("who do you want to chat with? ")
    addr = (data[client_ID][0], 6001)
    chatInitiator.connect(addr)
    secure = input("1 for encrypted chat, 2 for unencrypted chat: ")
    if secure == '1':
        secretKey = int(input("choose your secret key: "))
        key = ((5^secretKey) % 23)
        json_payload = {"user": username, "key": key}
        chatInitiator.send(json.dumps(json_payload).encode())      
        tempkey = chatInitiator.recv(2048).decode()
        if tempkey:
            finalkey = (int(tempkey) ^ secretKey) % 23
            integer_bytes = int.to_bytes(finalkey, length=32, byteorder='big')
            fernet_key = base64.urlsafe_b64encode(integer_bytes)
            f = Fernet(fernet_key)

            message = input('message: ')
            encrypted_message_bytes = f.encrypt(message.encode())
            encrypted_message_base64 = base64.b64encode(encrypted_message_bytes).decode()
            json_payload = {"user": username, "encrypted_message": encrypted_message_base64}
            chatInitiator.send(json.dumps(json_payload).encode())
            save_chat_log(username, message, client_ID)
    elif secure == '2':
        message = input("message: ")
        key = 0
        unencrypted_message = message
        json_payload = {"user": username, "key": key, "unencrypted_message": unencrypted_message}
        chatInitiator.send(json.dumps(json_payload).encode())
        save_chat_log(username, message, client_ID)
    chatInitiator.close()

def mainMenu():
    print("1. Users")
    print("2. Chat")
    print("3. History")
    nav = input("What do you want to do? (use the numbers): ")
    if nav == '1':
        display_available_users()
    elif nav == '2':
        chat()
    elif nav == '3':
        client = input("Who's chat history do you want to see? ")
        history(client)
    else:
        print("invalid input")

while True:
    mainMenu()
