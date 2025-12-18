import numpy as np
import matplotlib.pyplot as plt
import joblib
import pandas as pd
import os

# Load model
model = joblib.load("models/intrusion_model.pkl")

# Example attack input (DoS-like)
sample = pd.DataFrame([[
    0, 1, 20, 1, 0, 0, 500, 500, 1.0, 0.0
]], columns=[
    'duration', 'protocol_type', 'service', 'flag',
    'src_bytes', 'dst_bytes', 'count', 'srv_count',
    'same_srv_rate', 'diff_srv_rate'
])

# Predict probabilities
probs = model.predict_proba(sample)[0]

labels = ["Normal", "DoS", "Probe", "R2L", "U2R"]

plt.bar(labels, probs)
plt.ylabel("Probability")
plt.title("Attack Probability Distribution")
os.makedirs("static/plots", exist_ok=True)
plt.savefig("static/plots/confusion_matrix.png")
plt.close()
plt.close()