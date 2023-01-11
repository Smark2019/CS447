import socket
import threading


def connectionen():

    global server, username, message_handler, input_handler

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            HOST = input("host ip: ")
            PORT = int(input("host port: "))
            server.connect((HOST, PORT))
            break
        except:
            print("connection to host failed")

    username = input("Enter a username: ")
    print("Me"+" => ",end="")
    server.send(username.encode())

    message_handler = threading.Thread(target=handle_messages, args=())
    message_handler.start()

    input_handler = threading.Thread(target=input_handler, args=())
    input_handler.start()


def handle_messages():
    while True:
        print(server.recv(1024).decode())


def input_handler():
    while True:
        server.send((username + ': ' + input()).encode())
        print("Me"+" => ",end="")


connectionen()
