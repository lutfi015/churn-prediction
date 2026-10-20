import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from sklearn.ensemble import RandomForestClassifier

# --------------------------------------------------
# 1. SETUP HLAMAN & ENGINE DATABASE
# --------------------------------------------------
st.set_page_config(page_title="Churn Prediction Dashboard", layout="centered")

st.title("🎬 Customer Churn Prediction Dashboard")
st.write("Aplikasi interaktif buat memprediksi risiko churn pengguna berdasarkan riwayat aktivitas dan sentimen ulasan.")

# Ganti PASSWORD_KAMU dengan password PostgreSQL milikmu
DB_URL = "postgresql+psycopg2://postgres:admin@localhost:5432/postgres"

@st.cache_resource
def get_engine():
    return create_engine(DB_URL)

engine = get_engine()

# --------------------------------------------------
# 2. TRAIN MODEL SAAT APLIKASI DIBUKA
# --------------------------------------------------
def get_sentiment_score(text):
    if not isinstance(text, str):
        return 0
    pos_words = ['lancar', 'puas', 'lengkap', 'suka', 'bagus', 'mantap', 'membantu', 'terjangkau', 'cepat', 'hd']
    neg_words = ['mahal', 'sedikit', 'error', 'lemot', 'kecewa', 'ribet', 'unsubscribe', 'jelek', 'susah']
    
    words = text.lower().split()
    score = 0
    for w in words:
        if w in pos_words:
            score += 1
        elif w in neg_words:
            score -= 1
    return score

@st.cache_data
def train_model():
    query = """
    WITH user_usage AS (
        SELECT 
            user_id,
            SUM(watch_hours) AS total_watch_hours,
            COUNT(DISTINCT DATE(log_date)) AS active_days,
            MAX(log_date) AS last_active_date
        FROM activity_logs
        WHERE log_date >= CURRENT_DATE - INTERVAL '30 days'
        GROUP BY user_id
    )
    SELECT 
        u.user_id,
        u.plan_type,
        COALESCE(uu.total_watch_hours, 0) AS total_watch_hours,
        COALESCE(uu.active_days, 0) AS active_days,
        cr.review_text,
        CASE 
            WHEN uu.last_active_date IS NULL OR uu.last_active_date < CURRENT_DATE - INTERVAL '14 days' THEN 1 
            ELSE 0 
        END AS is_churn
    FROM users u
    LEFT JOIN user_usage uu ON u.user_id = uu.user_id
    LEFT JOIN customer_reviews cr ON u.user_id = cr.user_id;
    """
    df = pd.read_sql(query, engine)
    df['sentiment_score'] = df['review_text'].apply(get_sentiment_score)
    df_encoded = pd.get_dummies(df, columns=['plan_type'])
    
    feature_cols = ['total_watch_hours', 'active_days', 'sentiment_score', 
                    'plan_type_Basic', 'plan_type_Standard', 'plan_type_Premium']
    
    X = df_encoded[feature_cols]
    y = df_encoded['is_churn']
    
    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)
    return model, feature_cols

model, feature_cols = train_model()

# --------------------------------------------------
# 3. INPUT USER DARI SIDEBAR / PANEL INTERAKTIF
# --------------------------------------------------
st.sidebar.header("⚙️ Input Parameter User Baru")

watch_hours = st.sidebar.slider("Total Jam Nonton (30 Hari)", 0.0, 30.0, 10.0, step=0.5)
active_days = st.sidebar.slider("Hari Aktif Nonton (30 Hari)", 0, 30, 5)
plan_type = st.sidebar.selectbox("Tipe Paket", ["Basic", "Standard", "Premium"])
review_text = st.sidebar.text_area("Tulis Review User", "Aplikasi lancar dan mantap banget")

# --------------------------------------------------
# 4. PREDIKSI DATA INPUT
# --------------------------------------------------
user_sentiment = get_sentiment_score(review_text)

input_data = pd.DataFrame([{
    'total_watch_hours': watch_hours,
    'active_days': active_days,
    'sentiment_score': user_sentiment,
    'plan_type_Basic': 1 if plan_type == 'Basic' else 0,
    'plan_type_Standard': 1 if plan_type == 'Standard' else 0,
    'plan_type_Premium': 1 if plan_type == 'Premium' else 0
}])

# Pastikan urutan kolom sesuai training
input_data = input_data[feature_cols]

prediction = model.predict(input_data)[0]
probability = model.predict_proba(input_data)[0]

# --------------------------------------------------
# 5. TAMPILKAN HASIL PREDIKSI DI DASHBOARD
# --------------------------------------------------
st.subheader("📊 Hasil Analisis Prediksi")

col1, col2 = st.columns(2)
with col1:
    st.metric("Skor Sentimen Review", f"{user_sentiment}")
with col2:
    st.metric("Probabilitas Churn", f"{probability[1]*100:.1f}%")

if prediction == 1:
    st.error("⚠️ **Peringatan:** User ini berisiko tinggi **CHURN** (Akan berhenti berlangganan)!")
    st.info("💡 **Rekomendasi Action:** Kirimkan promo diskon perpanjangan atau rekomendasi film via Push Notification.")
else:
    st.success("✅ **Aman:** User ini diprediksi **ALIRAN AKTIF** (Kecil kemungkinan churn).")