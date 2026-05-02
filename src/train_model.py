import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

from pipeline import preprocessor

# Load data
df = pd.read_csv("../data/students.csv")

# Features & target
X = df.drop(columns=["pass", "final_score"])
y = df["pass"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# -------------------------------
# Model 1: Logistic Regression
# -------------------------------
log_model = Pipeline([
    ("preprocessor", preprocessor),
    ("model", LogisticRegression(max_iter=200, class_weight="balanced"))
])

log_model.fit(X_train, y_train)
y_pred_log = log_model.predict(X_test)

print("\n🔹 Logistic Regression Results:")
print(classification_report(y_test, y_pred_log))

# -------------------------------
# Model 2: Random Forest
# -------------------------------
rf_model = Pipeline([
    ("preprocessor", preprocessor),
    ("model", RandomForestClassifier(n_estimators=200, random_state=42))
])

rf_model.fit(X_train, y_train)
y_pred_rf = rf_model.predict(X_test)

print("\n🔹 Random Forest Results:")
print(classification_report(y_test, y_pred_rf))