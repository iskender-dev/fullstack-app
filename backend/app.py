from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    return psycopg2.connect(DATABASE_URL)


def create_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            text VARCHAR(255)
        )
    """)

    conn.commit()
    cur.close()
    conn.close()


@app.route("/")
def home():
    return "Backend is running!"


@app.route("/api/data", methods=["GET"])
def get_tasks():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tasks ORDER BY id")
    tasks = cur.fetchall()

    cur.close()
    conn.close()

    result = []

    for task in tasks:
        result.append({
            "id": task[0],
            "text": task[1]
        })

    return jsonify(result)


@app.route("/api/data", methods=["POST"])
def add_task():
    data = request.json
    text = data.get("text")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO tasks (text) VALUES (%s) RETURNING id",
        (text,)
    )

    task_id = cur.fetchone()[0]

    conn.commit()

    cur.close()
    conn.close()

    return jsonify({
        "id": task_id,
        "text": text
    })


@app.route("/api/data/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM tasks WHERE id = %s",
        (task_id,)
    )

    conn.commit()

    cur.close()
    conn.close()

    return jsonify({
        "message": "Deleted"
    })


if __name__ == "__main__":
    create_table()

    port = int(os.getenv("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )