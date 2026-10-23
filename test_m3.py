import sqlite3

print("Starting M3 Test...")

# Connect to database (this creates the file if it doesn't exist)
conn = sqlite3.connect("deceptor.db")
cursor = conn.cursor()

# Create the table
cursor.execute("CREATE TABLE IF NOT EXISTS strategies (id INTEGER PRIMARY KEY, name TEXT)")

# Insert the data using a parameter (the safe way)
cursor.execute("INSERT INTO strategies (name) VALUES (?)", ('admin_login_decoy',))

# Save changes
conn.commit()

# Read it back
cursor.execute("SELECT * FROM strategies")
print("Database test successful! Found strategy:", cursor.fetchone())

# Close connection
conn.close()