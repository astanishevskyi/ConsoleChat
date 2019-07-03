import select
import socket
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# check whether sufficient arguments are provided
if len(sys.argv) != 3:
    print('Try again')
    sys.exit()

HOST = str(sys.argv[1])  # take first argument as IP address
PORT = int(sys.argv[2])  # take second argument as port number

server.connect((HOST, PORT))  # connect to the server with parameters HOST and PORT

while True:
    socket_list = [sys.stdin, server]
    print(socket_list)
    read_socket, write_socket, err_socket = select.select(socket_list, [], [])

    for sock in read_socket:
        if sock == server:
            message = sock.recv(2048)
            # print(message)
        else:
            message = sys.stdin.readline()
            server.send(bytes(message, 'utf-8'))
            sys.stdout.write('<You> ')
            sys.stdout.write(message)
            sys.stdout.flush()

server.close()
