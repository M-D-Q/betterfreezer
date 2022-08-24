import socket
import sys
import mariadb
import re

class Maria():
    def __init__ (self,user,password,host,port,db):
        # https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/
        try:
            self.conn = mariadb.connect(
                user=user,
                password=user,
                host=host,
                port=port,
                database=freezer_db
                )

            # Get Cursor
            self.cur = self.conn.cursor()

        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

    def list_tracks(self, owner="*")
        self.cur.execute("SELECT name FROM  WHERE owner = ?; ",(owner,))
        return self.cur

    # add song into database
    def ajouter(self,artist_name,song_name,filename):
        self.cur.execute("INSERT INTO  (name,artist,owner) VALUES (?,?,?)",(tu[3],tu[2],tu[1]))
        self.conn.commit()
