# Architecture

## System flow

```text
Dataset / Excel
      |
      v
Feature preparation + validation
      |
      v
Training / evaluation
      |
      v
Joblib model artifact
      |
      v
FastAPI inference service
      |
      +---- POST /predict ----> Individual prediction
      |
      +---- POST /upload -----> Classroom analytics
                                  |
                                  v
                           Next.js dashboard
```

## ML responsibilities

- `src/pipeline.py` owns reusable preprocessing.
- `src/train_model.py` trains and compares classification models.
- `src/save_model.py` persists the selected model artifact.
- `models/` contains the artifact consumed by the serving layer.

## Serving responsibilities

`serving/app.py` is the inference boundary. It validates individual prediction input with Pydantic, loads the serialized model, performs inference, and returns a stable JSON response.

The Excel upload endpoint is a separate analytics path. It derives classroom risk from configured academic columns and generates rule-based suggestions.

## Frontend responsibilities

The Next.js dashboard is responsible for presentation, user interaction, API requests and displaying prediction/risk insights. Model training should remain outside the frontend.

## Design decisions

### Probability-driven risk

The `/predict` endpoint uses model probability to classify High, Medium and Low risk. This keeps the model output separate from the UI risk presentation.

### Rule-based classroom analytics

The `/upload` endpoint uses explicit academic thresholds for batch analytics. Keeping this logic separate makes the system easier to explain and prevents the dashboard from treating every risk signal as a machine-learning prediction.

### Model portability

Joblib allows the trained pipeline/model to be serialized and loaded by the API without retraining on every server start.

## Production hardening

Recommended next steps are automated tests, strict production CORS, structured logging, configuration management, upload schema validation, model versioning, containerization and CI/CD.
