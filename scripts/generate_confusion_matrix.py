import pandas as pd
import joblib
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import os

model = joblib.load("models/intrusion_model.pkl")
df = pd.read_csv("data/processed/cleaned_data.csv")

X = df.drop("class", axis=1)
y = df["class"]

y_pred = model.predict(X)

labels = [0, 1, 2, 3, 4]
names = ["Normal", "DoS", "Probe", "R2L", "U2R"]

cm = confusion_matrix(y, y_pred, labels=labels)

disp = ConfusionMatrixDisplay(cm, display_labels=names)
disp.plot(cmap="Blues")
plt.title("Confusion Matrix – NIDS")

os.makedirs("static/plots", exist_ok=True)
plt.savefig("static/plots/confusion_matrix.png")
plt.close()

print("✅ Confusion matrix saved")
