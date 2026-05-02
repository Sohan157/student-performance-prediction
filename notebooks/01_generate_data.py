import pandas as pd
import numpy as np

np.random.seed(42)

# Number of students
n = 1000

data = pd.DataFrame({
    "student_id": range(1, n+1),
    "study_hours": np.random.normal(5, 2, n).clip(0, 12),
    "attendance": np.random.uniform(50, 100, n),
    "quiz_score": np.random.uniform(40, 100, n),
    "assignment_score": np.random.uniform(40, 100, n),
    "midterm_score": np.random.uniform(30, 100, n),
    "projects_completed": np.random.randint(0, 5, n),
    "extracurricular": np.random.randint(0, 2, n)
})

# Create final score (realistic logic)
data["final_score"] = (
    0.3 * data["study_hours"] * 10 +
    0.2 * data["attendance"] +
    0.2 * data["quiz_score"] +
    0.2 * data["assignment_score"] +
    0.1 * data["midterm_score"]
)

# Add noise
data["final_score"] += np.random.normal(0, 5, n)

# Pass/Fail target
data["pass"] = (data["final_score"] >= 50).astype(int)

# Save dataset
data.to_csv("../data/students.csv", index=False)

print("✅ Dataset created successfully!")
print(data.head())