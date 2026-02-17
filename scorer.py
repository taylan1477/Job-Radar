# scorer.py – Ilan Skorlama Modulu v0.5 (TF-IDF & NLP)

import re
import warnings
import numpy as np
from config import (
    FIELD_KEYWORDS, FIELD_SCORES, FIELD_PRIORITY,
    LOCATION_KEYWORDS, LOCATION_SCORES,
    LEVEL_KEYWORDS, LEVEL_SCORES,
    FIELD_WEIGHT, LOCATION_WEIGHT, LEVEL_WEIGHT,
    NEGATIVE_KEYWORDS, SOFTWARE_KEYWORDS,
    EXPANDED_FIELD_CORPUS
)

# sklearn import (yoksa graceful fallback)
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    warnings.warn("scikit-learn bulunamadi! TF-IDF yerine basit keyword eslesmesi kullanilacak.")

# Global TF-IDF bilesenleri (tek seferde init edilecek)
_VECTORIZER = None
_FIELD_VECTORS = None
_FIELD_NAMES = []


def _init_tfidf():
    """TF-IDF vektorlerini hazirlar (lazy loading)."""
    global _VECTORIZER, _FIELD_VECTORS, _FIELD_NAMES
    
    # Eger zaten init edildiyse veya sklearn yoksa cik
    if _VECTORIZER is not None or not SKLEARN_AVAILABLE:
        return

    corpus_texts = []
    _FIELD_NAMES = []
    
    # Corpus'tan metinleri ve etiketleri al
    for field, text in EXPANDED_FIELD_CORPUS.items():
        corpus_texts.append(text)
        _FIELD_NAMES.append(field)
        
    # Turkce Stop Words (Basit liste)
    tr_stop_words = [
        "ve", "veya", "ile", "ama", "fakat", "lakin", "ancak", "cunku", "da", "de",
        "icin", "gibi", "kadar", "olan", "bir", "bu", "su", "o", "var", "yok",
        "mi", "mu", "mı", "mü", "daha", "en", "cok", "az", "bi", "ben", "sen",
        "biz", "siz", "onlar", "ne", "neden", "nasil", "niye", "ki", "ise",
        "diye", "yani", "iste", "bile", "dahi", "sonra", "once", "karsi"
    ]
    
    # Vectorizer'i eğit (N-gram: 1 ve 2 kelimelik, hem ingilizce hem turkce stop words)
    try:
        from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
        all_stop_words = list(ENGLISH_STOP_WORDS) + tr_stop_words
        
        _VECTORIZER = TfidfVectorizer(
            stop_words=all_stop_words,
            ngram_range=(1, 2), # "game developer", "data scientist" gibi kaliplari yakalar
            min_df=1            # En az 1 dokumanda gecenleri al (zaten corpus kucuk)
        )
        _FIELD_VECTORS = _VECTORIZER.fit_transform(corpus_texts)
        # print(f"  [DEBUG] TF-IDF Matrisi: {_FIELD_VECTORS.shape}")
    except Exception as e:
        print(f"  [HATA] TF-IDF Init Hatasi: {e}")
        pass


def _normalize(text):
    """Metni lowercase ve temizlenmis hale getirir."""
    if not text:
        return ""
    text = str(text).lower()
    # HTML tag'lerini temizle
    text = re.sub(r"<[^>]+>", " ", text)
    # URL'leri temizle (yanlis eslesme onleme)
    text = re.sub(r"https?://\S+", " ", text)
    # Fazla bosluklari temizle
    text = re.sub(r"\s+", " ", text).strip()
    return text


def is_restricted(text):
    """
    Ilanin ulke/vize kisitlamasi olup olmadigini kontrol eder.
    True donerse ilan atlanmali.
    """
    text = _normalize(text)
    for kw in NEGATIVE_KEYWORDS:
        if kw.lower() in text:
            return True
    return False


def _count_keyword_hits(text, keywords):
    """Metinde kac keyword eslestirdigini sayar (Fallback yontemi)."""
    count = 0
    for kw in keywords:
        kw_lower = kw.lower()
        if " " in kw_lower:
            # Cok kelimeli: substring
            if kw_lower in text:
                count += 1
        elif len(kw_lower) >= 4:
            # Tek kelime, 4+ karakter: substring
            if kw_lower in text:
                count += 1
        else:
            # Kisa kelime: word boundary (c#, c++, go)
            if re.search(r'\b' + re.escape(kw_lower) + r'\b', text):
                count += 1
    return count


def detect_field_tfidf(text):
    """TF-IDF ve Cosine Similarity kullanarak alan tahmini yapar."""
    if not SKLEARN_AVAILABLE:
        return None
        
    _init_tfidf()
    if not _VECTORIZER:
        return None
    
    try:
        # Metni vektorize et
        text_vector = _VECTORIZER.transform([text])
        
        # Benzerlik hesapla
        similarities = cosine_similarity(text_vector, _FIELD_VECTORS).flatten()
        
        # En yuksek skoru bul
        best_idx = similarities.argmax()
        best_score = similarities[best_idx]
        
        # Threshold: 0.1 altindaysa guvenme
        if best_score < 0.1:
            return None
            
        return _FIELD_NAMES[best_idx]
    except Exception as e:
        print(f"  [HATA] TF-IDF Tahmin: {e}")
        return None


