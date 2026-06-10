'use client'

import { useState } from 'react'

export default function Home() {

  const [file, setFile] = useState<File | null>(null)
  const [data, setData] = useState<any>(null)
  const [selectedStudent, setSelectedStudent] = useState<any>(null)
  const [filter, setFilter] = useState("All")
  const [search, setSearch] = useState("")

  const filteredStudents =
    data?.students.filter((student: any) => {

      const matchesRisk =
        filter === "All"
          ? true
          : student.risk_level === filter

      const matchesSearch =
        student.name
          .toLowerCase()
          .includes(search.toLowerCase()) ||

        student.usn
          .toLowerCase()
          .includes(search.toLowerCase())

      return matchesRisk && matchesSearch

    }) || []

  const finalIAs =
    data?.students.map(
      (s: any) => s.final_ia
    ) || []

  const averageIA =
    finalIAs.length > 0
      ? (
          finalIAs.reduce(
            (a: number, b: number) => a + b,
            0
          ) / finalIAs.length
        ).toFixed(2)
      : 0

  const highestIA =
    finalIAs.length > 0
      ? Math.max(...finalIAs)
      : 0

  const lowestIA =
    finalIAs.length > 0
      ? Math.min(...finalIAs)
      : 0

  async function uploadFile() {

    if (!file) return

    const formData = new FormData()
    formData.append("file", file)

    const res = await fetch(
      "http://127.0.0.1:8000/upload",
      {
        method: "POST",
        body: formData
      }
    )

    const result = await res.json()

    setData(result)
    setSelectedStudent(null)
  }

  return (
    <div className="min-h-screen p-8">

      <h1 className="text-4xl font-bold mb-8">
        🎓 Student Analytics Dashboard
      </h1>

      {/* Upload Section */}
      <div className="border rounded-xl p-6 mb-8">

        <h2 className="text-xl font-semibold mb-4">
          Upload Student Excel
        </h2>

        <input
          type="file"
          accept=".xlsx,.xls"
          onChange={(e) =>
            setFile(e.target.files?.[0] || null)
          }
        />

        <button
          onClick={uploadFile}
          className="ml-4 bg-blue-600 text-white px-4 py-2 rounded"
        >
          Analyze Class
        </button>

      </div>

      {data && (

        <>

          {/* Summary Cards */}
          <div className="grid grid-cols-4 gap-4 mb-8">

            <div className="border p-4 rounded-xl">
              <h3>Total Students</h3>
              <p className="text-3xl font-bold">
                {data.summary.total_students}
              </p>
            </div>

            <div className="border p-4 rounded-xl">
              <h3>High Risk</h3>
              <p className="text-3xl font-bold text-red-600">
                {data.summary.high_risk}
              </p>
            </div>

            <div className="border p-4 rounded-xl">
              <h3>Medium Risk</h3>
              <p className="text-3xl font-bold text-yellow-600">
                {data.summary.medium_risk}
              </p>
            </div>

            <div className="border p-4 rounded-xl">
              <h3>Low Risk</h3>
              <p className="text-3xl font-bold text-green-600">
                {data.summary.low_risk}
              </p>
            </div>

          </div>

          {/* Class Statistics */}
          <div className="border rounded-xl p-6 mb-8">

            <h2 className="text-2xl font-bold mb-4">
              Class Statistics
            </h2>

            <div className="grid grid-cols-3 gap-4">

              <div className="border p-4 rounded-xl">
                <h3>Highest IA</h3>
                <p className="text-3xl font-bold text-green-600">
                  {highestIA}
                </p>
              </div>

              <div className="border p-4 rounded-xl">
                <h3>Average IA</h3>
                <p className="text-3xl font-bold text-blue-600">
                  {averageIA}
                </p>
              </div>

              <div className="border p-4 rounded-xl">
                <h3>Lowest IA</h3>
                <p className="text-3xl font-bold text-red-600">
                  {lowestIA}
                </p>
              </div>

            </div>

          </div>

          {/* Filter Buttons */}
          <div className="flex gap-3 mb-4">

            <button
              onClick={() => setFilter("All")}
              className="px-4 py-2 border rounded"
            >
              All
            </button>

            <button
              onClick={() => setFilter("High")}
              className="px-4 py-2 bg-red-500 text-white rounded"
            >
              High Risk
            </button>

            <button
              onClick={() => setFilter("Medium")}
              className="px-4 py-2 bg-yellow-500 text-white rounded"
            >
              Medium Risk
            </button>

            <button
              onClick={() => setFilter("Low")}
              className="px-4 py-2 bg-green-500 text-white rounded"
            >
              Low Risk
            </button>

          </div>

          {/* Search Box */}
          <div className="mb-4">

            <input
              type="text"
              placeholder="Search by USN or Name..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="border p-2 rounded w-full"
            />

          </div>

          {/* Student Table */}
          <div className="border rounded-xl p-6">

            <h2 className="text-2xl font-bold mb-4">
              Student List
            </h2>

            <div className="overflow-x-auto">

              <table className="w-full border-collapse border">

                <thead>

                  <tr className="bg-gray-100">
                    <th className="border p-3">USN</th>
                    <th className="border p-3">Name</th>
                    <th className="border p-3">Final IA</th>
                    <th className="border p-3">Risk Level</th>
                  </tr>

                </thead>

                <tbody>

                  {filteredStudents.map(
                    (student: any, index: number) => (

                      <tr
                        key={index}
                        onClick={() =>
                          setSelectedStudent(student)
                        }
                        className="hover:bg-blue-50 cursor-pointer"
                      >

                        <td className="border p-3">
                          {student.usn}
                        </td>

                        <td className="border p-3">
                          {student.name}
                        </td>

                        <td className="border p-3 text-center">
                          {student.final_ia}
                        </td>

                        <td
                          className={`border p-3 font-semibold text-center
                          ${student.risk_level === "High"
                              ? "text-red-600"
                              : student.risk_level === "Medium"
                              ? "text-yellow-600"
                              : "text-green-600"
                            }`}
                        >
                          {student.risk_level}
                        </td>

                      </tr>

                    )
                  )}

                </tbody>

              </table>

            </div>

          </div>

          {/* Student Details */}
          {selectedStudent && (

            <div className="mt-8 border rounded-xl p-6 shadow">

              <h2 className="text-2xl font-bold mb-4">
                Student Details
              </h2>

              <div className="space-y-2">

                <p>
                  <strong>USN:</strong>{" "}
                  {selectedStudent.usn}
                </p>

                <p>
                  <strong>Name:</strong>{" "}
                  {selectedStudent.name}
                </p>

                <p>
                  <strong>Final IA:</strong>{" "}
                  {selectedStudent.final_ia}
                </p>

                <p>
                  <strong>Risk Level:</strong>{" "}

                  <span
                    className={
                      selectedStudent.risk_level === "High"
                        ? "text-red-600 font-bold"
                        : selectedStudent.risk_level === "Medium"
                        ? "text-yellow-600 font-bold"
                        : "text-green-600 font-bold"
                    }
                  >
                    {selectedStudent.risk_level}
                  </span>

                </p>

              </div>

              <div className="mt-4">

                <h3 className="font-bold text-lg mb-2">
                  Suggestions
                </h3>

                {selectedStudent.suggestions?.length > 0 ? (

                  selectedStudent.suggestions.map(
                    (s: string, i: number) => (
                      <p key={i}>• {s}</p>
                    )
                  )

                ) : (

                  <p>No suggestions available.</p>

                )}

              </div>

            </div>

          )}

        </>

      )}

    </div>
  )
}