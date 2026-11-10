from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Database location
DB_PATH = os.environ.get("DB_PATH", "/data/notes.db")


# Connect to database
def get_db_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    return conn


# Create database table
def init_db():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Home endpoint
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Dockerized Notes API is running",
        "status": "success"
    })


# Health endpoint
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200


# Get all notes
@app.route("/notes", methods=["GET"])
def get_notes():
    conn = get_db_connection()

    notes = conn.execute(
        "SELECT * FROM notes"
    ).fetchall()

    conn.close()

    return jsonify([dict(note) for note in notes])


# Create a note
@app.route("/notes", methods=["POST"])
def create_note():
    data = request.get_json(silent=True) or {}

    title = data.get("title")
    content = data.get("content")

    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "Valid title is required"}), 400

    if not isinstance(content, str) or not content.strip():
        return jsonify({"error": "Valid content is required"}), 400

    conn = get_db_connection()

    cursor = conn.execute(
        "INSERT INTO notes (title, content) VALUES (?, ?)",
        (title.strip(), content.strip())
    )

    conn.commit()

    note_id = cursor.lastrowid
    conn.close()

    return jsonify({
        "message": "Note created",
        "id": note_id
    }), 201


# Delete a note
@app.route("/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    conn = get_db_connection()

    cursor = conn.execute(
        "DELETE FROM notes WHERE id = ?",
        (note_id,)
    )

    conn.commit()
    deleted = cursor.rowcount
    conn.close()

    if deleted == 0:
        return jsonify({"error": "Note not found"}), 404

    return jsonify({"message": "Note deleted"})


# Initialize database
init_db()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
