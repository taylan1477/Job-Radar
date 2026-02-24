# nlp_processor.py
import re
import warnings
import numpy as np
from corpus import EXPANDED_FIELD_CORPUS

# sklearn import (yoksa graceful fallback)
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    warnings.warn("scikit-learn bulunamadi! TF-IDF devredisi.")

def normalize_text(text):
    """Metni lowercase ve temizlenmis hale getirir."""
    if not text:
        return ""
    text = str(text).lower()
    # HTML tag'lerini temizle
    text = re.sub(r"<[^>]+>", " ", text)
    # URL'leri temizle
    text = re.sub(r"https?://\S+", " ", text)
    # Fazla bosluklari temizle
    text = re.sub(r"\s+", " ", text).strip()
    return text

def detect_language(text):
    """
    Metnin dilini tespit eder (en, tr, es, de, vb.)
    Hata durumunda None doner.
    """
    try:
        from langdetect import detect
        if len(text) > 20: 
            return detect(text)
    except ImportError:
        pass
    except Exception:
        pass
    return None

class FieldDetector:
    """TF-IDF tabanli alan tespiti yapan sinif."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FieldDetector, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
            
        self.vectorizer = None
        self.field_vectors = None
        self.field_names = []
        self._init_tfidf()
        self._initialized = True

    def _init_tfidf(self):
        if not SKLEARN_AVAILABLE:
            return

        corpus_texts = []
        self.field_names = []
        
        for field, text in EXPANDED_FIELD_CORPUS.items():
            corpus_texts.append(text)
            self.field_names.append(field)
            
        # Turkce Stop Words
        tr_stop_words = [
            "ve", "veya", "ile", "ama", "fakat", "lakin", "ancak", "cunku", "da", "de",
            "icin", "gibi", "kadar", "olan", "bir", "bu", "su", "o", "var", "yok",
            "mi", "mu", "mı", "mü", "daha", "en", "cok", "az", "bi", "ben", "sen",
            "biz", "siz", "onlar", "ne", "neden", "nasil", "niye", "ki", "ise",
            "diye", "yani", "iste", "bile", "dahi", "sonra", "once", "karsi"
        ]
        
        try:
            from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
            all_stop_words = list(ENGLISH_STOP_WORDS) + tr_stop_words
            
            self.vectorizer = TfidfVectorizer(
                stop_words=all_stop_words,
                ngram_range=(1, 2),
                min_df=1
            )
            self.field_vectors = self.vectorizer.fit_transform(corpus_texts)
        except Exception as e:
            print(f"  [HATA] TF-IDF Init Hatasi: {e}")

    def predict(self, text):
        """Metnin hangi alana ait oldugunu tahmin eder."""
        if not SKLEARN_AVAILABLE or not self.vectorizer:
            return None
            
        try:
            text_vector = self.vectorizer.transform([text])
            similarities = cosine_similarity(text_vector, self.field_vectors).flatten()
            best_idx = similarities.argmax()
            best_score = similarities[best_idx]
            
            if best_score < 0.1:
                return None
                
            return self.field_names[best_idx]
        except Exception as e:
            print(f"  [HATA] TF-IDF Tahmin: {e}")
            return None
