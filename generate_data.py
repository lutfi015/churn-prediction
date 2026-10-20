import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text

# 1. Koneksi ke Database
DB_URL = "postgresql+psycopg2://postgres:admin@localhost:5432/postgres"
engine = create_engine(DB_URL)

print("Membuat 500 data dummy di PostgreSQL...")

plans = ['Basic', 'Standard', 'Premium']
reviews_pos = [
    'Aplikasi lancar jaya dan film lengkap', 
    'Suka banget sama rekomendasi tayangannya', 
    'Kualitas HD mantap ga pernah lag',
    'Fitur download offline sangat membantu'
]
reviews_neg = [
    'Mahal tapi koleksi film sedikit sekali', 
    'Sering error pas mau nonton', 
    'Aplikasi lemot banget kecewa',
    'Sistem pembayaran ribet mending unsubscribe'
]

with engine.begin() as conn:
    # Bersihkan data lama
    conn.execute(text("TRUNCATE customer_reviews, activity_logs, users CASCADE;"))

    for i in range(1, 501):
        user_id = f"USR-{1000 + i}"
        signup_date = datetime.now() - timedelta(days=random.randint(60, 180))
        plan = random.choice(plans)

        conn.execute(
            text("INSERT INTO users (user_id, signup_date, plan_type) VALUES (:u, :s, :p)"),
            {"u": user_id, "s": signup_date, "p": plan}
        )

        # 30% peluang user churn
        is_churn = random.random() < 0.3

        if is_churn:
            # User churn: nggak nonton sama sekali dalam 15-40 hari terakhir
            if random.random() > 0.4:
                last_active = datetime.now() - timedelta(days=random.randint(15, 40))
                conn.execute(
                    text("INSERT INTO activity_logs (user_id, watch_hours, log_date) VALUES (:u, :w, :l)"),
                    {"u": user_id, "w": round(random.uniform(0.5, 2.0), 2), "l": last_active}
                )
            conn.execute(
                text("INSERT INTO customer_reviews (user_id, review_text, review_date) VALUES (:u, :r, :d)"),
                {"u": user_id, "r": random.choice(reviews_neg), "d": datetime.now() - timedelta(days=20)}
            )
        else:
            # User aktif: sering nonton dalam 1-10 hari terakhir
            for _ in range(random.randint(2, 6)):
                log_date = datetime.now() - timedelta(days=random.randint(1, 10))
                conn.execute(
                    text("INSERT INTO activity_logs (user_id, watch_hours, log_date) VALUES (:u, :w, :l)"),
                    {"u": user_id, "w": round(random.uniform(1.0, 5.0), 2), "l": log_date}
                )
            conn.execute(
                text("INSERT INTO customer_reviews (user_id, review_text, review_date) VALUES (:u, :r, :d)"),
                {"u": user_id, "r": random.choice(reviews_pos), "d": datetime.now() - timedelta(days=5)}
            )

print("Sukses! 500 data dummy berhasil masuk ke database.")