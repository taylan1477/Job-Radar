# scorer.py – Ilan Skorlama Modulu v0.2

import re
from config import (
    FIELD_KEYWORDS, FIELD_SCORES, FIELD_PRIORITY,
    LOCATION_KEYWORDS, LOCATION_SCORES,
    LEVEL_KEYWORDS, LEVEL_SCORES,
    FIELD_WEIGHT, LOCATION_WEIGHT, LEVEL_WEIGHT,
    NEGATIVE_KEYWORDS, SOFTWARE_KEYWORDS,
)


def _normalize(text):
    """Metni lowercase ve temizlenmis hale getirir."""
    if not text:
        return ""
    text = text.lower()
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
    """Metinde kac keyword eslestirdigini sayar."""
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
            # Kisa kelime: word boundary
            if kw_lower == "c#":
                if re.search(r'\bc#', text):
                    count += 1
            else:
                if re.search(r'\b' + re.escape(kw_lower) + r'\b', text):
                    count += 1
    return count


def detect_field(text):
    """
    Hit-count bazli alan tespiti.
    Her alan icin keyword hit sayisi hesaplanir, en cok hit alan kazanir.
    Esitlikte oncelik sirasi gecerlidir.
    """
    text = _normalize(text)

    best_field = "diğer"
    best_hits = 0
    best_priority = len(FIELD_PRIORITY) + 1

    for i, field in enumerate(FIELD_PRIORITY):
        keywords = FIELD_KEYWORDS[field]
        hits = _count_keyword_hits(text, keywords)
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
    En yuksek puanli lokasyon doner.
    """
    text = _normalize(text)
    best_location = "diğer"
    best_score = -1

    for location, keywords in LOCATION_KEYWORDS.items():
        for kw in keywords:
            kw_lower = kw.lower()
            if kw_lower in text:
                score = LOCATION_SCORES.get(location, 0)
                if score > best_score:
                    best_score = score
                    best_location = location
                break

    return best_location


def detect_level(text):
    """
    Metin icinde seviye tespiti yapar.
    Oncelik sirasi: junior -> mid -> senior -> lead
    """
    text = _normalize(text)

    priority_order = ["junior", "mid", "senior", "lead"]

    for level in priority_order:
        keywords = LEVEL_KEYWORDS[level]
        for kw in keywords:
            kw_lower = kw.lower()
            if " " in kw_lower:
                if kw_lower in text:
                    return level
            elif len(kw_lower) >= 4:
                if kw_lower in text:
                    return level
            else:
                if re.search(r'\b' + re.escape(kw_lower) + r'\b', text):
                    return level

    return "bilinmiyor"


def calculate_score(field, location, level):
    """
    Agirlikli toplam skor hesaplar.
    Formul: (Alan*0.5 + Lokasyon*0.3 + Level*0.2)
    """
    field_score = FIELD_SCORES.get(field, 1)
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
    Job dict'e skor bilgilerini ekler ve dondurur.
    Kisitli ilanlar icin 'restricted' = True set edilir.
    """
    full_text = f"{job.get('title', '')} {job.get('summary', '')}"

    # Ulke/vize kisitlamasi kontrol
    restricted = is_restricted(full_text)

    field = detect_field(full_text)
    location = detect_location(full_text)
    level = detect_level(full_text)

    field_score = FIELD_SCORES.get(field, 1)
    location_score = LOCATION_SCORES.get(location, 0)
    level_score = LEVEL_SCORES.get(level, 0)

    if restricted:
        total_score = 0.0
    else:
        total_score = calculate_score(field, location, level)

    job["field"] = field
    job["location"] = location
    job["level"] = level
    job["field_score"] = field_score
    job["location_score"] = location_score
    job["level_score"] = level_score
    job["total_score"] = total_score
    job["restricted"] = restricted

    return job
