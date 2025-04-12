from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/api/grades", methods=["GET"])
def get_grades():
    conn = get_db_connection()
    grades = conn.execute("SELECT * FROM grades").fetchall()
    conn.close()
    return jsonify([dict(row) for row in grades])

@app.route("/api/grades", methods=["POST"])
def add_grade():
    data = request.get_json()
    course = data.get("course")
    credits = data.get("credits")
    grade = data.get("grade")

    conn = get_db_connection()
    conn.execute("INSERT INTO grades (course, credits, grade) VALUES (?, ?, ?)",
                 (course, credits, grade))
    conn.commit()
    conn.close()
    return jsonify({"message": "Grade added"}), 201

@app.route("/api/gpa", methods=["GET"])
def calculate_gpa():
    conn = get_db_connection()
    grades = conn.execute("SELECT * FROM grades").fetchall()
    conn.close()

    total_credits = 0
    total_points = 0
    grade_map = {"A": 4.0, "B": 3.0, "C": 2.0, "D": 1.0, "F": 0.0}

    for row in grades:
        credits = row["credits"]
        grade = row["grade"]
        if grade in grade_map:
            total_points += grade_map[grade] * credits
            total_credits += credits

    gpa = total_points / total_credits if total_credits > 0 else 0.0
    return jsonify({"gpa": round(gpa, 2)})

if __name__ == "__main__":
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course TEXT NOT NULL,
            credits INTEGER NOT NULL,
            grade TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    app.run(debug=True)