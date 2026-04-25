import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

# Load processed data
df = pd.read_csv("data/processed/cleaned_data.csv")

X = df.drop('class', axis=1)
y = df['class']

# STRATIFIED SPLIT (VERY IMPORTANT)
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# BALANCED + STRONG RANDOM FOREST
model = RandomForestClassifier(
    n_estimators=300,          # stronger ensemble
    random_state=42,
    class_weight='balanced',  #  KEY FIX
    n_jobs=-1
)

model.fit(X_train, y_train)

# Save model
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/intrusion_model.pkl")

# Evaluation
y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n")
print(classification_report(
    y_test,
    y_pred,
    target_names=[
        "Normal",
        "DoS",
        "Probe",
        "R2L",
        "U2R"
    ]
))
