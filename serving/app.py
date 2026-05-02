from fastapi import FastAPI, HTTPException
import joblib
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from pathlib import Path

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