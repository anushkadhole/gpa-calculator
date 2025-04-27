from flask import Flask, request, jsonify
from flask_cors import CORS
from database import get_db, query_db, close_connection
from models import create_tables

app = Flask(__name__)
CORS(app)

@app.before_request
def before_request():
    db = get_db()
    create_tables(db)

@app.teardown_appcontext
def teardown(exception):
    close_connection(exception)

@app.route("/api/grades", methods=["GET"])
def get_grades():
    grades = query_db("SELECT * FROM grades")
    return jsonify([dict(row) for row in grades])

@app.route("/api/grades", methods=["POST"])
def add_grade():
    data = request.get_json()
    course = data.get("course")
    credits = data.get("credits")
    grade = data.get("grade")
    db = get_db()
    db.execute("INSERT INTO grades (course, credits, grade) VALUES (?, ?, ?)", (course, credits, grade))
    db.commit()
    return jsonify({"message": "Grade added"}), 201

@app.route("/api/gpa", methods=["GET"])
def calculate_gpa():
    grades = query_db("SELECT * FROM grades")
    total_points = 0
    total_credits = 0
    grade_map = {"A": 4.0, "B": 3.0, "C": 2.0, "D": 1.0, "F": 0.0}

    for row in grades:
        credits = row["credits"]
        grade = row["grade"].upper()
        total_points += grade_map.get(grade, 0.0) * credits
        total_credits += credits

    gpa = total_points / total_credits if total_credits else 0.0
    return jsonify({"gpa": round(gpa, 2)})

if __name__ == "__main__":
    app.run(debug=True)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # <--- important for Render deployment
    app.run(host="0.0.0.0", port=port)
