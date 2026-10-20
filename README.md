# 🎬 Customer Churn Prediction System (End-to-End ML & NLP Pipeline)

![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit_learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

Solusi *End-to-End Data Science* untuk memprediksi risiko *customer churn* pada platform *streaming video*. Proyek ini mengintegrasikan pemrosesan data dari database relational (PostgreSQL), ekstraksi fitur sentimen ulasan menggunakan *Natural Language Processing* (NLP), pelatihan model Machine Learning (*Random Forest*), dan penyajian *dashboard* interaktif *real-time* berbasis Streamlit.

---

## 📌 Business Problem & Motivation

Di industri media dan layanan *subscription*, biaya akuisisi pelanggan baru (*Customer Acquisition Cost / CAC*) bisa mencapai **5–25x lebih mahal** dibandingkan mempertahankan pelanggan yang ada (*Customer Retention*). 

**Tujuan Proyek:**
1. Membangun sistem deteksi dini (*early-warning system*) untuk mengidentifikasi pengguna yang berpotensi berhenti berlangganan (*churn*) dalam 14 hari ke depan.
2. Memahami *behavioral factors* (jam tonton, frekuensi aktif) dan *emotions/feedbacks* (sentimen ulasan) yang paling mempengaruhi keputusan *churn*.
3. Menyediakan alat bantu keputusan (*decision-support tool*) bagi tim pemasaran melalui *dashboard* interaktif.

---

## 🛠️ Tech Stack & Architecture

- **Database:** PostgreSQL (Aggregations, CTEs, Window Functions)
- **Data Engineering / ETL:** Python, Pandas, SQLAlchemy, Psycopg2
- **NLP & Feature Engineering:** Rule-Based Lexicon Sentiment Analysis
- **Machine Learning:** Scikit-Learn (Random Forest Classifier, Train-Test Split, Classification Report)
- **Interactive Web App:** Streamlit
- **Version Control:** Git & GitHub

### 🔄 Data Pipeline Workflow
```
[PostgreSQL Database] 
       │ (SQL ETL Query)
       ▼
[Pandas DataFrame Engine] 
       │ (Lexicon NLP Sentiment Scoring & One-Hot Encoding)
       ▼
[Train-Test Split (80:20 Stratified)] 
       │
       ▼
[Random Forest Classifier Model] 
       │
       ▼
[Streamlit Interactive Web Dashboard]
```

---

## 💡 Feature Engineering & NLP Approach

Dalam proyek ini, fitur ulasan tidak hanya diukur berdasarkan kuantitas panjang teks, melainkan dianalisis secara kualitatif menggunakan **Lexicon-Based Sentiment Analysis**:

* **Positive Lexicons:** `['lancar', 'puas', 'lengkap', 'suka', 'bagus', 'mantap', 'membantu', 'terjangkau', 'cepat', 'hd']` $\rightarrow$ menambah skor (`+1`)
* **Negative Lexicons:** `['mahal', 'sedikit', 'error', 'lemot', 'kecewa', 'ribet', 'unsubscribe', 'jelek', 'susah']` $\rightarrow$ mengurangi skor (`-1`)

> **Impact:** Mengubah fitur ulasan teks mentah menjadi skor emosional terukur melipatgandakan *Feature Importance* ulasan dari **14% menjadi 35.3%**, membuat model mampu memahami aspek psikologis pengguna.

---

## 📊 Model Evaluation & Business Insights

### 1. Feature Importance Breakdown
Model *Random Forest Classifier* mengidentifikasi 3 pilar utama penentu *churn*:
- **Total Watch Hours (~45.4%):** Variabel *behavioral* utama. Penurunan drastis durasi menonton adalah indikator tercepat pengguna akan *churn*.
- **Sentiment Score (~35.3%):** Tingkat kepuasan emosional pengguna dari ulasan teks.
- **Active Days (~18.9%):** Frekuensi log-in/aktivitas pengguna dalam 30 hari terakhir.

### 2. Strategy & Metric Optimization
- **Primary Metric Priority:** **Recall**
- **Business Justification:** Dalam kasus *churn prediction*, biaya akibat *False Negative* (gagal mendeteksi user yang beneran mau *churn* = kehilangan *Customer Lifetime Value*) jauh lebih besar dibandingkan risiko *False Positive* (salah memprediksi user aktif dikira *churn* = hanya rugi biaya promosi perpanjangan).

---

## 📂 Project Structure

```text
churn-prediction/
│
├── generate_data.py   # Script simulasi pembuatan 500 data sintetis di PostgreSQL
├── main.py            # Pipeline ETL, NLP preprocessing, training & evaluasi ML
├── app.py             # Dashboard Web Application menggunakan Streamlit
├── requirements.txt   # File pustaka/dependencies Python
├── .gitignore         # File pengecualian git
└── README.md          # Dokumentasi utama proyek
```

---

## 🚀 How to Run locally

### Prerequisites
1. Python 3.10+ terinstall.
2. PostgreSQL server berjalan lokal (misal via DBeaver / pgAdmin).

### Quickstart Guide

1. **Clone Repository:**
   ```bash
   git clone https://github.com/USERNAME_KAMU/churn-prediction.git
   cd churn-prediction
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate Data ke PostgreSQL:**
   Pastikan kredensial `DB_URL` pada script sesuai dengan password PostgreSQL lokal kamu.
   ```bash
   python generate_data.py
   ```

4. **Jalankan Machine Learning Evaluasi:**
   ```bash
   python main.py
   ```

5. **Luncurkan Streamlit Dashboard:**
   ```bash
   streamlit run app.py
   ```
   Buka browser di `http://localhost:8501` untuk mencoba dashboard interaktif.

---

## 👨‍💻 Author
- gp