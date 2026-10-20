-- ===================================================
-- 1. TAHAP PEMBUATAN TABEL (DDL)
-- ===================================================

-- Tabel 1: Data Profil Pengguna
CREATE TABLE users (
    user_id VARCHAR(20) PRIMARY KEY,
    signup_date DATE,
    plan_type VARCHAR(10)
);

-- Tabel 2: Catatan Aktivitas Nonton
CREATE TABLE activity_logs (
    log_id SERIAL PRIMARY KEY,
    user_id VARCHAR(20) REFERENCES users(user_id),
    watch_hours NUMERIC(5,2),
    log_date DATE
);

-- Tabel 3: Ulasan Pelanggan
CREATE TABLE customer_reviews (
    review_id SERIAL PRIMARY KEY,
    user_id VARCHAR(20) REFERENCES users(user_id),
    review_text TEXT,
    review_date DATE
);

-- ===================================================
-- 2. TAHAP PENGISIAN DATA SAMPEL (DML)
-- ===================================================

INSERT INTO users (user_id, signup_date, plan_type) VALUES
('USR-1000', '2026-01-15', 'Basic'),
('USR-1001', '2026-02-01', 'Premium'),
('USR-1002', '2026-01-10', 'Standard'),
('USR-1003', '2026-03-05', 'Standard'),
('USR-1004', '2026-02-20', 'Basic');

INSERT INTO activity_logs (user_id, watch_hours, log_date) VALUES
('USR-1000', 2.50, '2026-10-15'),
('USR-1001', 3.90, '2026-10-17'),
('USR-1002', 1.20, '2026-09-01'),
('USR-1003', 4.10, '2026-10-18'),
('USR-1004', 1.50, '2026-10-14');

INSERT INTO customer_reviews (user_id, review_text, review_date) VALUES
('USR-1000', 'Sangat puas filmnya lengkap dan kualitas HD', '2026-10-16'),
('USR-1001', 'Fitur download offline sangat membantu', '2026-10-17'),
('USR-1002', 'Mahal tapi koleksi film sedikit sekali', '2026-09-02'),
('USR-1003', 'Rekomendasi tayangan bagus banget suka sekali', '2026-10-18'),
('USR-1004', 'Aplikasi cepat lancar dan harga terjangkau', '2026-10-15');