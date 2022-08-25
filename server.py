import socket
import threading
import wave
import pyaudio
import database

host = '10.125.24.64'
port = 1233
CHUNK = 1024
db_manager = database.Maria()


def streaming_audio(title, s):
    wf = wave.open(title, 'rb')

    # instantiate PyAudio (1)
    p = pyaudio.PyAudio()

    # open stream (2)
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # read data
    data = wf.readframes(CHUNK)

    # play stream (3)
    while len(data):
        stream.write(data)
        data = wf.readframes(CHUNK)
        s.send(data)

    # stop stream (4)
    stream.stop_stream()
    stream.close()

    # close PyAudio (5)
    p.terminate()

#default value for testing purposes
user_name = "bidon"


def client_handler(connection):
    connection.send(str.encode('You are now connected to the replay server... Type bye to stop'))
    continue_com = True
    while continue_com:
        data = connection.recv(2048)
        message = data.decode('utf-8')
        if message == 'bye':
            connection.close()
            continue_com = False
        elif message == "liste":
            liste_playlists = db_manager.list_playlists(user_name)
            reply = f'Liste of musics:\n {str(liste_playlists)}'
            connection.sendall(str.encode(reply))
        elif "playlist" in message:
            liste_musics_in_playslists = db_manager.playlist_content()
        else:
            streaming_audio("Musics/Fanfare60.wav", connection)


def accept_connections(server_socket):
    client, address = server_socket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    t = threading.Thread(target=client_handler, args=(client,))
    t.start()


def start_server(host, port):
    server_socket = socket.socket()
    try:
        server_socket.bind((host, port))
    except socket.error as e:
        print(str(e))
    print(f'Server is listing on the port {port}...')
    server_socket.listen()

    while True:
        accept_connections(server_socket)


start_server(host, port)
