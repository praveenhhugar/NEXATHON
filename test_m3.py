import os
print("Starting M3 Test...")

# Let's test if the database can be created
import sqlite3
DB_NAME = "deceptor.db"
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS strategies (id INTEGER PRIMARY KEY, name TEXT)''')
cursor.execute('''INSERT INTO strategies (name) VALUES ('admin_login_decoy')''')
conn.commit()

# Read it back
cursor.execute('''SELECT * FROM strategies''')
print("Database test successful! Found strategy:", cursor.fetchone())
conn.close()