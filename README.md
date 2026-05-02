# 📘 Student Performance Prediction System

A full-stack machine learning system that predicts whether a student will **PASS or FAIL** based on academic and behavioral features, and provides **risk analysis + actionable suggestions**.

---

## 🚀 Features

- 📊 Predict student performance (PASS / FAIL)
- 📈 Probability score for prediction
- ⚠️ Risk level classification (High / Medium / Low)
- 💡 Personalized suggestions for improvement
- 🌐 REST API using FastAPI
- 🖥️ Interactive frontend dashboard using Next.js
- 🔄 End-to-end ML pipeline

---

## 🧠 Tech Stack

**Backend (ML + API)**
- Python
- Scikit-learn
- Pandas
- FastAPI
- Joblib

**Frontend**
- Next.js
- React
- Tailwind CSS

---

## 📂 Project Structure

Student-Performance-Prediction/
│
├── data/
│   └── students.csv
│
├── models/
│   └── student_model.pkl
│
├── notebooks/
│   ├── 01_generate_data.py
│   └── 02_eda.py
│
├── src/
│   ├── train_model.py
│   ├── save_model.py
│   └── predict.py
│
├── serving/
│   └── app.py
│
├── dashboard/
│   └── app/page.tsx
│
└── README.md

---

## ⚙️ How It Works

1. Data is generated and analyzed  
2. Machine learning model is trained  
3. Model is saved using `joblib`  
4. FastAPI serves predictions via `/predict`  
5. Next.js frontend sends user input to API  
6. Results displayed with insights  

---

## 🧪 API Endpoints

### GET `/`
Check if API is running

### GET `/health`
Health check for model

### POST `/predict`

#### Request:
```json
{
  "study_hours": 5,
  "attendance": 75,
  "quiz_score": 60,
  "assignment_score": 65,
  "midterm_score": 60,
  "projects_completed": 2
}

Response:
{
  "prediction": "PASS",
  "probability": 0.87,
  "risk_level": "Low",
  "suggestions": [
    "Keep up the good work"
  ]
}
git clone <your-repo-link>
cd Student-Performance-Prediction

Backend Setup
pip install -r requirements.txt
uvicorn serving.app:app --reload

Frontend Setup
cd dashboard
npm install
npm run dev

Model Details
Algorithm: Logistic Regression
Handles class imbalance using class_weight="balanced"
Evaluated using Precision, Recall, F1-score

 Use Case
Identify at-risk students early
Provide actionable academic guidance
Assist educators in decision-making

 Key Highlights
End-to-end ML system (not just model)
Real-time predictions via API
Interactive UI dashboard
Industry-relevant project

 Future Improvements
 Add charts and analytics
 Explainability (SHAP)
 Deploy on cloud (Render + Vercel)
 Authentication system