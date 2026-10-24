import sqlite3

def get_real_data(path):
    # In-memory DB for simplicity
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE files (name TEXT, content TEXT)")
    cursor.execute("INSERT INTO files VALUES (?, ?)", (path, "This is real, confidential company data."))
    conn.commit()
    return {"status": "200 OK", "data": "Real Data"}