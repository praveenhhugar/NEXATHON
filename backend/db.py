import sqlite3
from datetime import datetime

DB_NAME = "deceptor.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY, timestamp TEXT, ip TEXT, path TEXT, method TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS decisions (id INTEGER PRIMARY KEY, strategy_id INTEGER, action TEXT, success BOOLEAN, timestamp TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS strategies (id INTEGER PRIMARY KEY, name TEXT, type TEXT, tries INTEGER DEFAULT 0, hits INTEGER DEFAULT 0)''')
    
    cursor.execute("SELECT COUNT(*) FROM strategies")
    if cursor.fetchone()[0] == 0:
        strategies = [(1, "admin_login_decoy", "admin"), (2, "config_file_honeytoken", "config"), (3, "cloud_dashboard_decoy", "cloud")]
        cursor.executemany("INSERT INTO strategies (id, name, type) VALUES (?, ?, ?)", strategies)
    conn.commit()
    conn.close()

def log_event(ip, path, method):
    conn = get_db()
    conn.execute("INSERT INTO events (timestamp, ip, path, method) VALUES (?, ?, ?, ?)", (datetime.now().isoformat(), ip, path, method))
    conn.commit()
    conn.close()

def update_strategy_stats(strategy_id, hit=False):
    conn = get_db()
    if hit:
        conn.execute("UPDATE strategies SET tries = tries + 1, hits = hits + 1 WHERE id = ?", (strategy_id,))
    else:
        conn.execute("UPDATE strategies SET tries = tries + 1 WHERE id = ?", (strategy_id,))
    conn.commit()
    conn.close()