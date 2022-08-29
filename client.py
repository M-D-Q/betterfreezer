import socket
import glob
import os
import pyaudio
from constants import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

print(WELCOME_MESSAGE_CLIENT )

print(CLIENT_HELP)

# Audio
FORMAT = pyaudio.paInt16
CHUNK = 1024
CHANNELS = 1
RATE = 44100
WAVE_OUTPUT_FILENAME = "output.wav"
p = pyaudio.PyAudio()
frames = []


# Connexion
user_name = input(ENTER_NAME)
s.send(user_name)
valid = False
while not valid:
    data = s.recv(1024)
    print('Server:', data.decode())
    if data.decode() == CREATE_ACCOUNT or data.decode() == PASSWORD_QUESTION \
            or data.decode() == CHOOSE_PASSWORD:
        message = input()
        s.send(message.encode())
    elif VALIDED in data.decode():
        valid = True
server = True
while server:
    msg = input(MESSAGE_TO_SEND)
    if msg == ASK_LIST:
        s.send(msg.encode())
        response = s.recv(2048)
        print(response.decode('utf-8'))
    elif PLAY_KEY_WORD in msg:
        # need to verify if the music is here locally
        # need to think of a better command analysis
        key_word = msg.split(" ")[1]
        possible_findings = glob.glob(f"Musics/*{key_word}*")
        if len(possible_findings) > 0:
            print(possible_findings)
            choice = input(CHOOSE_MUSIC)
            os.system(f"mpv '{possible_findings[int(choice)]}'")
        # otherwise, ask for it on the server
        else:
            s.send(msg.encode())
            stream = p.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            output=True,
                            frames_per_buffer=CHUNK)
            while True:
                try:
                    # read data
                    data = s.recv(CHUNK)
                    # play stream (3)
                    stream.write(data)
                except socket.error as error_message:
                    break
            # stop stream (4)
            stream.stop_stream()
            stream.close()
    elif msg == "bye":
        break
    else:
        print(ERR_INVALID_COMMAND)
    data = s.recv(1024)
    print('Received', data.decode())

s.close()

