import sqlite3

def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
  CREATE TABLE "user" (
	"userID"	INTEGER,
	"username"	TEXT NOT NULL,
	"email"	TEXT NOT NULL,
	"reset_token"	INTEGER,
	PRIMARY KEY("userID" AUTOINCREMENT)
)
    ''')
    conn.commit()
    conn.close()

init_db()