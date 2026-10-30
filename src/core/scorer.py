# scorer.py – Ilan Skorlama Modulu v0.7 (Genisletilmis 7 Alan Modeli)

import re
from src.utils.config import (
    FIELD_KEYWORDS, FIELD_SCORES, FIELD_PRIORITY,
    LOCATION_KEYWORDS, LOCATION_SCORES,
    LEVEL_KEYWORDS, LEVEL_SCORES,
    FIELD_WEIGHT, LOCATION_WEIGHT, LEVEL_WEIGHT,
    NEGATIVE_KEYWORDS, SOFTWARE_KEYWORDS
)
from src.core.nlp_processor import normalize_text, detect_language, FieldDetector

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
    """Metinde kac keyword eslestirdigini sayar."""
    count = 0
    for kw in keywords:
        kw_lower = kw.lower()
        if " " in kw_lower:
            if kw_lower in text:
                count += 1
        elif len(kw_lower) >= 4:
            if kw_lower in text:
                count += 1
        else:
            if re.search(r'\b' + re.escape(kw_lower) + r'\b', text):
                count += 1
    return count


def detect_field(text, use_tfidf=True):
    """
    Genisletilmis 7 Alan Tespiti (Oncelikli + TF-IDF + Keyword):
    1. Kritik Oncelikli Rol Kontrolu.
    2. TF-IDF ile tahmin.
    3. Keyword Hit Count ile dene.
    """
    text = normalize_text(text)

    # --- 1. Kritik Oncelikli Roller (Override) ---
    # 1. GameDev (1 numara tercih)
    if re.search(r'\b(game dev|game design|game program|unity|unreal|godot|oyun gelis|oyun tasarim|gameplay)\w*', text):
        return "gamedev"

    # 2. Savunma & Simulasyon
    if re.search(r'\b(simülasyon|simulation|askeri simülasyon|taktik simülasyon|c4isr|harp oyunu|sistem entegrasyon|ara katman|middleware dev|rti dds|dis/hla)\w*', text):
        return "savunma_simülasyon"

    # 3. Sistem & Network
    if re.search(r'\b(sistem yöneticisi|sysadmin|system administrator|noc mühendisi|noc engineer|network operations center|ağ otomasyonu)\w*', text):
        return "sistem_network"

    # 4. Veri & BI
    if re.search(r'\b(veritabanı yöneticisi|database administrator|iş zekası|bi developer|etl developer|web scraping mühendisi|veri madenciliği)\w*', text):
        return "veri_bi"

    # 5. Endustriyel & Surec Otomasyonu
    if re.search(r'\b(erp uzmanı|erp geliştiricisi|sap danışmanı|dynamics 365|endüstriyel otomasyon|scada|süreç otomasyonu|process automation|rpa developer|wms geliştiricisi|depo yönetim)\w*', text):
        return "endüstriyel_otomasyon"

    # 6. Yazilim (Frontend/Backend/Mobil/SDET)
    if any(k in text for k in ["backend", "frontend", "fullstack", "full stack", "flutter", "react native", "android developer", "ios developer", "software engineer", "yazılım mühendisi"]):
        return "yazılım"

    # --- 2. Yontem: TF-IDF ---
    if use_tfidf:
        try:
            detector = FieldDetector()
            detected = detector.predict(text)
            if detected and detected in FIELD_SCORES:
                return detected
        except Exception:
            pass

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
        if location in ["ankara", "remote", "hybrid_ankara"]:
            continue
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
        except Exception:
            pass
            
    return "bilinmiyor"


def calculate_score(field, location, level, source=""):
    """
    Agirlikli toplam skor hesaplar. LinkedIn ilanlarina +1 ekler.
    """
    field_score = FIELD_SCORES.get(field, 1)
    location_score = LOCATION_SCORES.get(location, 0)
    level_score = LEVEL_SCORES.get(level, 0)

    total = (
        field_score * FIELD_WEIGHT
        + location_score * LOCATION_WEIGHT
        + level_score * LEVEL_WEIGHT
    )
    
    if source and "linkedin" in str(source).lower():
        total += 1.0

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
        restricted = True
        job["restricted_reason"] = f"Language: {detected_lang}"
        location = "dead"
    else:
        location = detect_location(full_text)
    
    # --- 1. Alan, Lokasyon, Level Tespiti ---
    field = detect_field(full_text)
    level = detect_level(full_text)
    
    # --- 2. Skorlama ---
    if restricted:
        total_score = -10.0
        if job.get("restricted_reason", "").startswith("Language:"):
            location = "dead"
    else:
        total_score = calculate_score(field, location, level, source=job.get("source", ""))

    job["field"] = field
    job["location"] = location
    job["level"] = level
    job["total_score"] = total_score
    job["restricted"] = restricted

    return job
