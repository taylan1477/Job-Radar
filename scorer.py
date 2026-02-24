# scorer.py – Ilan Skorlama Modulu v0.6 (Refactored)

import re
from config import (
    FIELD_KEYWORDS, FIELD_SCORES, FIELD_PRIORITY,
    LOCATION_KEYWORDS, LOCATION_SCORES,
    LEVEL_KEYWORDS, LEVEL_SCORES,
    FIELD_WEIGHT, LOCATION_WEIGHT, LEVEL_WEIGHT,
    NEGATIVE_KEYWORDS, SOFTWARE_KEYWORDS
)
from nlp_processor import normalize_text, detect_language, FieldDetector

def is_restricted(text):
    """
    Ilanin ulke/vize kisitlamasi olup olmadigini kontrol eder.
    True donerse ilan atlanmali.
    """
    text = normalize_text(text)
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


def detect_field(text, use_tfidf=True):
    """
    Hibrit Alan Tespiti (Öncelikli + TF-IDF + Keyword):
    1. Kritik Keyword Kontrolü.
    2. TF-IDF ile dene.
    3. Keyword Hit Count ile dene.
    """
    text = normalize_text(text)

    # --- 1. Kritik Oncelikli Keywordler (Override) ---
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
    if use_tfidf:
        detector = FieldDetector()
        detected = detector.predict(text)
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
    text = normalize_text(text)
    
    # 1. Hibrit Ankara (En net)
    if re.search(r'(hybrid|hibrit|karma)\s+.*ankara|ankara\s+.*(hybrid|hibrit|karma)', text):
        return "hybrid_ankara"
        
    # 2. Ankara Varligi (Baskın)
    if "ankara" in text:
        return "ankara"

    # 3. Klasik Remote
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
    Junior/Entry level oncelikli.
    """
    text = normalize_text(text)
    
    # 1. Junior/Entry "Guclu" Sinyaller (Override)
    junior_signals = [
        r'\bjunior\b', r'\bjr\b', r'\bentry level\b', r'\bentry-level\b',
        r'yeni mezun', r'stajyer', r'intern\b', r'yetistir', r'ogrenci', r'student',
        r'no experience', r'experience not required', r'0-2 year', r'0-1 year'
    ]
    for pattern in junior_signals:
        if re.search(pattern, text):
            return "junior"

    # 2. Unvan Eslesmesi (Sirali)
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
            elif min_year < 2: 
                return "junior"
        except:
            pass
            
    return "bilinmiyor"


def calculate_score(field, location, level):
    """
    Agirlikli toplam skor hesaplar.
    """
    field_score = FIELD_SCORES.get(field, 0)
    
    # Eger sozlukte yoksa (TF-IDF ile yeni gelenler)
    if field_score == 0:
        if field in ["frontend", "backend", "full stack"]:
             field_score = 3 
        else:
             field_score = 1
            
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
    Tam is ilani analizi yapar.
    """
    full_text = " ".join(filter(None, [
        job.get("title", ""),
        job.get("summary", ""),
        job.get("description", ""),
        job.get("location", ""),
        job.get("company", ""),
    ]))

    # --- 0. Dil ve Kisitlama Kontrolu ---
    restricted = is_restricted(full_text)
    
    # Dil tespiti (Himalayas vb. icin)
    detected_lang = detect_language(full_text)
    if detected_lang and detected_lang not in ["en", "tr"]:
        try:
             # Kullanici gorsun diye sadece DEAD olanlari yazdiralim
             title_sanitized = job.get('title', '').encode('utf-8', 'ignore').decode('utf-8')
             print(f"  [DİL TESPİTİ] {detected_lang} -> DEAD: {title_sanitized}")
        except:
             pass
        restricted = True
        job["restricted_reason"] = f"Language: {detected_lang}"
        location = "dead"
    
    # --- 1. Alan, Lokasyon, Level Tespiti ---
    field = detect_field(full_text)
    location = detect_location(full_text)
    level = detect_level(full_text)
    
    # --- 2. Skorlama ---
    if restricted:
        total_score = -10.0
        # Dil yuzunden restrict edildiyse, location'i dead yap (yukaridaki detect_location ezmis olabilir)
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
