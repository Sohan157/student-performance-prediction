import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
from xgboost import XGBClassifier

from pipeline import preprocessor

# Load data
df = pd.read_csv("../data/students.csv")

X = df.drop(columns=["pass", "final_score"])
y = df["pass"]

# Handle imbalance
scale_pos_weight = (len(y) - sum(y)) / sum(y)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# XGBoost model
xgb_model = Pipeline([
    ("preprocessor", preprocessor),
    ("model", XGBClassifier(
        n_estimators=300,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        scale_pos_weight=scale_pos_weight,
        random_state=42,
        use_label_encoder=False,
        eval_metric="logloss"
    ))
])

# Train
xgb_model.fit(X_train, y_train)

# Predict
y_pred = xgb_model.predict(X_test)

# Results
print("\n🔥 XGBoost Results:")
print(classification_report(y_test, y_pred))