import sqlite3

def get_fake_data(path):
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE files (name TEXT, content TEXT)")
    # This is the Honeytoken. It looks real, but it's a trap.
    cursor.execute("INSERT INTO files VALUES (?, ?)", (path, "DB_PASSWORD=admin123"))
    conn.commit()
    # The attacker thinks they got real data
    return {"status": "200 OK", "data": "Decoy Data"}