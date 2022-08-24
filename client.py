import socket
import sys

HOST = '127.0.0.1'    # The remote host
PORT = int(sys.argv[1])              # The same port as used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

print("""Type in : 'quit' to exit
        'list' to view your songs
        'play $MUSIC' to play the track of your choice""")

server = True
while server:
    msg=input("message to send: ")
    if msg == "list" :
        s.sendall(msg.encode())
    elif msg == "play":
        s.sendall(msg.encode())
    elif msg == "quit()" :
        break
    else :
        print("Invalid command line")
    data = s.recv(1024)
    print('Received', data.decode())

s.close()
