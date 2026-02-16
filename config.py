# config.py – Job Radar Konfigurasyon v0.2

# ──────────────────────────────────────────────
# Google Sheets Ayarlari
# ──────────────────────────────────────────────
CREDENTIALS_FILE = "credentials.json"
SPREADSHEET_ID = "1Lx5tsZCd4egPwQ1-GzuD5w1w0ykc7yZL_93FHYdfOVU"
SPREADSHEET_NAME = "Job Radar"
WORKSHEET_NAME = "İlanlar"

# ──────────────────────────────────────────────
# JSearch API (RapidAPI) – Opsiyonel
# Ucretsiz kayit: https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch
# ──────────────────────────────────────────────
JSEARCH_API_KEY = "4db166c327mshd0a363cfdf01f48p191bbejsn9019fc4a59c0"
JSEARCH_QUERIES = [
    # Remote gamedev (verimli – 10+ sonuc)
    {"query": "game developer", "remote_only": True},
    {"query": "unity developer", "remote_only": True},
    {"query": "unreal developer", "remote_only": True},
    {"query": "game programmer", "remote_only": True},
    # Remote yazilim (genel)
    {"query": "C# developer", "remote_only": True},
]

# ──────────────────────────────────────────────
# Kariyer.net Scraping Ayarlari
# ──────────────────────────────────────────────
KARIYER_SEARCHES = [
    {"keyword": "game developer", "city": "ankara"},
    {"keyword": "unity", "city": "ankara"},
    {"keyword": "oyun geliştirici", "city": "ankara"},
    {"keyword": "yazılım mühendisi", "city": "ankara"},
    {"keyword": "software engineer", "city": "ankara"},
    {"keyword": "c# developer", "city": "ankara"},
    {"keyword": "python developer", "city": "ankara"},
    {"keyword": "backend developer", "city": "ankara"},
    {"keyword": "mobil uygulama geliştirici", "city": "ankara"},
    {"keyword": "game developer", "city": ""},  # Tum Turkiye
    {"keyword": "unity developer", "city": ""},  # Tum Turkiye
]

# ──────────────────────────────────────────────
# LinkedIn Jobs Arama Ayarlari (Playwright scraping)
# ──────────────────────────────────────────────
LINKEDIN_SEARCHES = [
    {"keyword": "game developer", "location": "Turkey"},
    {"keyword": "unity developer", "location": "Turkey"},
    {"keyword": "software engineer", "location": "Ankara, Turkey"},
    {"keyword": "C# developer", "location": "Turkey"},
    {"keyword": "python developer", "location": "Ankara, Turkey"},
]

# ──────────────────────────────────────────────
# Skor Agirliklari
# ──────────────────────────────────────────────
FIELD_WEIGHT = 0.5
LOCATION_WEIGHT = 0.3
LEVEL_WEIGHT = 0.2

# ──────────────────────────────────────────────
# Negatif Keyword'ler – Bu keyword'leri iceren ilanlar atlanir
# ──────────────────────────────────────────────
NEGATIVE_KEYWORDS = [
    "us only", "usa only", "us citizens only", "us citizen",
    "united states only", "u.s. only", "u.s. citizens",
    "must be located in the us", "must reside in the us",
    "us-based only", "based in the united states",
    "uk only", "eu only", "eu citizens only",
    "must be authorized to work in the us",
    "work authorization required", "visa sponsorship not available",
    "security clearance required", "dod clearance", "ts/sci",
    "us work authorization", "us employment eligibility",
    "legally authorized to work in the united states",
]

# ──────────────────────────────────────────────
# Relevance Keyword'leri – Kariyer.net ilaninin en az birini icermesi lazim
# Yazilim / muhendislik ile alakali oldugunu dogrular
# ──────────────────────────────────────────────
RELEVANCE_KEYWORDS = [
    # Yazilim spesifik unvanlar (muhendis/engineer tek basina genis)
    "yazılım", "software", "developer", "geliştirici",
    "yazılım mühendisi", "bilgisayar mühendisi",
    "software engineer", "web developer",
    "programcı", "programmer", "kodlama", "coding",
    # Spesifik teknolojiler
    "unity", "unreal", "game dev", "oyun geliştir",
    "python", "java", "c#", "c++",
    ".net", "dotnet", "react", "angular", "vue", "node", "javascript",
    "typescript", "flutter", "swift", "kotlin", "android", "ios",
    "mobile developer", "mobil geliştirici",
    "frontend", "backend", "full stack", "fullstack",
    "devops", "cloud", "aws", "azure", "docker", "kubernetes",
    "database", "sql", "veri tabanı",
    # Bilisim/IT
    "bilişim", "bilgi teknoloji", "bilgisayar", "computer science",
    "siber güvenlik", "cyber security", "network engineer",
    # Data / AI
    "data scientist", "data engineer", "veri bilimi",
    "yapay zeka", "machine learning", "deep learning",
    # Test / QA (yazilim)
    "test engineer", "test mühendisi", "qa engineer",
    "quality assurance", "test automation",
    # Tasarim (teknik)
    "ui/ux", "ux designer", "web tasarım",
]

