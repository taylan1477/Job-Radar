# analyze_keywords.py
import pandas as pd
from collections import Counter
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

# Mevcut modullerden veri cekmek icin
from src.clients.rss_sources import fetch_all_jobs as fetch_rss_jobs
from src.core.scorer import score_job

def analyze_jobs():
    print("Veri cekiliyor (RSS kaynaklari - Ucretsiz)...")
    # Sadece RSS kullan (Hizli ve API keysiz)
    jobs = fetch_rss_jobs()
    
    if not jobs:
        print("Hic ilan bulunamadi.")
        return

    print(f"{len(jobs)} ilan cekildi. Skorlaniyor...")
    
    # DataFrame'e cevir
    scored_jobs = [score_job(j) for j in jobs]
    df = pd.DataFrame(scored_jobs)
    
    # "Diger" veya "Yazilim" olanlari filtrele (Spesifik olmayanlar)
    others = df[df['field'].isin(['diğer', 'yazılım', 'bilinmiyor'])]
    gamedev = df[df['field'] == 'gamedev']
    
    print(f"\nToplam: {len(df)}")
    print(f"Gamedev: {len(gamedev)}")
    print(f"Diger/Yazilim/Bilinmiyor: {len(others)}")
    
    if others.empty:
        print("Analiz edilecek 'Diger' ilan yok.")
        return

    # Metinleri birlestir
    text_corpus = []
    for _, row in others.iterrows():
        # Title ve Summary'i al
        text = f"{row.get('title', '')} {row.get('summary', '')}"
        text_corpus.append(text)
        
    print("\n--- 'Diger' Kategorisindeki Sik Gecen Kelimeler (TF-IDF Harici Basit Sayim) ---")
    all_text = " ".join(text_corpus).lower()
    # Basit temizlik
    all_text = re.sub(r'<[^>]+>', '', all_text)
    all_text = re.sub(r'[^a-z\s]', '', all_text)
    
    words = all_text.split()
    # Stop words temizligi
    filtered_words = [w for w in words if w not in ENGLISH_STOP_WORDS and len(w) > 3]
    
    common = Counter(filtered_words).most_common(20)
    for word, count in common:
        print(f"{word}: {count}")

    print("\n--- TF-IDF ile Ayirt Edici Kelimeler ---")
    # TF-IDF
    vectorizer = TfidfVectorizer(stop_words='english', max_features=20)
    try:
        tfidf_matrix = vectorizer.fit_transform(text_corpus)
        feature_names = vectorizer.get_feature_names_out()
        print("En yuksek skorlu terimler:", ", ".join(feature_names))
    except ValueError:
        print("Yeterli veri yok veya kelime hazinesi olusturulamadi.")

if __name__ == "__main__":
    analyze_jobs()
