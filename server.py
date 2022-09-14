import socket
import threading
import wave
import pyaudio
import database
import pytube

HOST = '10.5.0.4'
PORT = 1233
CHUNK = 1024
db_manager = database.Maria()
PASSWORD_TRY = 3

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


def download_video(key_word):
    """Takes the first result by default"""
    search_result = pytube.Search(key_word)
    only_audio_results = search_result.results[0].streams.filter(only_audio=True)
    stream = only_audio_results[0]
    file_path = stream.download()
    return file_path


def client_handler(connection):
    """The guy who talks with the client"""
    # Fist, gonna check if they already exist
    user_name = connection.recv(2048).decode()
    user_id = db_manager.check_username_existence(user_name)
    valid = True
    if user_id < 0:
        # user doesn't exist. Signing up.
        connection.send(f"Do you want to create an account, {user_name}".encode())
        data = connection.recv(2048).decode()
        if data == "yes":
            connection.send(f"Choose a password".encode())
            password = connection.recv(2048).decode()
            db_manager.add_user(user_name, password)
            valid = True
            connection.send("valided".encode())
        else:
            return -1
    else:
        # user exist. Asking for password
        number_of_tries = 0
        while number_of_tries < PASSWORD_TRY and not valid:
            number_of_tries += 1
            connection.send(f"Password ?".encode())
            password = connection.recv(2048).decode()
            valid = db_manager.check_user_password(user_name, password)
    if valid:
        connection.send("valided".encode())
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
                list_musics_in_playlist = db_manager.playlist_content()
                connection.send(str.encode(list_musics_in_playlist.encode))
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
    return 0


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
