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
        self.cur.execute("""SELECT playlists.name, playlists.id, users.id, playlists.user_id FROM playlists
        INNER JOIN users ON playlists.user_id=users.id
        WHERE users.name = ?; """,(user))
        #return self.cur
        # aesthetics
        result=[]
        print("================ Playlists ==============")
        print("playlists.name, users.id, playlists.user_id")
        for line in self.cur:
            result.append(line)
            print(line)
        print("================ Finished  ==============")
        return result


    #list all songs contained in one playlist
    def playlist_content(self, playlist_id):
        self.cur.execute("""SELECT playlist_songs.id, songs.name, songs.id, artists.name, playlists.name 
        FROM playlist_songs
        INNER JOIN songs ON playlist_songs.song_id=songs.id
        INNER JOIN artists ON songs.artist_id=artists.id
        INNER JOIN playlists ON playlist_songs.playlist_id=playlists.id
        WHERE playlists.id = ?; """,(playlist_id,))
        #return self.cur
        # aesthetics
        result = []
        print("==============Playlist Content============")
        print("playlist_songs.id, songs.name, artists.name, playlists.name")
        for line in self.cur:
            result.append(line)
            print(line)
        print("================  Finished  ==============")
        return result

    # add song into database
    def add_song_database(self,artist_name,song_name,filename):
        #First add artist | Try 1st time without "try", then do it with try except
        #if artist exists, then add song
        #if artist doesnt exist, then add him, then add song.
        try :
            print("coucou dans try)")
            self.cur.execute("INSERT INTO artists (name) VALUES (?);",(artist_name,))
            self.cur.execute("""INSERT INTO songs (artist_id, name, filename)
                SELECT id
                , ? AS name
                , ? AS filename
                FROM artists
                WHERE name=?""",(song_name, filename, artist_name,))
        except :
            print("coucou dans except")
            self.cur.execute("""INSERT INTO songs (artist_id, name, filename)
                SELECT id
                , ? AS name
                , ? AS filename
                FROM artists
                WHERE name=?""",(song_name, filename, artist_name,))
        self.conn.commit()
    

    def create_playlist(self, user, playlist_name):
        self.cur.execute("""INSERT INTO playlists (user_id, name)
                SELECT id
                , ? AS name
                FROM users
                WHERE name=?;""",(playlist_name, user,))
        self.conn.commit()


    def add_song_playlist(self, song_id, playlist_id ):
        self.cur.execute("""INSERT INTO playlist_songs (song_id, playlist_id)
                VALUES (?,?);""",(song_id, playlist_id,))
        self.conn.commit()

# ADD USER
    def add_user(self, username, password):
        self.cur.execute("INSERT INTO users (name, password) VALUES (?, ?);",(username, password,))
        self.conn.commit()
    
    def add_user_full(self, username, password):
        self.add_user(username, password)
        self.create_playlist(username, "My Songs")

# CHECK USER CREDENTIALS ON LOGIN
    def check_user(self, username, password):
        self.cur.execute("""SELECT name, password,
        CASE password
            WHEN ? THEN
        FROM users
        WHERE name=?;""",(song_id, playlist_id,))
        
"""While inserting rows, you may want to find the Primary Key of the last inserted row when 
it is generated, as with auto-incremented values. You can retrieve this using the lastrowid() method on the cursor."""

if __name__ == "__main__":
    toast = Maria()
    #toast.add_song_database("M2iCloudDevops", "Chanson5", "Kek/Kek")
    #toast.add_user("Bidon","12345a67890")
    #toast.create_playlist("Max", "Playlist des enfers")
    #toast.add_song_playlist("7", "5484")
    toast.playlist_content("1")
    for k in toast.playlist_content("1"):
        print(f'k{k}')