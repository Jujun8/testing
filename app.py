import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Dummy data Shopee reviews
customer_reviews = [
    {"product": "Product A", "review": "Sangat puas dengan produk ini!", "label": "positif"},
    {"product": "Product B", "review": "Barang cepat sampai, kualitas bagus.", "label": "positif"},
    {"product": "Product A", "review": "Lumayan, tapi pengiriman agak lama.", "label": "netral"},
    {"product": "Product C", "review": "Tidak sesuai deskripsi, sangat kecewa.", "label": "negatif"},
    {"product": "Product B", "review": "Mantap!", "label": "positif"},
    {"product": "Product C", "review": "Jelek banget, kecewa parah.", "label": "negatif"},
]

# Convert to DataFrame
df = pd.DataFrame(customer_reviews)

# Train simple model
def train_model():
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df['review'])
    y = df['label']
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
    st.write("Melatih model klasifikasi sentimen berdasarkan ulasan pelanggan...")

    model, vectorizer = train_model()

    st.success("✅ Model berhasil dilatih!")
    st.subheader("🔍 Contoh Prediksi Otomatis")
    for review in df['review']:
        pred, _ = predict_sentiment(review, model, vectorizer)
        st.write(f"- \"{review}\" → **{pred}**")

# ------- Page 3: Form Prediksi Review -------
elif page == "Prediksi Review":
    st.title("📝 Halaman Prediksi Review")
    st.write("Masukkan teks review pelanggan dan dapatkan prediksi sentimen.")

    # Pastikan model sudah dilatih
    model, vectorizer = train_model()

    with st.form("form_prediksi"):
        user_input = st.text_area("Masukkan Review Anda di Sini")
        submitted = st.form_submit_button("Prediksi")

        if submitted and user_input.strip():
            pred, prob = predict_sentiment(user_input, model, vectorizer)
            st.success(f"Prediksi Sentimen: **{pred.capitalize()}** (Probabilitas: {prob:.2f})")
