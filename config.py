# config.py – Job Radar Konfigürasyon

# ──────────────────────────────────────────────
# Google Sheets Ayarları
# ──────────────────────────────────────────────
CREDENTIALS_FILE = "credentials.json"
SPREADSHEET_NAME = "Job Radar"
WORKSHEET_NAME = "İlanlar"

# ──────────────────────────────────────────────
# Skor Ağırlıkları
# ──────────────────────────────────────────────
FIELD_WEIGHT = 0.5
LOCATION_WEIGHT = 0.3
LEVEL_WEIGHT = 0.2

# ──────────────────────────────────────────────
# Alan Tanımları (Keyword → Alan)
# Öncelik sırası: gamedev > c# > python > mobile > java > cv > diğer
# ──────────────────────────────────────────────
FIELD_KEYWORDS = {
    "gamedev": [
        "unity", "unreal", "game developer", "game designer", "game programmer",
        "game artist", "game development", "gameplay", "mobile game", "video game",
        "oyun geliştirici", "oyun tasarımcı", "oyun programcı", "oyun",
        "godot", "cocos2d", "gamemaker", "game engine", "game studio",
    ],
    "c#": [
        "c#", "csharp", "c sharp", ".net", "dotnet", "asp.net", "blazor",
        "wpf", "xamarin", "maui",
    ],
    "python": [
        "python", "django", "flask", "fastapi", "pytorch", "tensorflow",
        "machine learning", "data science", "yapay zeka", "makine öğrenmesi",
    ],
    "mobile": [
        "mobile developer", "android", "ios", "flutter", "react native",
        "swift", "kotlin", "mobil geliştirici", "mobil uygulama",
    ],
    "java": [
        "java", "spring", "spring boot", "j2ee", "jakarta",
    ],
    "cv": [
        "computer vision", "opencv", "image processing", "görüntü işleme",
        "deep learning", "derin öğrenme",
    ],
}

# Alan Puanları
FIELD_SCORES = {
    "gamedev": 5,
    "c#": 4,
    "python": 3,
    "mobile": 3,
    "java": 2,
    "cv": 2,
    "diğer": 1,
}

# Öncelik sırası (ilk eşleşen kazanır)
FIELD_PRIORITY = ["gamedev", "c#", "python", "mobile", "java", "cv"]

# ──────────────────────────────────────────────
# Lokasyon Tanımları
# ──────────────────────────────────────────────
LOCATION_KEYWORDS = {
    "ankara": ["ankara"],
    "remote": ["remote", "uzaktan", "anywhere", "worldwide", "work from home", "wfh", "evden"],
    "hybrid_ankara": ["hybrid ankara", "hibrit ankara"],
    "türkiye": ["turkey", "türkiye", "turkiye"],
    "istanbul": ["istanbul", "İstanbul"],
}

LOCATION_SCORES = {
    "ankara": 5,
    "remote": 5,
    "hybrid_ankara": 4,
    "türkiye": 3,
    "istanbul": 1,
    "diğer": 0,
}

# ──────────────────────────────────────────────
# Level Tanımları
# ──────────────────────────────────────────────
LEVEL_KEYWORDS = {
    "junior": [
        "junior", "jr", "entry level", "entry-level", "associate",
        "yeni mezun", "stajyer", "intern", "0-2 yıl", "0-1 yıl",
        "new grad", "graduate",
    ],
    "mid": [
        "mid level", "mid-level", "middle", "intermediate",
        "2-5 yıl", "3-5 yıl", "2+ yıl", "3+ yıl",
    ],
    "senior": [
        "senior", "sr", "staff", "principal", "kıdemli",
        "5+ yıl", "7+ yıl", "10+ yıl",
    ],
    "lead": [
        "lead", "manager", "director", "head of", "vp ",
        "takım lideri", "müdür", "yönetici",
    ],
}

LEVEL_SCORES = {
    "junior": 5,
    "entry": 5,
    "mid": 3,
    "senior": -5,
    "lead": -10,
    "bilinmiyor": 0,
}
