from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

# Numeric columns
num_cols = [
    "study_hours",
    "attendance",
    "quiz_score",
    "assignment_score",
    "midterm_score",
    "projects_completed"
]

# Pipeline for numeric data
num_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

# Final preprocessor
preprocessor = ColumnTransformer([
    ("num", num_pipeline, num_cols)
])