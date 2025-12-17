from flask import Flask, render_template, request
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)

# Load trained artifacts
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

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    confidence = None
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
            scaled = scaler.transform(input_df)

            probabilities = model.predict_proba(scaled)[0]
            predicted_class = np.argmax(probabilities)

            prediction = LABEL_MAP[predicted_class]
            confidence = round(probabilities[predicted_class] * 100, 2)

        except Exception as e:
            error = f"❌ Input error: {e}"

    return render_template(
        'index.html',
        prediction=prediction,
        confidence=confidence,
        error=error
    )

if __name__ == '__main__':
    app.run(debug=True)
