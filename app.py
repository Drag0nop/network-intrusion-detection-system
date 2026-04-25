from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
import numpy as np
import os
import time
from threading import Thread

app = Flask(__name__)

model = joblib.load("models/intrusion_model.pkl")
scaler = joblib.load("models/scaler.pkl")
encoders = joblib.load("models/encoders.pkl")

FEATURE_NAMES = [
    'duration',
    'protocol_type',
    'service',
    'flag',
    'src_bytes',
    'dst_bytes',
    'count',
    'srv_count',
    'same_srv_rate',
    'diff_srv_rate'
]

LABEL_MAP = {
    0: "✅ Normal Traffic",
    1: "🚨 DoS Attack",
    2: "🕵️ Probe Attack",
    3: "🔐 R2L Attack",
    4: "⚠️ U2R Attack"
}

# REAL-TIME ALERT STORAGE
alerts = []
stream_running = True

# SIMULATED REAL-TIME STREAM
def simulated_stream():
    global alerts

    df = pd.read_csv("data/processed/cleaned_data.csv")

    for _, row in df.iterrows():
        if not stream_running:
            break

        # Select ONLY required features
        input_df = pd.DataFrame(
            [[row[col] for col in FEATURE_NAMES]],
            columns=FEATURE_NAMES
        )

        scaled_array = scaler.transform(input_df)
        scaled_df = pd.DataFrame(scaled_array, columns=FEATURE_NAMES)

        probs = model.predict_proba(scaled_df)[0]
        pred = int(np.argmax(probs))

        if pred != 0:
            alerts.append({
                "type": LABEL_MAP[pred],
                "confidence": round(float(probs[pred]) * 100, 2)
            })

            if len(alerts) > 10:
                alerts.pop(0)

        time.sleep(2)  # simulate real-time delay

# START SIMULATED STREAM
Thread(target=simulated_stream, daemon=True).start()

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    confidence = None
    probabilities = None
    error = None

    if request.method == 'POST':
        try:
            duration = float(request.form['duration'])

            protocol = encoders['protocol_type'].transform(
                [request.form['protocol']]
            )[0]

            service = encoders['service'].transform(
                [request.form['service']]
            )[0]

            flag = encoders['flag'].transform(
                [request.form['flag']]
            )[0]

            src_bytes = float(request.form['src_bytes'])
            dst_bytes = float(request.form['dst_bytes'])
            count = float(request.form['count'])
            srv_count = float(request.form['srv_count'])
            same_srv_rate = float(request.form['same_srv_rate'])
            diff_srv_rate = float(request.form['diff_srv_rate'])

            values = [
                duration, protocol, service, flag,
                src_bytes, dst_bytes, count, srv_count,
                same_srv_rate, diff_srv_rate
            ]

            input_df = pd.DataFrame([values], columns=FEATURE_NAMES)


            scaled_array = scaler.transform(input_df)
            scaled_df = pd.DataFrame(scaled_array, columns=FEATURE_NAMES)

            probs = model.predict_proba(scaled_df)[0]
            predicted_class = int(np.argmax(probs))

            prediction = LABEL_MAP[predicted_class]
            confidence = round(probs[predicted_class] * 100, 2)

            probabilities = {
                "Normal": float(probs[0]),
                "DoS": float(probs[1]),
                "Probe": float(probs[2]),
                "R2L": float(probs[3]),
                "U2R": float(probs[4])
            }

        except Exception as e:
            error = f"❌ Input error: {e}"

    return render_template(
        'index.html',
        prediction=prediction,
        confidence=confidence,
        probabilities=probabilities,
        error=error
    )

@app.route('/alerts')
def get_alerts():
    return jsonify(alerts)

if __name__ == '__main__':
    app.run(debug=True)
