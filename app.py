
from flask import Flask, jsonify, request
import os
import sqlite3

app = Flask(__name__)

DATABASE_PATH = os.environ.get("DATABASE_PATH", "data/app.db")


def get_connection():
    folder = os.path.dirname(DATABASE_PATH)
    if folder:
        os.makedirs(folder, exist_ok=True)

    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL
            )
        """)
        conn.commit()
    finally:
        conn.close()


@app.route("/")
def hello():
    init_db()
    return "Halo dari Flask + Docker + Jenkins! SQLite tersambung."


@app.route("/messages", methods=["GET"])
def get_messages():
    init_db()
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT id, content FROM messages ORDER BY id"
        ).fetchall()
        return jsonify([dict(row) for row in rows])
    finally:
        conn.close()


@app.route("/messages", methods=["POST"])
def add_message():
    data = request.get_json(silent=True) or {}
    content = data.get("content")

    if not isinstance(content, str) or not content.strip():
        return jsonify({"error": "Content tidak boleh kosong"}), 400

    init_db()
    conn = get_connection()
    try:
        cursor = conn.execute(
            "INSERT INTO messages (content) VALUES (?)",
            (content.strip(),)
        )
        conn.commit()

        return jsonify({
            "id": cursor.lastrowid,
            "content": content.strip()
        }), 201
    finally:
        conn.close()


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
