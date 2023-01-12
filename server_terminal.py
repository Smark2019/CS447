import socket
import threading


HOST = '0.0.0.0'        # ip address of server machine
PORT = 9090             # port number of the socket
ADDR = (HOST, PORT)

clients = []            # list for keeping clients' sockets
username_lookup = {}    # dict structure for client & username matches


def start():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # server socker definition by IPV4 and usage of TCP Protocol.

    server.bind(ADDR) # defined socket binded to given addres (host_ip , port_number)
    server.listen(100) # queue def.

    print('Running on host: '+str(HOST))
    print('Running on port: '+str(PORT))

    while True:
        conn, addr = server.accept()                     # continously, new connections and their address' accepted.
        username = conn.recv(1024).decode()              # based on rules, first message should be username

        print('New user entered chat: ' + str(username))
        broadcast('New user entered chat: ' + str(username))  # all other clients are receiving given welcome message.

        username_lookup[conn] = username        # client's socket and its username are matched in the dict structure

        clients.append(conn)                    # new client added into clients list.

        threading.Thread(target=handle_client, args=(conn, addr)).start() # new thread started for this new client


def broadcast(msg): # broadcast func to distribute a message to all clients in the chat 
    for connection in clients:
        connection.send(msg.encode())


def handle_client(conn, addr): # for every client, this func is run separately
    while True:
        try:
            msg = conn.recv(1024) # try to get message
        except:                   # under any error for regarding client, remove it from list.
            clients.remove(conn)  
            print(str(username_lookup[conn] + " left the chat."))
            broadcast(str(username_lookup[conn] + " left the chat."))  # sends informative message for rest of the clients
            break
        if msg.decode != "":
            print("[New Message] " + str(msg.decode()))
            for connection in clients:      # The message which is not empty, are sent to all other clients.s
                if connection != conn:
                    connection.send(msg)    


start() # init the server
