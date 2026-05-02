import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("../data/students.csv")

print("✅ Data Loaded Successfully!\n")

# Basic info
print("🔹 Shape:", df.shape)
print("\n🔹 Columns:\n", df.columns)
print("\n🔹 Data Types:\n", df.dtypes)

# Missing values
print("\n🔹 Missing Values:\n", df.isnull().sum())

# Statistical summary
print("\n🔹 Summary:\n", df.describe())

# -------------------------------
# 📊 Visualization
# -------------------------------

# Pass/Fail distribution
plt.figure()
df["pass"].value_counts().plot(kind="bar")
plt.title("Pass vs Fail Distribution")
plt.xlabel("Pass (1) / Fail (0)")
plt.ylabel("Count")
plt.show()

# Correlation heatmap
plt.figure()
sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
plt.title("Feature Correlation")
plt.show()

# Study hours vs final score
plt.figure()
plt.scatter(df["study_hours"], df["final_score"])
plt.xlabel("Study Hours")
plt.ylabel("Final Score")
plt.title("Study Hours vs Final Score")
plt.show()