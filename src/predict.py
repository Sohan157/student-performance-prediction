import joblib
import pandas as pd

# Load model
model = joblib.load("../models/student_model.pkl")

# Sample input
sample = pd.DataFrame([{
    "study_hours": 6,
    "attendance": 80,
    "quiz_score": 70,
    "assignment_score": 75,
    "midterm_score": 65,
    "projects_completed": 2
}])

# Predict
prediction = model.predict(sample)[0]
prob = model.predict_proba(sample)[0][1]

print("Prediction:", "PASS" if prediction == 1 else "FAIL")
print("Probability of Passing:", round(prob, 2))