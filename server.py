import socket
import threading
import wave
import pyaudio
import database
import pytube

HOST = '10.125.24.64'
PORT = 1233
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


# default value for testing purposes
user_name = "bidon"


def download_video(key_word):
    """Takes the first result by default"""
    search_result = pytube.Search(key_word)
    only_audio_results = search_result.results[0].streams.filter(only_audio=True)
    stream = only_audio_results[0]
    file_path = stream.download()
    return file_path


def client_handler(connection):
    """The guy who talks with the client"""
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
            # we search on the server if we haven't downloaded the video yet
            # ok smart boy. How do I get the song id with just a keyword, huh?
            song_id = -1
            if song_id > 0:
                file_path = db_manager.fetch_song_filename(song_id)
            # if the video isn't downloaded yet
            else:
                title = message.split(" ")[1]
                file_path = download_video(title)
            streaming_audio(file_path, connection)


def accept_connections(server_socket):
    """Setup the communication between the server and a client"""
    client, address = server_socket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    t = threading.Thread(target=client_handler, args=(client,))
    t.start()


def start_server(host, port):
    """server setup"""
    server_socket = socket.socket()
    try:
        server_socket.bind((host, port))
    except socket.error as e:
        print(str(e))
    print(f'Server is listing on the port {port}...')
    server_socket.listen()

    while True:
        accept_connections(server_socket)


start_server(HOST, PORT)
