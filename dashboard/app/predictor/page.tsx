'use client'
import { useState } from 'react';

export default function Home() {
  const [form, setForm] = useState({
    study_hours: 5,
    attendance: 75,
    quiz_score: 60,
    assignment_score: 65,
    midterm_score: 60,
    projects_completed: 2
  });

  const [result, setResult] = useState<any>(null);

  function handleChange(e: any) {
    setForm({
      ...form,
      [e.target.name]: Number(e.target.value)
    });
  }

  async function predict() {
    const res = await fetch("https://student-performance-prediction-nw5k.onrender.com/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(form)
    });

    const data = await res.json();
    setResult(data);
  }

  return (
    <div className="min-h-screen flex flex-col items-center p-6">
      
      <h1 className="text-3xl font-bold mb-6">
        🎓 Student Performance Dashboard
      </h1>

      {/* INPUT FORM WITH LABELS */}
      <div className="grid grid-cols-2 gap-4 mb-6 w-[400px]">

        <div>
          <label className="text-sm">Study Hours</label>
          <input name="study_hours" type="number" value={form.study_hours}
            onChange={handleChange} className="border p-2 rounded w-full" />
        </div>

        <div>
          <label className="text-sm">Attendance (%)</label>
          <input name="attendance" type="number" value={form.attendance}
            onChange={handleChange} className="border p-2 rounded w-full" />
        </div>

        <div>
          <label className="text-sm">Quiz Score</label>
          <input name="quiz_score" type="number" value={form.quiz_score}
            onChange={handleChange} className="border p-2 rounded w-full" />
        </div>

        <div>
          <label className="text-sm">Assignment Score</label>
          <input name="assignment_score" type="number" value={form.assignment_score}
            onChange={handleChange} className="border p-2 rounded w-full" />
        </div>

        <div>
          <label className="text-sm">Midterm Score</label>
          <input name="midterm_score" type="number" value={form.midterm_score}
            onChange={handleChange} className="border p-2 rounded w-full" />
        </div>

        <div>
          <label className="text-sm">Projects Completed</label>
          <input name="projects_completed" type="number" value={form.projects_completed}
            onChange={handleChange} className="border p-2 rounded w-full" />
        </div>

      </div>

      {/* BUTTON */}
      <button 
        onClick={predict}
        className="bg-blue-600 text-white px-6 py-2 rounded-lg"
      >
        Predict Student
      </button>

      {/* RESULT */}
      {result && (
        <div className="mt-6 p-5 border rounded-xl text-center shadow-md w-80">
          
          <h2 className="text-xl font-semibold">
            Prediction: {result.prediction}
          </h2>

          <p className="mt-2">
            Probability: {(result.probability * 100).toFixed(1)}%
          </p>

          {/* Risk */}
          <p className={`mt-2 font-medium ${
            result.risk_level === "High"
              ? "text-red-600"
              : result.risk_level === "Medium"
              ? "text-yellow-600"
              : "text-green-600"
          }`}>
            Risk Level: {result.risk_level}
          </p>

          {/* Suggestions */}
          <div className="mt-4 text-left">
            <h3 className="font-semibold mb-2">Suggestions:</h3>
            {result.suggestions?.map((s: string, i: number) => (
              <p key={i} className="text-sm">• {s}</p>
            ))}
          </div>

        </div>
      )}
    </div>
  );
}