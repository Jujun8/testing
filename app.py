import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import os

# Membaca data dari file Excel
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("shopee_review_stemming_ok.csv.zip")  # Pastikan file berada di folder yang sama dengan file app.py
        return df
    except Exception as e:
        st.error(f"Gagal membaca file Excel: {e}")
        return pd.DataFrame(columns=["product", "review", "label"])

df = load_data()

# Train simple model
def train_model(data):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(data['review'])
    y = data['label']
    model = LogisticRegression()
    model.fit(X, y)
    return model, vectorizer

# Sentiment prediction
def predict_sentiment(review_text, model, vectorizer):
    X = vectorizer.transform([review_text])
    prediction = model.predict(X)[0]
    proba = model.predict_proba(X).max()
    return prediction, proba

# ---------- Streamlit UI ----------
st.set_page_config(page_title="Dashboard Shopee Sentimen", layout="centered")

st.sidebar.title("📊 Navigasi Halaman")
page = st.sidebar.radio("Pilih Halaman", ["Halaman Awal", "Pelatihan Model", "Prediksi Review"])

# ------- Page 1: Dataset & Statistik -------
if page == "Halaman Awal":
    st.title("🛒 Halaman Awal - Dataset Review Shopee")
    
    if df.empty:
        st.warning("Dataset tidak tersedia atau gagal dimuat.")
    else:
        st.subheader("📦 Dataset Review")
        st.dataframe(df)

        st.subheader("📈 Distribusi Sentimen")
        sentiment_count = df['label'].value_counts()
        st.bar_chart(sentiment_count)

        st.subheader("📌 Produk Tersedia")
        st.write(df['product'].unique())

# ------- Page 2: Pelatihan Model -------
elif page == "Pelatihan Model":
    st.title("⚙️ Halaman Pelatihan Model")
    if df.empty:
        st.warning("Tidak bisa melatih model karena dataset kosong.")
    else:
        st.write("Melatih model klasifikasi sentimen berdasarkan ulasan pelanggan...")

        model, vectorizer = train_model(df)

        st.success("✅ Model berhasil dilatih!")
        st.subheader("🔍 Contoh Prediksi Otomatis")
        for review in df['review']:
            pred, _ = predict_sentiment(review, model, vectorizer)
            st.write(f"- \"{review}\" → **{pred}**")

# ------- Page 3: Form Prediksi Review -------
elif page == "Prediksi Review":
    st.title("📝 Halaman Prediksi Review")
    st.write("Masukkan teks review pelanggan dan dapatkan prediksi sentimen.")

    if df.empty:
        st.warning("Tidak bisa memproses prediksi karena dataset kosong.")
    else:
        model, vectorizer = train_model(df)

        with st.form("form_prediksi"):
            user_input = st.text_area("Masukkan Review Anda di Sini")
            submitted = st.form_submit_button("Prediksi")

            if submitted and user_input.strip():
                pred, prob = predict_sentiment(user_input, model, vectorizer)
                st.success(f"Prediksi Sentimen: **{pred.capitalize()}** (Probabilitas: {prob:.2f})")
