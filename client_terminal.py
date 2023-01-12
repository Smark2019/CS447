import socket
import threading


def init_connection():

    global server, username, message_handler, input_handler

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # server socker definition by IPV4 and usage of TCP Protocol.
    while True:
        try:                                               # asks user to give the server address and port number 
            HOST = input("host ip: ")
            PORT = int(input("host port: "))
            server.connect((HOST, PORT))                   # server connection is established
            break
        except:
            print("connection to host failed")

    username = input("Enter a username: ")
    while username == "":
        username = input("Enter a username: ")
    print("Me"+" => ",end="")
    server.send(username.encode())          # based on rule, username of the client (first message) automatically sent to server.

    message_handler = threading.Thread(target=handle_messages, args=()) # thread for coming messages from rest of the clients.
    message_handler.start()

    input_handler = threading.Thread(target=handle_input, args=()) # thread for client's sending message for rest of the clients.
    input_handler.start()


def handle_messages():
    while True:
        print(server.recv(1024).decode())  # prints coming messages to the terminal


def handle_input():
    while True:
        server.send((username + ': ' + input()).encode()) # sends the message of the client to rest of the clients with the its username
        print("Me"+" => ",end="")


init_connection() # initilize the connection to the server.
