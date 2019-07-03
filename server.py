import socket
from threading import Thread
from sys import argv

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create a socket with parameters IPv4 and TCP-connection
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # add socket option to reuse address


# check whether sufficient arguments are provided
if len(argv) != 3:
    print('Write sript, host, port')
    exit()

HOST = str(argv[1])  # take first argument as IP address
PORT = int(argv[2])  # take second argument as port number

server.bind((HOST, PORT))  # bind the server to the entered IP address and port number
server.listen(10)  # listen for 10 active connections

clients_list = []


def broadcast(message, connection):
    '''
    This function sends the message to all clients who's client is not the same as the sender of message
    '''
    for client in clients_list:

        try:
            client.send(bytes(message, 'utf-8'))
        except:
            print('debil')
            client.close()

            # if link is broken, we remove the client
            remove(client)


def remove(connection):
    '''
    Remove the object from client_list (close connection with client)
    '''
    if connection in clients_list:
        clients_list.remove(connection)


def clientthread(conn, addr):
    # send the message to client who just joined a chatroom
    conn.send(bytes('Welcome to the chatroom', 'utf-8'))

    while True:

        try:
            message = conn.recv(1024)  # fucking bug

            if message:

                # print(message)

                # print the message and user's address who sent message
                print('<' + addr[0] + '>' + str(message))
                # call broadcast function to send to all users
                message_to_send = "<" + addr[0] + ">" + str(message)
                broadcast(message_to_send, conn)
            else:
                # print('xyi')
                remove(conn)

        except:
            continue


while True:
    # accept a connection request and contain two parameters
    # conn is a socket object for user
    # addr contains IP address of the client who just connected
    conn, addr = server.accept()

    clients_list.append(conn)  # add client in client_list

    Thread(target=clientthread, args=(conn, addr)).start()  # create new thread for every user that connect

conn.close()
server.close()
