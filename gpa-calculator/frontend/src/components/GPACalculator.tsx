import React, { useEffect, useState } from "react";

interface GradeEntry {
  id?: number;
  course: string;
  credits: number;
  grade: string;
}

export default function GPACalculator() {
  const [grades, setGrades] = useState<GradeEntry[]>([]);
  const [gpa, setGPA] = useState<number>(0.0);
  const [form, setForm] = useState<GradeEntry>({ course: "", credits: 3, grade: "A" });

  const fetchGrades = async () => {
    const res = await fetch("http://localhost:5000/api/grades");
    const data = await res.json();
    setGrades(data);
  };

  const fetchGPA = async () => {
    const res = await fetch("http://localhost:5000/api/gpa");
    const data = await res.json();
    setGPA(data.gpa);
  };

  const addGrade = async () => {
    await fetch("http://localhost:5000/api/grades", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    });
    setForm({ course: "", credits: 3, grade: "A" });
    fetchGrades();
    fetchGPA();
  };

  useEffect(() => {
    fetchGrades();
    fetchGPA();
  }, []);

  return (
    <div className="p-4 max-w-md mx-auto bg-white rounded shadow">
      <h1 className="text-2xl font-bold mb-4">GPA Calculator</h1>
      <div className="mb-4">
        <input
          type="text"
          placeholder="Course"
          value={form.course}
          onChange={(e) => setForm({ ...form, course: e.target.value })}
          className="border p-2 w-full mb-2"
        />
        <input
          type="number"
          placeholder="Credits"
          value={form.credits}
          onChange={(e) => setForm({ ...form, credits: +e.target.value })}
          className="border p-2 w-full mb-2"
        />
        <select
          value={form.grade}
          onChange={(e) => setForm({ ...form, grade: e.target.value })}
          className="border p-2 w-full mb-2"
        >
          {["A", "B", "C", "D", "F"].map((g) => (
            <option key={g} value={g}>
              {g}
            </option>
          ))}
        </select>
        <button
          onClick={addGrade}
          className="bg-blue-500 text-white px-4 py-2 rounded"
        >
          Add Grade
        </button>
      </div>
      <h2 className="text-xl font-semibold mb-2">Current GPA: {gpa}</h2>
      <ul>
        {grades.map((grade) => (
          <li key={grade.id}>
            {grade.course} - {grade.credits} credits - {grade.grade}
          </li>
        ))}
      </ul>
    </div>
  );
}