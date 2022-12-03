import socket
import threading

HOST = "localhost"
PORT = 9090

# indicates that we are gonna use IPV4 and TCP protocol.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT)) # socket binding to given IP address and port number

server.listen()

clients = []
usernames = []


#broadcast (here, message arg should be encoded by utf-8 )
def broadcast(message):
    for client in clients:
        client.send(message)



#handling
def handle(client):
    while True:

        try:
            
            # if things regarding this client's connection all goes well
            #  take the message and broadcast it to all users.
            message = client.recv(1024)
            print(f"{usernames[clients.index(client)]} is saying {message}")
            broadcast(message)

        except:
            # if a connection or another error occurs
            # close this client's connection and then remove its username
            index_of_client = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index_of_client]
            usernames.remove(username)
            break





#receive
def receive():
    while True:
        client , address = server.accept()
        print(f"{str(address)} just connected .")

        # wanting user to type its username :
        client.send("USERNAME : ".encode('utf-8'))
        username = client.recv(1024)
        usernames.append(username)

        print( f"Username of the client is {username}")
        broadcast(f"{username} connected to the server ! \n".encode('utf-8'))
        client.send("Connected to the server.".encode('utf-8'))

        thread = threading.Thread(target=handle, args = (client,))
        thread.start()

print("Server has just been started !")
receive()
