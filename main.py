import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

# 1. KONEKSI & TARIK DATA DARI POSTGRESQL
DB_URL = "postgresql+psycopg2://postgres:admin@localhost:5432/postgres"
engine = create_engine(DB_URL)

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

# 2. FEATURE ENGINEERING: NLP SENTIMENT ANALYSIS (LEXICON-BASED)
def get_sentiment_score(text):
    if not isinstance(text, str):
        return 0  # Skor 0 jika tidak ada review
    
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

# Terapkan fungsi sentimen ke dataset
df['sentiment_score'] = df['review_text'].apply(get_sentiment_score)

# One-Hot Encoding untuk plan_type
df_encoded = pd.get_dummies(df, columns=['plan_type'])

# Gunakan 'sentiment_score' sebagai fitur baru menggantikan 'review_length'
feature_cols = ['total_watch_hours', 'active_days', 'sentiment_score', 
                'plan_type_Basic', 'plan_type_Standard', 'plan_type_Premium']

X = df_encoded[feature_cols]
y = df_encoded['is_churn']

# 3. TRAIN-TEST SPLIT (80% Train, 20% Test)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 4. TRAINING MODEL
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# 5. PREDIKSI DATA TEST
y_pred = model.predict(X_test)

# 6. HASIL EVALUASI
print("\n=== CLASSIFICATION REPORT ===")
print(classification_report(y_test, y_pred))

importance = pd.DataFrame({
    'Fitur': feature_cols,
    'Pengaruh (%)': model.feature_importances_ * 100
}).sort_values(by='Pengaruh (%)', ascending=False)

print("\n=== FITUR PALING BERPENGARUH TERHADAP CHURN ===")
print(importance)