def detect_field(text, use_tfidf=True):
    """
    Hibrit Alan Tespiti:
    1. TF-IDF ile dene (daha akilli).
    2. Sonuc guvensizse veya sklearn yoksa Klasik Keyword sayimina don.
    """
    text = _normalize(text)

    # 1. Yontem: TF-IDF
    if use_tfidf and SKLEARN_AVAILABLE:
        detected = detect_field_tfidf(text)
        if detected:
            return detected

    # 2. Yontem: Keyword Hit Count (Yedek)
    best_field = "diğer"
    best_hits = 0
    best_priority = len(FIELD_PRIORITY) + 1

    for i, field in enumerate(FIELD_PRIORITY):
        keywords = FIELD_KEYWORDS.get(field, [])
        hits = _count_keyword_hits(text, keywords)
        
        # Kurallar: Daha cok hit alan kazanir. Esitse oncelik sirasi.
        if hits > best_hits or (hits == best_hits and hits > 0 and i < best_priority):
            best_hits = hits
            best_field = field
            best_priority = i

    # Eger hicbir ozel alan bulunamadiysa, genel yazilim kontrolu yap
    if best_field == "diğer":
        sw_hits = _count_keyword_hits(text, SOFTWARE_KEYWORDS)
        if sw_hits > 0:
            return "yazılım"

    return best_field


def detect_location(text):
    """
    Metin icinde lokasyon tespiti yapar.
    Hibrit/Remote ayrimi icin keyword + context bakar.
    """
    text = _normalize(text)
    
    # 1. Hibrit Ankara Kontrolu
    if re.search(r'(hybrid|hibrit|karma)\s+.*ankara|ankara\s+.*(hybrid|hibrit|karma)', text):
        return "hybrid_ankara"
        
    # 2. Ankara Kontrolu
    # Sadece "Ankara" gecmesi yetmez, "Remote" ile karisabilir.
    # Eger "Ankara" geciyor VE "Remote" gecmiyorsa -> Ankara
    # Eger hem Ankara hem Remote geciyorsa -> Genelde Remote (ama merkez ankara)
    
    has_ankara = "ankara" in text
    
    # Remote kontrolu
    is_remote = False
    for kw in LOCATION_KEYWORDS["remote"]:
        if kw in text:
            is_remote = True
            break
            
    if has_ankara and not is_remote:
        return "ankara"
        
    if is_remote:
        return "remote"
        
    if has_ankara: # Remote da olsa Ankara tercih sebebi
        return "ankara" # veya 'hybrid_ankara' varsayabiliriz? Simdilik Ankara

    # Diger sehirler / Ulkeler
    best_location = "diğer"
    # Istanbul, Izmir vs.
    for location, keywords in LOCATION_KEYWORDS.items():
        if location in ["ankara", "remote", "hybrid_ankara"]: continue
        for kw in keywords:
            if kw.lower() in text:
                return location

    return "diğer"


def detect_level(text):
    """
    Metin icinde seviye tespiti yapar.
    Unvan eslesmesi + Yil bazli tahmin ve 'Senior' vurgusu.
    """
    text = _normalize(text)

    # 1. Acik Unvan Eslesmesi (En guclu)
    # Lead -> Senior -> Mid -> Junior siralamasi onemli
    priority_order = ["lead", "senior", "mid", "junior", "entry"] 
    for level in priority_order:
        keywords = LEVEL_KEYWORDS.get(level, [])
        for kw in keywords:
            # Word boundary ile ara (junior developer, not juniorn)
            if re.search(r'\b' + re.escape(kw) + r'\b', text):
                return level

    # 2. Yil Bazli Tahmin (Regex)
    # Örnek: "5+ years", "3-5 yil", "minimum 2 years", "at least 4 years"
    year_match = re.search(r'(\d+)\s*\+?\s*(?:-|to)?\s*(\d+)?\s*(?:years?|yıl|yil)', text)
    
    if year_match:
        try:
            min_year = int(year_match.group(1))
            # Basit mantik
            if min_year >= 5:
                # 5 yil ise Senior ihtimali yuksek ama Mid de olabilir.
                return "senior" 
            elif min_year >= 2:
                return "mid"
            elif min_year == 0 or min_year == 1:
                return "junior"
        except:
            pass
            
    # 3. Dolayli Ifadeler
    if "experienced" in text or "tecrübeli" in text:
        return "mid"
    
    return "bilinmiyor"


def calculate_score(field, location, level):
    """
    Agirlikli toplam skor hesaplar.
    """
    # config.py'deki static skorlar
    field_score = FIELD_SCORES.get(field, 0)
    
    # Eger sozlukte yoksa (TF-IDF ile yeni gelenler: frontend, backend vb.)
    if field_score == 0:
        if field in ["frontend", "backend", "full stack"]:
             # Genel yazilim puanina esit veya biraz daha iyi
             field_score = 3 
        else:
             field_score = 1 # Diger
            
    location_score = LOCATION_SCORES.get(location, 0)
    level_score = LEVEL_SCORES.get(level, 0)

    total = (
        field_score * FIELD_WEIGHT
        + location_score * LOCATION_WEIGHT
        + level_score * LEVEL_WEIGHT
    )

    return round(total, 2)


def score_job(job):
    """
    Tam is ilani analizi yapar (v0.5).
    """
    # Tum metin kaynaklarini birlestir
    full_text = " ".join(filter(None, [
        job.get("title", ""),
        job.get("summary", ""),
        job.get("description", ""),  # Eger varsa full description
        job.get("location", ""),
        job.get("company", ""),
    ]))

    restricted = is_restricted(full_text)

    field = detect_field(full_text)
    location = detect_location(full_text)
    level = detect_level(full_text)

    if restricted:
        total_score = 0.0
    else:
        total_score = calculate_score(field, location, level)

    job["field"] = field
    job["location"] = location
    job["level"] = level
    job["total_score"] = total_score
    job["restricted"] = restricted

    return job
