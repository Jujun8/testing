
import ipywidgets as widgets
from IPython.display import display, clear_output


# Dummy data for demonstration
customer_reviews = [
    {"product": "Product A", "review": "Sangat puas dengan produk ini!"},
    {"product": "Product B", "review": "Barang cepat sampai, kualitas bagus."},
    {"product": "Product A", "review": "Lumayan, tapi pengiriman agak lama."},
    {"product": "Product C", "review": "Tidak sesuai deskripsi, sangat kecewa."},
    {"product": "Product B", "review": "Mantap!"},
]

# Function to simulate sentiment analysis (very basic)
def analyze_sentiment(review):
    review_lower = review.lower()
    if "puas" in review_lower or "bagus" in review_lower or "mantap" in review_lower:
        return "Positif"
    elif "kecewa" in review_lower or "tidak sesuai" in review_lower:
        return "Negatif"
    else:
        return "Netral"

# Function to display reviews for a specific product
def display_product_reviews(product_name):
    clear_output(wait=True)
    print(f"Review untuk {product_name}:")
    found_reviews = False
    for review_data in customer_reviews:
        if review_data["product"] == product_name:
            sentiment = analyze_sentiment(review_data["review"])
            print(f"- {review_data['review']} (Sentimen: {sentiment})")
            found_reviews = True
    if not found_reviews:
        print("Belum ada review untuk produk ini.")
    display(widgets.Button(description="Kembali ke Halaman Utama", on_click=lambda b: display_main_page()))

# Function to display the main page
def display_main_page():
    clear_output(wait=True)
    print("Halaman Utama: Analisis Kepuasan Pelanggan Shopee (Berdasarkan Review)")

    # Total Reviews
    total_reviews = len(customer_reviews)
    print(f"\nTotal Review: {total_reviews}")

    # Sentiment Distribution
    positive_count = 0
    negative_count = 0
    neutral_count = 0
    for review_data in customer_reviews:
        sentiment = analyze_sentiment(review_data["review"])
        if sentiment == "Positif":
            positive_count += 1
        elif sentiment == "Negatif":
            negative_count += 1
        else:
            neutral_count += 1

    print(f"\nDistribusi Sentimen:")
    print(f"- Positif: {positive_count}")
    print(f"- Negatif: {negative_count}")
    print(f"- Netral: {neutral_count}")

    # Product-wise Review Links
    print("\nPilih Produk untuk Melihat Review:")
    unique_products = sorted(list(set([review["product"] for review in customer_reviews])))

    for product in unique_products:
        button = widgets.Button(description=product)
        button.on_click(lambda b, prod=product: display_product_reviews(prod))
        display(button)

# Function to display the 'About' page
def display_about_page():
    clear_output(wait=True)
    print("Halaman Tentang:")
    print("Aplikasi sederhana untuk menganalisis kepuasan pelanggan Shopee berdasarkan review.")
    print("Dibuat menggunakan Google Colaboratory/Jupyter Notebooks.")
    print("Analisis sentimen yang digunakan sangat dasar dan hanya untuk demonstrasi.")
    display(widgets.Button(description="Kembali ke Halaman Utama", on_click=lambda b: display_main_page()))

# Create navigation buttons
main_button = widgets.Button(description="Halaman Utama")
about_button = widgets.Button(description="Tentang")

# Link buttons to their respective pages
main_button.on_click(lambda b: display_main_page())
about_button.on_click(lambda b: display_about_page())

# Display the navigation buttons initially
display(widgets.HBox([main_button, about_button]))

# Display the main page on startup
display_main_page()
