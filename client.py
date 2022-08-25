import socket
import glob
import os
import pyaudio
import wave

HOST = '10.125.24.64'  # The remote host
PORT = 1233  # The same port as used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

print("Welcome to the future of music streaming")

print("""Type in : 'bye' to exit
        'list' to view your songs
        'play $MUSIC' to play the track of your choice""")

# Audio
FORMAT = pyaudio.paInt16
CHUNK = 1024
CHANNELS = 1
RATE = 44100
WAVE_OUTPUT_FILENAME = "output.wav"
p = pyaudio.PyAudio()
frames = []

# Welcome message
data = s.recv(1024)
print('Received', data.decode())
server = True
while server:
    msg = input("message to send: ")
    if msg == "liste":
        s.send(msg.encode())
        response = s.recv(2048)
        print(response.decode('utf-8'))
    elif "play" in msg:
        # need to verify if the music is here locally
        # need to think of a better command analysis
        key_word = msg.split(" ")[1]
        possible_findings = glob.glob(f"Musics/*{key_word}*")
        if len(possible_findings) > 0:
            print(possible_findings)
            choice = input("Which music do you want to listen to? Enter the index")
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
        print("Invalid command line")
    data = s.recv(1024)
    print('Received', data.decode())

s.close()