# ──────────────────────────────────────────────
# Alan Tanimlari (Keyword -> Alan)
# Oncelik sirasi: gamedev > c# > python > mobile > java > cv > diger
# ──────────────────────────────────────────────
FIELD_KEYWORDS = {
    "gamedev": [
        "unity developer", "unity engineer", "unity programmer",
        "unreal developer", "unreal engineer", "unreal programmer",
        "game developer", "game designer", "game programmer",
        "game artist", "game development", "gameplay programmer",
        "gameplay engineer", "mobile game", "video game",
        "oyun geliştirici", "oyun tasarımcı", "oyun programcı",
        "godot", "cocos2d", "gamemaker", "game engine", "game studio",
        "game dev", "game design", "game programming", "game producer",
        "game tester", "game qa",
    ],
    "c#": [
        "c# developer", "c# engineer", "csharp", "c sharp",
        ".net developer", ".net engineer", "dotnet", "asp.net",
        "blazor", "wpf", "xamarin", "maui",
    ],
    "python": [
        "python developer", "python engineer",
        "django", "flask", "fastapi",
        "pytorch", "tensorflow",
        "machine learning engineer", "data scientist",
        "yapay zeka", "makine öğrenmesi",
        "ml engineer", "ai engineer",
    ],
    "mobile": [
        "mobile developer", "mobile engineer",
        "android developer", "android engineer",
        "ios developer", "ios engineer",
        "flutter developer", "react native developer",
        "swift developer", "kotlin developer",
        "mobil geliştirici", "mobil uygulama",
    ],
    "java": [
        "java developer", "java engineer",
        "spring boot", "spring developer",
        "j2ee", "jakarta",
    ],
    "cv": [
        "computer vision", "opencv",
        "image processing", "görüntü işleme",
        "deep learning engineer", "derin öğrenme",
    ],
}

# Alan Puanlari
FIELD_SCORES = {
    "gamedev": 5,
    "c#": 4,
    "python": 3,
    "mobile": 3,
    "java": 2,
    "cv": 2,
    "yazılım": 2,
    "diğer": 1,
}

# Oncelik sirasi (ilk eslesen kazanir)
FIELD_PRIORITY = ["gamedev", "c#", "python", "mobile", "java", "cv"]

# ──────────────────────────────────────────────
# Ek Alan Keyword'leri – Genel yazilim tespiti (diger'den biraz iyi)
# ──────────────────────────────────────────────
SOFTWARE_KEYWORDS = [
    "software engineer", "software developer", "yazılım mühendisi",
    "yazılım geliştirici", "full stack", "fullstack", "frontend developer",
    "backend developer", "web developer", "devops", "site reliability",
    "bilgisayar mühendisi", "computer engineer",
]

# ──────────────────────────────────────────────
# Lokasyon Tanimlari
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
# Level Tanimlari
# ──────────────────────────────────────────────
LEVEL_KEYWORDS = {
    "junior": [
        "junior", "entry level", "entry-level",
        "yeni mezun", "stajyer", "intern", "0-2 yıl", "0-1 yıl",
        "new grad", "graduate", "fresh graduate",
    ],
    "mid": [
        "mid level", "mid-level", "middle", "intermediate",
        "2-5 yıl", "3-5 yıl", "2+ yıl", "3+ yıl",
    ],
    "senior": [
        "senior", "staff", "principal", "kıdemli",
        "5+ yıl", "7+ yıl", "10+ yıl",
    ],
    "lead": [
        "lead developer", "lead engineer", "tech lead",
        "engineering manager", "director of engineering",
        "head of engineering", "vp engineering",
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
