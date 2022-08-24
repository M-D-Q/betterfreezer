#!/bin/bash

# download and launch title (need to check existence before)
function get_music {
        USER=$1
        SERVEUR=$2
        file_name=$3
        sftp $USER@$SERVEUR <<END_SCRIPT
        bell
        get "$file_name"
END_SCRIPT

        mpv "$file_name"
}

function main_loop {
USER=$1
#list musics in server
sftp $USER@$SERVEUR <<END_SCRIPT
cd Musics
ls
END_SCRIPT

#allow user to check for a music with keyword
cd /home/$USER/Musics2
read -p "Recherche :" MUSIC
KEK=$MUSIC 
liste_recherche=$(ls *$MUSIC* 2> /dev/null 1> /dev/null)
echo "Music Found: $liste_recherche"

# if music not found in local
if [[ -z $liste_recherche ]]
then
    #we check the server
    ssh $USER@$SERVEUR -o SendEnv=KEK /bin/bash << 'ENDSCRIPT'
    MUSIC=$(printenv | grep KEK | cut -d = -f2)

    echo "coucou avant tout"
    echo $MUSIC
    cd /home/$USER/Musics/
    echo "coucou avant recherhce"
    liste_recherche="$(ls /home/$USER/Musics/*$MUSIC*)"
    echo $liste_recherche
    
    # if music not in server, we download it
    echo "coucocu avant if"
    if [[ -z "$liste_recherche" ]]
    then
        echo "coucou dans if"
        output_file=\$\(python /home/maxlarbs/.local/bin/spotdl $MUSIC\)
        #sed '\''s/\"/\\\"/g\'\''
        echo kek1
        echo "$output_file"
        title_music="$(echo "$output_file" | grep "YouTube" | cut -dy -f 2 )"
        echo kek2
        echo $title_music
        exit
        echo kek3
        get_music $USER $SERVEUR "$title_music"
    else
        echo "coucou dans else"
        #we download it on the local side
        exit
        echo kek4
        get_music $USER $SERVEUR "$title_music"
        echo kek5
    fi
ENDSCRIPT

else
    #music is on local side. Just need to launch it.
    echo "coucou premier else"
    mpv "$(echo "$liste_recherche" | head -n1)"
fi
}


SERVEUR=$1
USER=$2

choice=n
while [[ $choice = n ]]
do
    echo $choice
    main_loop $USER
    read -p "Wanna leave, bro? y/n " choice
    echo "$choice apres imput"
    if [[ $choice = y ]]
    then
        echo "Au revoir, bro."
        echo $choice
    fi

done