# Student Performance Prediction System

An end-to-end machine learning application that predicts student **PASS/FAIL** outcomes, estimates prediction probability, classifies academic risk, and generates actionable suggestions.

The project combines a Python ML pipeline, FastAPI model-serving API, Excel-based classroom analytics, and a Next.js dashboard.

## Architecture

```text
Student Data / Excel
        |
        v
Validation + Feature Preparation
        |
        v
ML Training Pipeline
        |
        v
Serialized Model (Joblib)
        |
        v
FastAPI
   |            |
 /predict     /upload
   |            |
   +------v-----+
          |
          v
Next.js Dashboard
          |
          v
Risk + Prediction + Suggestions
```

## What the project demonstrates

- End-to-end ML workflow from data preparation to model serving
- Train/test split with stratification
- Reusable preprocessing pipeline
- Classification models for comparison
- Model serialization with Joblib
- FastAPI REST endpoints
- Pydantic request validation
- Prediction probability and risk classification
- Excel upload for batch classroom analytics
- Personalized rule-based academic suggestions
- Next.js/React dashboard for results

## Tech stack

### Machine Learning

- Python
- Pandas
- Scikit-learn
- Joblib

### API

- FastAPI
- Pydantic
- Uvicorn

### Frontend

- Next.js
- React
- Tailwind CSS

## Repository structure

```text
student-performance-prediction/
├── data/
│   └── students.csv
├── models/
│   └── student_model.pkl
├── notebooks/
│   ├── 01_generate_data.py
│   └── 02_eda.py
├── src/
│   ├── pipeline.py
│   ├── train_model.py
│   ├── save_model.py
│   └── predict.py
├── serving/
│   └── app.py
├── dashboard/
│   └── app/
└── README.md
```

## ML pipeline

1. Load the student dataset.
2. Select academic and behavioral features.
3. Split data into training and test sets using stratification.
4. Apply the reusable preprocessing pipeline.
5. Train and evaluate classification models.
6. Serialize the selected model with Joblib.
7. Load the model in FastAPI for inference.
8. Return prediction, probability, risk level and suggestions.

### Model evaluation

The training code currently compares **Logistic Regression** and **Random Forest** using classification metrics. The repository documentation intentionally does not claim XGBoost as the final model unless it is actually used by the training/serving pipeline. This keeps the README consistent with the implementation.

For a future model-selection iteration, additional candidates such as XGBoost can be evaluated against the same held-out test set and selected based on measured performance rather than project description alone.

## API

### `GET /`

Basic API status response.

### `GET /health`

Returns API health and whether the serialized model loaded successfully.

### `POST /predict`

Predict an individual student's outcome.

Example input:

```json
{
  "study_hours": 5,
  "attendance": 75,
  "quiz_score": 60,
  "assignment_score": 65,
  "midterm_score": 60,
  "projects_completed": 2
}
```

Example response:

```json
{
  "prediction": "PASS",
  "probability": 0.87,
  "risk_level": "Low",
  "suggestions": [
    "Keep up the good work"
  ]
}
```

### `POST /upload`

Upload an Excel file for classroom-level analytics. The endpoint calculates total students, high/medium/low risk counts, and student-level suggestions from the configured academic columns.

## Risk logic

The prediction endpoint maps model probability to three UI-friendly risk levels:

```text
probability < 0.40  -> High
0.40 - 0.69        -> Medium
>= 0.70            -> Low
```

The Excel analytics endpoint uses Final IA marks for its classroom risk classification. These are two different views of risk and are kept explicit to avoid silently mixing model probability with rule-based academic thresholds.

## Local setup

### Backend

```bash
pip install -r requirements.txt
uvicorn serving.app:app --reload
```

API documentation is available through FastAPI's generated Swagger UI at `/docs`.

### Frontend

```bash
cd dashboard
npm install
npm run dev
```

## Interview talking points

### Why use a preprocessing pipeline?

It keeps transformations consistent between training and inference and reduces the risk of applying different preprocessing logic to production data.

### Why stratify the train/test split?

The target is a classification problem, so stratification helps preserve the class distribution in both training and test sets.

### Why return probability instead of only PASS/FAIL?

Probability provides a confidence signal that can be mapped to risk levels and used by the dashboard for prioritization.

### Is risk the same as prediction?

No. Prediction is the model's PASS/FAIL output. Risk is a presentation layer that maps probability to High/Medium/Low categories. The Excel upload flow additionally uses explicit academic thresholds.

### Why FastAPI?

It provides typed request validation with Pydantic, automatic OpenAPI documentation and a lightweight Python service for model inference.

## Future engineering improvements

- Automated model-selection/evaluation report
- Stronger schema validation for uploaded Excel files
- Unit and integration tests
- Configurable model path and application settings
- Restricted CORS origins for production
- Structured application logging
- Dockerized deployment
- SHAP/model explainability
- CI/CD with GitHub Actions
- Authentication and role-based access for educator dashboards
