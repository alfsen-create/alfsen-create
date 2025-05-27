import os
import sqlite3
import uuid
import json
from datetime import datetime
import numpy as np

try:
    from sentence_transformers import SentenceTransformer
except Exception:
    SentenceTransformer = None

EMBED_MODEL_NAME = 'all-MiniLM-L6-v2'

class AlfredMemoryDB:
    """Simple local memory database with summarization and embedding search."""

    def __init__(self, db_path="alfred_mobile.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._setup()
        self.embed_model = None
        if SentenceTransformer is not None:
            try:
                self.embed_model = SentenceTransformer(EMBED_MODEL_NAME)
            except Exception:
                self.embed_model = None

    def _setup(self):
        cur = self.conn.cursor()
        cur.execute(
            """CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                agent TEXT,
                summary TEXT,
                content TEXT,
                meta TEXT,
                ts TEXT,
                embedding BLOB
            )"""
        )
        self.conn.commit()

    def add_memory(self, agent, content, meta=None):
        summary = self.summarize(content)
        emb = self.embed(summary)
        memory_id = str(uuid.uuid4())
        cur = self.conn.cursor()
        cur.execute(
            'INSERT INTO memories (id, agent, summary, content, meta, ts, embedding) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (
                memory_id,
                agent,
                summary,
                json.dumps(content),
                json.dumps(meta or {}),
                datetime.utcnow().isoformat(),
                emb.tobytes() if emb is not None else None,
            ),
        )
        self.conn.commit()
        return memory_id

    def get_memory(self, memory_id):
        cur = self.conn.cursor()
        cur.execute(
            'SELECT id, agent, summary, content, meta, ts FROM memories WHERE id=?',
            (memory_id,),
        )
        row = cur.fetchone()
        if not row:
            return None
        return {
            'id': row[0],
            'agent': row[1],
            'summary': row[2],
            'content': json.loads(row[3]),
            'meta': json.loads(row[4]),
            'timestamp': row[5],
        }

    def search(self, query, limit=10):
        emb = self.embed(query)
        if emb is None:
            return []
        cur = self.conn.cursor()
        results = []
        for row in cur.execute('SELECT id, summary, embedding FROM memories'):
            if row[2] is None:
                continue
            row_emb = np.frombuffer(row[2], dtype=np.float32)
            sim = self.cosine_sim(emb, row_emb)
            results.append((sim, row[0], row[1]))
        results.sort(reverse=True)
        return [
            {'id': memid, 'summary': summary, 'similarity': float(sim)}
            for sim, memid, summary in results[:limit]
        ]

    def prune(self, keep=100):
        cur = self.conn.cursor()
        cur.execute('SELECT id FROM memories ORDER BY ts DESC LIMIT ?', (keep,))
        keep_ids = {row[0] for row in cur.fetchall()}
        cur.execute('SELECT id FROM memories')
        all_ids = {row[0] for row in cur.fetchall()}
        to_delete = all_ids - keep_ids
        for memid in to_delete:
            cur.execute('DELETE FROM memories WHERE id=?', (memid,))
        self.conn.commit()
        return len(to_delete)

    def summarize(self, content, max_chars=500):
        """Simple truncation-based summarization."""
        if isinstance(content, str):
            text = content
        elif isinstance(content, list):
            text = ' '.join([m.get('content', '') for m in content])
        else:
            text = str(content)
        if len(text) > max_chars:
            return text[:max_chars] + '...'
        return text

    def embed(self, text):
        if self.embed_model is None:
            return None
        vec = self.embed_model.encode([text])[0]
        return np.array(vec, dtype=np.float32)

    def cosine_sim(self, a, b):
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

    def export(self, path):
        cur = self.conn.cursor()
        all_rows = list(cur.execute('SELECT id, agent, summary, content, meta, ts FROM memories'))
        data = []
        for row in all_rows:
            data.append(
                {
                    'id': row[0],
                    'agent': row[1],
                    'summary': row[2],
                    'content': json.loads(row[3]),
                    'meta': json.loads(row[4]),
                    'timestamp': row[5],
                }
            )
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return len(data)
