import sqlite3

dbUrl = 'C:/Users/Fyalisia/miniconda3/envs/bsc/data.db'

class Database:
    def create_database():
        conn = sqlite3.connect(dbUrl)
        #print("Opened database successfully")
        
        c = conn.cursor()
        
        c.execute('''CREATE TABLE IF NOT EXISTS Tweet(id integer PRIMARY KEY AUTOINCREMENT, tweet_data varchar(255));''')
        #print("Table created successfully")
        
        conn.commit()
        
        conn.close()
        
        
    def insert_database(text):
        conn = sqlite3.connect(dbUrl)
        
        c = conn.cursor()
        
        data = {
            "text": text
        }
        
        q = "INSERT INTO Tweet(tweet_data) VALUES (:text)"
        
        c.execute(q, data)
        
        conn.commit()
        
        conn.close()
        
        



