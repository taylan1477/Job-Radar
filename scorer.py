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
    Hibrit Alan Tespiti (Öncelikli + TF-IDF + Keyword):
    1. [YENİ] Kritik Keyword Kontrolü (GameDev vb. için kesin eşleşme).
    2. TF-IDF ile dene.
    3. Keyword Hit Count ile dene.
    """
    text = _normalize(text)

    # --- 1. Kritik Oncelikli Keywordler (Override) ---
    # GameDev kaciyorsa, burasi yakalar.
    if re.search(r'\b(game dev|game design|game program|unity|unreal|godot|oyun gelis|oyun tasarim)\w*', text):
        return "gamedev"
    
    # Diger kesinlesmis alanlar
    if "flutter" in text or "react native" in text or "ios developer" in text or "android developer" in text:
        return "mobile"
    if "frontend" in text or "front-end" in text:
        return "frontend"
    if "backend" in text or "back-end" in text:
        return "backend"

    # --- 2. Yontem: TF-IDF ---
    if use_tfidf and SKLEARN_AVAILABLE:
        detected = detect_field_tfidf(text)
        if detected:
            return detected

    # --- 3. Yontem: Keyword Hit Count (Yedek) ---
    best_field = "diğer"
    best_hits = 0
    best_priority = len(FIELD_PRIORITY) + 1

    for i, field in enumerate(FIELD_PRIORITY):
        keywords = FIELD_KEYWORDS.get(field, [])
        hits = _count_keyword_hits(text, keywords)
        
        if hits > best_hits or (hits == best_hits and hits > 0 and i < best_priority):
            best_hits = hits
            best_field = field
            best_priority = i

    if best_field == "diğer":
        sw_hits = _count_keyword_hits(text, SOFTWARE_KEYWORDS)
        if sw_hits > 0:
            return "yazılım"

    return best_field


def detect_location(text):
    """
    Metin icinde lokasyon tespiti yapar.
    Ankara oncelikli.
    """
    text = _normalize(text)
    
    # 1. Hibrit Ankara (En net)
    if re.search(r'(hybrid|hibrit|karma)\s+.*ankara|ankara\s+.*(hybrid|hibrit|karma)', text):
        return "hybrid_ankara"
        
    # 2. Ankara Varligi (Baskın)
    # Eger metinde Ankara geciyorsa, Remote bile olsa "Ankara" olarak isaretle.
    # Cunku kullanici Ankara istiyor. Remote olmasi eksi degil arti.
    # Ayrica "Remote in Ankara" gibi ifadeler de Ankara puani almali (5 puan).
    # "Remote" (5 puan) ile "Ankara" (5 puan) arasinda fark yok skorda ama
    # kategorik olarak Ankara demek daha dogru (cunku ofis orada).
    if "ankara" in text:
        return "ankara"

    # 3. Klasik Remote
    is_remote = False
    for kw in LOCATION_KEYWORDS["remote"]:
        if kw in text:
            return "remote"

    # 4. Diger sehirler
    for location, keywords in LOCATION_KEYWORDS.items():
        if location in ["ankara", "remote", "hybrid_ankara"]: continue
        for kw in keywords:
            if kw.lower() in text:
                return location

    return "diğer"


def detect_level(text):
    """
    Metin icinde seviye tespiti yapar.
    Junior/Entry level oncelikli (Junior, Yeni Mezun, Stajyer, <2 yil).
    """
    text = _normalize(text)
    
    # 1. Junior/Entry "Guclu" Sinyaller (Override)
    # Eger bunlardan biri varsa direk Junior/Entry don.
    # Senior kelimesi gecse bile "Junior to Senior" olabilir, ama genelde baslikta "Junior" varsa Junior'dur.
    junior_signals = [
        r'\bjunior\b', r'\bjr\b', r'\bentry level\b', r'\bentry-level\b',
        r'yeni mezun', r'stajyer', r'intern\b', r'yetistir', r'ogrenci', r'student',
        r'no experience', r'experience not required', r'0-2 year', r'0-1 year'
    ]
    for pattern in junior_signals:
        if re.search(pattern, text):
            return "junior" # veya "entry" (Score: 5)

    # 2. Unvan Eslesmesi (Sirali)
    # Lead -> Senior -> Mid -> Junior (Junior yukarida bulunduysa zaten dondu)
    priority_order = ["lead", "senior", "mid", "junior", "entry"] 
    for level in priority_order:
        keywords = LEVEL_KEYWORDS.get(level, [])
        for kw in keywords:
            if re.search(r'\b' + re.escape(kw) + r'\b', text):
                return level

    # 3. Yil Bazli Tahmin (Regex)
    year_match = re.search(r'(\d+)\s*\+?\s*(?:-|to)?\s*(\d+)?\s*(?:years?|yıl|yil)', text)
    if year_match:
        try:
            min_year = int(year_match.group(1))
            if min_year >= 5:
                return "senior" 
            elif min_year >= 2:
                return "mid"
            elif min_year < 2: # 0, 1
                return "junior"
        except:
            pass
            
    # 4. Keyword Destekli Tahmin
    if "senior" not in text and "mid" not in text and "lead" not in text:
        # Eger hicbir level gecmiyor ama "Developer" geciyorsa
        # ve deneyim yili da yoksa...
        # "Junior" varsaymak riskli mi? Evet. Ama "Bilinmiyor" (0 puan) yerine
        # eger "experience" kelimesi hic gecmiyorsa belki Entry olabilir?
        # Simdilik bilinmiyor kalsin ama "learning", "enthusiastic" vb varsa Junior yapalim.
        if "learning" in text or "willing to learn" in text or "passion" in text:
             pass # Simdilik pas gecelim, cok aggressive olmasin.

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

    # --- 0. Dil Kontrolu ve Kisitlamalar ---
    # Once keyword blacklist check
    restricted = is_restricted(full_text)
    
    # Himalayas veya diger siteler icin Dil Kontrolu (YENI)
    try:
        from langdetect import detect
        # Kisa metinlerde hata verebilir, birlestirilmis metni kullan
        if len(full_text) > 20: 
            lang = detect(full_text)
            # print(f"  [DEBUG] Lang: {lang} | Len: {len(full_text)}")
            
            if lang not in ["en", "tr"]:
                try:
                    # Kullanici gorsun diye sadece DEAD olanlari yazdiralim
                    print(f"  [DİL TESPİTİ] {lang} -> DEAD: {job.get('title', '').encode('utf-8', 'ignore').decode('utf-8')}")
                except:
                    pass
                    
                restricted = True
                job["restricted_reason"] = f"Language: {lang}"
                location = "dead"
    
    except ImportError:
        pass 
    except Exception as e:
        pass

    # --- 1. Alan, Lokasyon, Level Tespiti ---
    # Bu degerler her durumda lazim (raporda gostermek icin)
    field = detect_field(full_text)
    location = detect_location(full_text)
    level = detect_level(full_text)
    
    # --- 2. Dil Kontrolu Sonrasi Skorlama ---
    # print(f"  [DEBUG] Check restricted before final block: {restricted}")
    if restricted:
        total_score = -10.0 # Dil uyusmazligi veya restricted keyword varsa negatif bas
        # Dil yuzunden restrict edildiyse, location'i dead yap (yukarida detect_location ezmis olabilir)
        if job.get("restricted_reason", "").startswith("Language:"):
             location = "dead"
    else:
        total_score = calculate_score(field, location, level)

    job["field"] = field
    job["location"] = location
    job["level"] = level
    job["total_score"] = total_score
    job["restricted"] = restricted

    return job
