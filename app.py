
from flask import Flask, jsonify
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
            CREATE TABLE IF NOT EXISTS data_mahasiswa (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                matakuliah TEXT NOT NULL,
                nama TEXT NOT NULL,
                status TEXT NOT NULL
            )
        """)

        jumlah = conn.execute(
            "SELECT COUNT(*) FROM data_mahasiswa"
        ).fetchone()[0]

        if jumlah == 0:
            conn.execute("""
                INSERT INTO data_mahasiswa
                    (matakuliah, nama, status)
                VALUES (?, ?, ?)
            """, (
                "Komputasi Awan",
                "Dimas Dwi Karunia Ramadhan",
                "Berhasil Terhubung ke Database & Docker"
            ))

        conn.commit()
    finally:
        conn.close()


@app.route("/")
def hello():
    try:
        init_db()

        conn = get_connection()
        try:
            rows = conn.execute("""
                SELECT id, matakuliah, nama, status
                FROM data_mahasiswa
                ORDER BY id
            """).fetchall()

            return jsonify({
                "data_mahasiswa": [dict(row) for row in rows],
                "database_connection": "CONNECTED",
                "message": "Halo dari Flask + Database SQLite + Docker + Jenkins!"
            })
        finally:
            conn.close()

    except sqlite3.Error:
        app.logger.exception("Koneksi database gagal")
        return jsonify({
            "data_mahasiswa": [],
            "database_connection": "DISCONNECTED",
            "message": "Gagal terhubung ke database"
        }), 500


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
