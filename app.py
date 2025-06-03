import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Membaca data dari file ZIP yang diunggah
df = pd.read_csv("/mnt/data/shopee_review_stemming_ok.csv.zip")  # path file yang diunggah ke Streamlit

# Train simple model
def train_model():
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df['review'])
    y = df['label']
    model = LogisticRegression()
    model.fit(X, y)
    return model, vectorizer
