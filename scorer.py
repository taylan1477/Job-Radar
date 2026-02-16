# scorer.py – İlan Skorlama Modülü

import re
from config import (
    FIELD_KEYWORDS, FIELD_SCORES, FIELD_PRIORITY,
    LOCATION_KEYWORDS, LOCATION_SCORES,
    LEVEL_KEYWORDS, LEVEL_SCORES,
    FIELD_WEIGHT, LOCATION_WEIGHT, LEVEL_WEIGHT,
)


def _normalize(text):
    """Metni lowercase ve temizlenmiş hale getirir."""
    if not text:
        return ""
    text = text.lower()
    # HTML tag'lerini temizle
    text = re.sub(r"<[^>]+>", " ", text)
    # Fazla boşlukları temizle
    text = re.sub(r"\s+", " ", text).strip()
    return text


def detect_field(text):
    """
    Metin içinde alan tespiti yapar.
    Öncelik sırasına göre ilk eşleşen alan döner.
    """
    text = _normalize(text)

    for field in FIELD_PRIORITY:
        keywords = FIELD_KEYWORDS[field]
        for kw in keywords:
            if kw.lower() in text:
                return field

    return "diğer"


def detect_location(text):
    """
    Metin içinde lokasyon tespiti yapar.
    En yüksek puanlı lokasyon döner.
    """
    text = _normalize(text)
    best_location = "diğer"
    best_score = -1

    for location, keywords in LOCATION_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in text:
                score = LOCATION_SCORES.get(location, 0)
                if score > best_score:
                    best_score = score
                    best_location = location
                break

    return best_location


def detect_level(text):
    """
    Metin içinde seviye tespiti yapar.
    İlk eşleşen seviye döner (junior öncelikli).
    """
    text = _normalize(text)

    # Öncelik sırası: junior → mid → senior → lead
    priority_order = ["junior", "mid", "senior", "lead"]

    for level in priority_order:
        keywords = LEVEL_KEYWORDS[level]
        for kw in keywords:
            if kw.lower() in text:
                return level

    return "bilinmiyor"


def calculate_score(field, location, level):
    """
    Ağırlıklı toplam skor hesaplar.
    Formül: (Alan*0.5 + Lokasyon*0.3 + Level*0.2)
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
    Tam iş ilanı analizi yapar.
    Job dict'e skor bilgilerini ekler ve döndürür.
    """
    # Başlık + açıklama birleştir
    full_text = f"{job.get('title', '')} {job.get('summary', '')}"

    field = detect_field(full_text)
    location = detect_location(full_text)
    level = detect_level(full_text)

    field_score = FIELD_SCORES.get(field, 1)
    location_score = LOCATION_SCORES.get(location, 0)
    level_score = LEVEL_SCORES.get(level, 0)
    total_score = calculate_score(field, location, level)

    job["field"] = field
    job["location"] = location
    job["level"] = level
    job["field_score"] = field_score
    job["location_score"] = location_score
    job["level_score"] = level_score
    job["total_score"] = total_score

    return job
