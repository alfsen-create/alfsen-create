import sqlite3
import json
from config import DB_PATH

class RequestTracker:
    def __init__(self, db_path=DB_PATH):
        self.conn = sqlite3.connect(db_path)
        self.create_table()
    def create_table(self):
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                request_id TEXT UNIQUE,
                status TEXT,
                command TEXT,
                steps TEXT,
                results TEXT
            )''')
    def upsert_request(self, request_id, status, command=None, steps=None, results=None):
        with self.conn:
            self.conn.execute('''
                INSERT INTO requests (request_id, status, command, steps, results)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(request_id) DO UPDATE SET
                    status=excluded.status, steps=excluded.steps, results=excluded.results
            ''', (request_id, status, command,
                  json.dumps(steps or []), json.dumps(results or {})))
    def get_request(self, request_id):
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM requests WHERE request_id=?', (request_id,))
        return cur.fetchone()
