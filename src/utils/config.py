# config.py – Job Radar Konfigurasyon v0.5 (rules.yaml Loader & Fallback)

import os
from pathlib import Path
import yaml

# ──────────────────────────────────────────────
# Google Sheets Ayarlari
# ──────────────────────────────────────────────
CREDENTIALS_FILE = "credentials.json"
SPREADSHEET_ID = "1Lx5tsZCd4egPwQ1-GzuD5w1w0ykc7yZL_93FHYdfOVU"
SPREADSHEET_NAME = "Job Radar"
WORKSHEET_NAME = "İlanlar"

# ──────────────────────────────────────────────
# JSearch API Key
# ──────────────────────────────────────────────
JSEARCH_API_KEY = "4db166c327mshd0a363cfdf01f48p191bbejsn9019fc4a59c0"

# ──────────────────────────────────────────────
# rules.yaml Dosyasini Yukle
# ──────────────────────────────────────────────
RULES_PATH = Path("rules.yaml")

def load_rules(file_path: Path = RULES_PATH) -> dict:
    """rules.yaml dosyasini guvenli sekilde okur."""
    if file_path.exists():
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                if isinstance(data, dict):
                    return data
        except Exception as e:
            print(f"[UYARI] rules.yaml okunamadi: {e}. Varsayilanlar kullaniliyor.")
    return {}

_rules = load_rules()

# ──────────────────────────────────────────────
# Skor Agirliklari
# ──────────────────────────────────────────────
_weights = _rules.get("weights", {})
FIELD_WEIGHT = float(_weights.get("field", 0.3))
LOCATION_WEIGHT = float(_weights.get("location", 0.4))
LEVEL_WEIGHT = float(_weights.get("level", 0.3))

# ──────────────────────────────────────────────
# Alan Puanlari ve Oncelik Siralamasi
# ──────────────────────────────────────────────
FIELD_SCORES = _rules.get("field_scores", {
    "gamedev": 5,
    "savunma_simülasyon": 4,
    "yazılım": 4,
    "sistem_network": 3,
    "veri_bi": 3,
    "endüstriyel_otomasyon": 3,
    "diğer": 1,
})

FIELD_PRIORITY = _rules.get("field_priority", [
    "gamedev",
    "savunma_simülasyon",
    "yazılım",
    "sistem_network",
    "veri_bi",
    "endüstriyel_otomasyon",
    "diğer"
])

# ──────────────────────────────────────────────
# Lokasyon Puanlari
# ──────────────────────────────────────────────
LOCATION_SCORES = _rules.get("location_scores", {
    "ankara": 5,
    "remote": 5,
    "hybrid_ankara": 5,
    "türkiye": 3,
    "istanbul": 3,
    "izmir": 2,
    "bursa": 2,
    "avrupa": 1,
    "abd": 0,
    "diğer": 0,
    "dead": -10,
})

# ──────────────────────────────────────────────
# Seviye Puanlari
# ──────────────────────────────────────────────
LEVEL_SCORES = _rules.get("level_scores", {
    "junior": 5,
    "entry": 5,
    "mid": 2,
    "bilinmiyor": 0,
    "senior": -10,
    "lead": -15,
})

# ──────────────────────────────────────────────
# Anahtar Kelimeler (Field, Location, Level, Negative, Relevance)
# ──────────────────────────────────────────────
FIELD_KEYWORDS = _rules.get("field_keywords", {})
LOCATION_KEYWORDS = _rules.get("location_keywords", {})
LEVEL_KEYWORDS = _rules.get("level_keywords", {})
NEGATIVE_KEYWORDS = _rules.get("negative_keywords", [])

# Kariyer.net ve harici filtreler icin relevance listesi
RELEVANCE_KEYWORDS = _rules.get("relevance_keywords", [
    "yazılım", "software", "developer", "geliştirici", "mühendis", "engineer",
    "programcı", "programmer", "kodlama", "coding", "web developer",
    "unity", "unreal", "game dev", "oyun geliştir", "gameplay", "game designer",
    "simülasyon", "simulation", "sistem entegrasyon", "system integration",
    "ara katman", "middleware", "sistem yöneticisi", "system administrator", "sysadmin",
    "noc", "network", "ağ mühendisi", "it operasyon", "sre", "devops", "cloud",
    "veritabanı", "database", "dba", "sql", "iş zekası", "business intelligence",
    "bi developer", "etl", "veri madenciliği", "data mining", "scraping",
    "data engineer", "veri mühendisi", "data analyst", "erp", "sap", "otomasyon",
    "automation", "scada", "plc", "rpa", "wms", "ürün mühendisi", "streaming",
    "uygulama destek", "application support", "sdet", "test engineer", "qa engineer"
])

# Genel teknik tespit icin yedek liste
SOFTWARE_KEYWORDS = [
    "developer", "engineer", "programmer", "geliştirici", "mühendis",
    "programcı", "coding", "development", "yazılım", "software",
    "bilişim", "it", "teknik", "analist", "uzman"
]

# ──────────────────────────────────────────────
# Platform Bazli Arama Sorgulari
# ──────────────────────────────────────────────
_searches = _rules.get("searches", {})
LINKEDIN_SEARCHES = _searches.get("linkedin", [])
JSEARCH_QUERIES = _searches.get("jsearch", [])
KARIYER_SEARCHES = _searches.get("kariyer", [])
