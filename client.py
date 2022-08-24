import socket
import sys

HOST = '10.125.24.64'    # The remote host
PORT = 1233            # The same port as used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

print("Welcome to the future of music streaming")

print("""Type in : 'bye' to exit
        'list' to view your songs
        'play $MUSIC' to play the track of your choice""")

server = True
while server:
    msg=input("message to send: ")
    if msg == "list":
        s.send(msg.encode())
        response = s.recv(2048)
        print(response.decode('utf-8'))
    elif msg == "play":
        s.send(msg.encode())
        response = s.recv(2048)
        print(response.decode('utf-8'))
    elif msg == "bye":
        break
    else:
        print("Invalid command line")
    data = s.recv(1024)
    print('Received', data.decode())

s.close()
