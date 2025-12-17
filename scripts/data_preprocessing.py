import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib
import os

def preprocess_data():
    # Load dataset
    df = pd.read_csv("data/raw/kdd_dataset.csv")

    # Drop difficulty column if present
    if 'difficulty' in df.columns:
        df.drop(columns=['difficulty'], inplace=True)

    # 🔥 Create and store encoders
    encoders = {}

    for col in ['protocol_type', 'service', 'flag']:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le

    # 🔥 MULTI-CLASS ATTACK MAPPING
    attack_mapping = {
        'normal': 0,

        # DoS
        'neptune': 1, 'smurf': 1, 'back': 1,
        'teardrop': 1, 'land': 1, 'pod': 1,

        # Probe
        'satan': 2, 'ipsweep': 2,
        'portsweep': 2, 'nmap': 2,

        # R2L
        'guess_passwd': 3, 'ftp_write': 3,
        'imap': 3, 'phf': 3,
        'multihop': 3, 'warezmaster': 3,
        'warezclient': 3,

        # U2R
        'buffer_overflow': 4, 'loadmodule': 4,
        'rootkit': 4, 'perl': 4
    }

    df['class'] = df['class'].map(attack_mapping)
    df.dropna(inplace=True)
    df['class'] = df['class'].astype(int)

    # ✅ ONLY 10 FEATURES
    selected_features = [
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

    X = df[selected_features]
    y = df['class']

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Create folders
    os.makedirs("models", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)

    # 🔥 SAVE scaler and encoders
    joblib.dump(scaler, "models/scaler.pkl")
    joblib.dump(encoders, "models/encoders.pkl")

    # Save processed data
    processed_df = pd.DataFrame(X_scaled, columns=selected_features)
    processed_df['class'] = y.values
    processed_df.to_csv("data/processed/cleaned_data.csv", index=False)

    print("✅ Data preprocessing completed successfully (MULTI-CLASS + encoders saved)")

if __name__ == "__main__":
    preprocess_data()
