import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from pipeline import preprocessor

# Load data
df = pd.read_csv("../data/students.csv")

X = df.drop(columns=["pass", "final_score"])
y = df["pass"]

# Train final model
model = Pipeline([
    ("preprocessor", preprocessor),
    ("model", LogisticRegression(max_iter=200))
])

model.fit(X, y)

# Save model
joblib.dump(model, "../models/student_model.pkl")

print("✅ Model saved successfully!")