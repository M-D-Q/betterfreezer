#!/bin/sh

# constantes
HOST=10.5.0.6
LOGIN=test
PASSWORD=test
PORT=21
FILENAME=$1

# le telecharggement de la musique
ftp -i -n $HOST $PORT << END_SCRIPT
quote USER $LOGIN
quote PASS $PASSWORD
cwd /music_share
mget $FILENAME
quit
END_SCRIPT

