import streamlit as st

# Dummy data review
customer_reviews = [
    {"product": "Product A", "review": "Sangat puas dengan produk ini!"},
    {"product": "Product B", "review": "Barang cepat sampai, kualitas bagus."},
    {"product": "Product A", "review": "Lumayan, tapi pengiriman agak lama."},
    {"product": "Product C", "review": "Tidak sesuai deskripsi, sangat kecewa."},
    {"product": "Product B", "review": "Mantap!"},
]

# Fungsi analisis sentimen sederhana
def analyze_sentiment(review):
    review_lower = review.lower()
    if "puas" in review_lower or "bagus" in review_lower or "mantap" in review_lower:
        return "Positif"
    elif "kecewa" in review_lower or "tidak sesuai" in review_lower:
        return "Negatif"
    else:
        return "Netral"

# Buat halaman utama
def main_page():
    st.title("📊 Analisis Kepuasan Pelanggan Shopee")
    st.subheader("Berdasarkan Review")

    st.write(f"**Total Review:** {len(customer_reviews)}")

    # Hitung distribusi sentimen
    sentiments = [analyze_sentiment(r['review']) for r in customer_reviews]
    positif = sentiments.count("Positif")
    negatif = sentiments.count("Negatif")
    netral = sentiments.count("Netral")

    st.write("### Distribusi Sentimen")
    st.bar_chart({"Sentimen": {"Positif": positif, "Negatif": negatif, "Netral": netral}})

    st.write("### Pilih Produk untuk Melihat Review")
    unique_products = sorted(set([r["product"] for r in customer_reviews]))
    selected_product = st.selectbox("Pilih Produk", unique_products)

    if st.button("Lihat Review"):
        show_product_reviews(selected_product)

# Halaman review produk tertentu
def show_product_reviews(product_name):
    st.write(f"## Review untuk {product_name}")
    found = False
    for r in customer_reviews:
        if r['product'] == product_name:
            sentiment = analyze_sentiment(r['review'])
            st.write(f"- {r['review']} (Sentimen: **{sentiment}**)") 
            found = True
    if not found:
        st.write("Belum ada review untuk produk ini.")

# Halaman tentang
def about_page():
    st.title("📘 Tentang Aplikasi")
    st.write("""
    Aplikasi ini dibuat untuk menganalisis kepuasan pelanggan Shopee berdasarkan ulasan produk.
    
    - Dibuat dengan Streamlit
    - Menggunakan analisis sentimen dasar (keyword-based)
    - Hanya untuk keperluan demo/data mining sederhana
    """)

# Navigasi halaman
page = st.sidebar.selectbox("Navigasi", ["Halaman Utama", "Tentang"])

if page == "Halaman Utama":
    main_page()
elif page == "Tentang":
    about_page()
