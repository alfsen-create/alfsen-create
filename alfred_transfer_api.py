from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from memory_engine import AlfredMemoryDB
import os

app = Flask(__name__)
CORS(app)

db_path = os.environ.get('ALFRED_DB_PATH', 'alfred_mobile.db')
db = AlfredMemoryDB(db_path)

@app.route('/api/status')
def status():
    count = db.conn.execute('SELECT COUNT(*) FROM memories').fetchone()[0]
    return jsonify({'status': 'ready', 'count': count})

@app.route('/api/memory', methods=['POST'])
def add_memory():
    data = request.json
    agent = data.get('agent', 'unknown')
    content = data['content']
    meta = data.get('meta', {})
    memid = db.add_memory(agent, content, meta)
    return jsonify({'id': memid})

@app.route('/api/memory/<memid>', methods=['GET'])
def get_memory(memid):
    m = db.get_memory(memid)
    if not m:
        return jsonify({'error': 'not found'}), 404
    return jsonify(m)

@app.route('/api/search', methods=['GET'])
def search():
    q = request.args.get('q', '')
    limit = int(request.args.get('limit', 10))
    return jsonify(db.search(q, limit=limit))

@app.route('/api/prune', methods=['POST'])
def prune():
    keep = int(request.json.get('keep', 100))
    deleted = db.prune(keep=keep)
    return jsonify({'deleted': deleted})

@app.route('/api/export', methods=['GET'])
def export():
    path = 'alfred_export.json'
    count = db.export(path)
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(port=7740, debug=True)
