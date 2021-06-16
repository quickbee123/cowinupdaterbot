import psycopg2


class Database():

    def __init__(self, db_url:str):

        self.conn =  psycopg2.connect(db_url)

    def __del__(self):

        self.conn.close()    

    def get_stickers(self):

        cur = self.conn.cursor()
        cur.execute("SELECT * FROM stickers")
        stickers = cur.fetchall()
        cur.close()
        return stickers

    def add_sticker(self, file_id:str):

        cur = self.conn.cursor()
        cur.execute('INSERT INTO stickers (file) VALUES (%s)',(file_id,))
        self.conn.commit()
        cur.close()
