import sys
import mariadb

class Maria():
    def __init__ (self):
    #def __init__ (self,user,password,host,port,db):
        # https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/
        try:
            self.conn = mariadb.connect(
                user="freezer",
                password="freezer",
                host="localhost",
                port=3306,
                database="freezer_db"
                )

            # Get Cursor
            self.cur = self.conn.cursor()

        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

    def list_playlists(self, user):
    #list all of the user's playlists
    #additional columns in the select for testing purposes
        self.cur.execute("""SELECT playlists.name, users.id, playlists.user_id FROM playlists
        INNER JOIN users ON playlists.user_id=users.id
        WHERE users.name = ?; """,(user))
        return self.cur
        # aesthetics
        print("================ Playlists ==============")
        print("playlists.name, users.id, playlists.user_id")
        for line in self.cur:
            print(line)
        print("================ Finished  ==============")

    #list all songs contained in one playlist
    def playlist_content(self, playlist_id):
        self.cur.execute("""SELECT playlist_songs.id, songs.name, artists.name, playlists.name 
        FROM playlist_songs
        INNER JOIN songs ON playlist_songs.song_id=songs.id
        INNER JOIN artists ON songs.artist_id=artists.id
        INNER JOIN playlists ON playlist_songs.playlist_id=playlists.id
        WHERE playlists.name = ?; """,(playlist_id))
        return self.cur
        # aesthetics
        print("==============Playlist Content============")
        print("playlist_songs.id, songs.name, artists.name, playlists.name")
        for line in self.cur:
            print(line)
        print("================  Finished  ==============")

    # add song into database
    def add_song_database(self,artist_name,song_name,filename):
        #First add artist | Try 1st time without "try", then do it with try except
        #if artist exists, then add song
        #if artist doesnt exist, then add him, then add song.
        self.cur.execute("INSERT INTO artists (name) VALUES (?);",(artist_name))
        self.conn.commit()
        #NEED to manage for duplicate artists

        #Then add song
        #self.cur.execute("INSERT INTO songs (name, filename) VALUES (?,?)",(song_name,filename))
        #add the artist_id found using the artist_name 
        self.cur.execute("""INSERT INTO songs (artist_id, name, filename)
                SELECT id
                , ? AS name
                , ? AS filename
                FROM artists
                WHERE name=?""",(song_name, filename, artist_name))
        self.conn.commit()

    def create_playlist(self, user, playlist_name):
        self.cur.execute("""INSERT INTO playlists (user_id, name)
                SELECT id
                , ? AS name
                FROM users
                WHERE name=?;""",(playlist_name, user))
        self.conn.commit()


    def add_song_playlist(self, song_id, playlist_id ):
        #A tester fortement!
        self.cur.execute("""INSERT INTO playlist_songs (song_id, playlist_id)
                SELECT songs.id
                , playlists.id
                FROM playlist_songs
                INNER JOIN songs ON playlist_songs.song_id=songs.id
                INNER JOIN playlists ON playlist_songs.playlist_id=playlists.id
                WHERE songs.id=? AND playlists.id=?;""",(song_id, playlist_id))
        self.conn.commit()

        
"""While inserting rows, you may want to find the Primary Key of the last inserted row when 
it is generated, as with auto-incremented values. You can retrieve this using the lastrowid() method on the cursor."""
