from fastapi import FastAPI, HTTPException
import joblib
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from pathlib import Path
from fastapi import UploadFile, File

# ---------------------------
# App Setup
# ---------------------------
app = FastAPI(title="Student Performance API 🚀")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# Load Model (robust path)
# ---------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "student_model.pkl"

try:
    model = joblib.load(MODEL_PATH)
    print("✅ Model loaded")
except Exception as e:
    model = None
    print("❌ Model load error:", e)

# ---------------------------
# Input Schema
# ---------------------------
class StudentInput(BaseModel):
    study_hours: float
    attendance: float
    quiz_score: float
    assignment_score: float
    midterm_score: float
    projects_completed: int

# ---------------------------
# Routes
# ---------------------------
@app.get("/")
def home():
    return {"message": "Student Performance API is running 🚀"}

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}

@app.post("/upload")
async def upload_excel(file: UploadFile = File(...)):
    df = pd.read_excel(file.file)

    students = []

    high = 0
    medium = 0
    low = 0

    for _, row in df.iterrows():

        final_ia = row["Final IA Marks (50M)"]

        # Risk Classification
        if final_ia < 25:
            risk = "High"
            high += 1

        elif final_ia < 40:
            risk = "Medium"
            medium += 1

        else:
            risk = "Low"
            low += 1

        # Suggestions Logic
        suggestions = []

        ia1 = row["IA 1 (25M)"]
        ia2 = row["IA 2 (25 M)"]
        cca3 = row["CCA 3(5M)"]

        if ia2 > ia1:
            suggestions.append(
                "Performance improving. Maintain current preparation."
            )

        elif ia2 < ia1:
            suggestions.append(
                "Performance declining. Review recent topics."
            )

        if cca3 <= 2:
            suggestions.append(
                "Focus on assignment and activity completion."
            )

        if final_ia < 25:
            suggestions.append(
                "Immediate faculty intervention recommended."
            )

        if not suggestions:
            suggestions.append(
                "Keep up the good work."
            )

        students.append({
            "usn": row["USN"],
            "name": row["Name"],
            "final_ia": final_ia,
            "risk_level": risk,
            "suggestions": suggestions
        })

    return {
        "summary": {
            "total_students": len(df),
            "high_risk": high,
            "medium_risk": medium,
            "low_risk": low
        },
        "students": students
    }
# ---------------------------
# Suggestions
# ---------------------------
def generate_suggestions(data: StudentInput):
    suggestions = []

    if data.study_hours < 4:
        suggestions.append("Increase study hours")
    if data.attendance < 75:
        suggestions.append("Improve attendance")
    if data.quiz_score < 60:
        suggestions.append("Focus on quizzes")
    if data.assignment_score < 60:
        suggestions.append("Complete assignments on time")
    if data.midterm_score < 50:
        suggestions.append("Revise core concepts")

    if not suggestions:
        suggestions.append("Keep up the good work")

    return suggestions

# ---------------------------
# Risk (3 levels for UI)
# ---------------------------
def get_risk_level(prob):
    if prob < 0.4:
        return "High"
    elif prob < 0.7:
        return "Medium"
    else:
        return "Low"

# ---------------------------
# Prediction
# ---------------------------
@app.post("/predict")
def predict(data: StudentInput):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    try:
        X = pd.DataFrame([data.dict()])

        prob = float(model.predict_proba(X)[0][1])
        pred = int(prob >= 0.5)

        return {
            "prediction": "PASS" if pred == 1 else "FAIL",
            "probability": round(prob, 2),
            "risk_level": get_risk_level(prob),
            "suggestions": generate_suggestions(data)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))