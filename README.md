# 🛡️ Network Intrusion Detection System (NIDS)

It is a **web-based Network Intrusion Detection System** built using **Python, Flask, Scikit-learn, and Chart.js**.  
The system detects **multi-class network attacks** and visualizes predictions, probabilities, and live alerts through a web interface.

---

## 📌 Project Highlights

- ✅ Multi-class intrusion detection (Normal, DoS, Probe, R2L, U2R)
- ✅ Machine Learning model using Random Forest
- ✅ Interactive Flask-based web dashboard
- ✅ Dynamic probability visualization (Chart.js)
- ✅ **Simulated real-time traffic detection** (OS-independent)
- ✅ Live intrusion alerts

---

## 🧠 Attack Classes

| Class | Description |
|------|------------|
| Normal | Legitimate network traffic |
| DoS | Denial of Service attacks |
| Probe | Surveillance and scanning attacks |
| R2L | Remote to Local attacks |
| U2R | User to Root attacks |

---

## 🏗️ Project Architecture
network_intrusion_detection/
│
├── data/
│   ├── raw/
│   │   └── nsl_kdd.csv
│   ├── processed/
│   │   └── cleaned_data.csv
│
├── models/
│   └── intrusion_model.pkl
│
├── scripts/
│   ├── data_preprocessing.py
│   ├── train_model.py
|   └──generate_confusion_matrix.py
│
├── app.py
├── requirements.txt
├── templates/
│   └── index.html
│
└── README.md


---

## ⚙️ Technologies Used

- **Backend:** Python, Flask  
- **Machine Learning:** Scikit-learn (Random Forest)  
- **Frontend:** HTML, CSS, JavaScript  
- **Visualization:** Chart.js  
- **Data Processing:** Pandas, NumPy  

---

## Features Explained
- Manual Traffic Analysis
- Probability  Distribution
- Simulated Real-time IDS
- Live Alerts

---

## Future Enhancements
- Real packet sniffing using Npcap
- Deep learning-based IDS(LSTM)
- User authentication and access control
- Docker-based deployment

---

## 🚀 How to Run the Project

### 1️⃣ Clone the Repository

git clone https://github.com/Drag0nop/network-intrusion-detection-system
cd NIDS

### 2️⃣ Install Dependencies
pip install -r requirements.txt

### 3️⃣ Train the Model
python scripts/data_preprocessing.py
python scripts/train_model.py

### 4️⃣ Run Flask Application
python app.py

### open your browser
http://127.0.0.1:5000
