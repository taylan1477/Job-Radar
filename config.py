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
FIELD_WEIGHT = 0.3
LOCATION_WEIGHT = 0.4
LEVEL_WEIGHT = 0.3

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
        # Engine / Framework
        "unity developer", "unity engineer", "unity programmer", "unity 3d",
        "unreal developer", "unreal engineer", "unreal programmer", "unreal engine",
        "godot", "cocos2d", "gamemaker", "game engine", "defold", "phaser",
        # Roller
        "game developer", "game designer", "game programmer", "game artist",
        "game producer", "game tester", "game qa", "gameplay programmer",
        "gameplay engineer", "gameplay designer", "level designer",
        "technical artist", "technical designer", "narrative designer",
        "game economy designer", "monetization designer",
        # Alanlar
        "game development", "game design", "game programming", "game studio",
        "mobile game", "video game", "pc game", "console game",
        "hyper casual", "hypercasual", "casual game", "midcore",
        "playable ad", "playable ads", "playables",
        "game dev", "indie game", "aaa game",
        # Turkce
        "oyun geliştirici", "oyun tasarımcı", "oyun programcı",
        "oyun stüdyosu", "oyun motoru",
        # Diller (gamedev baglami)
        "c++ game", "c++ developer", "c++ engineer", "c++ programmer",
        "kotlin game", "lua", "glsl", "hlsl", "shader",
        # 3D / Grafik
        "3d artist", "3d modeler", "3d animator", "vfx artist",
        "2d artist", "pixel art", "concept artist",
    ],
    "c#": [
        "c# developer", "c# engineer", "c# programmer", "csharp", "c sharp",
        ".net developer", ".net engineer", ".net core", "dotnet", "asp.net",
        "blazor", "wpf", "xamarin", "maui", "winforms",
        "entity framework", "linq",
    ],
    "python": [
        "python developer", "python engineer", "python programmer",
        "django", "flask", "fastapi", "celery", "sqlalchemy",
        "pytorch", "tensorflow", "keras", "scikit-learn", "pandas",
        "machine learning engineer", "data scientist", "data engineer",
        "yapay zeka", "makine öğrenmesi", "veri bilimci",
        "ml engineer", "ai engineer", "nlp engineer",
        "computer vision engineer", "deep learning",
    ],
    "c++": [
        "c++ developer", "c++ engineer", "c++ programmer",
        "cpp developer", "cpp engineer",
        "embedded developer", "embedded engineer", "embedded software",
        "systems programmer", "low level", "real-time",
        "qt developer", "boost", "cmake",
    ],
    "mobile": [
        "mobile developer", "mobile engineer",
        "android developer", "android engineer",
        "ios developer", "ios engineer",
        "flutter developer", "flutter engineer",
        "react native developer", "react native engineer",
        "swift developer", "swift engineer",
        "kotlin developer", "kotlin engineer", "kotlin mobile",
        "mobil geliştirici", "mobil uygulama", "mobil mühendis",
    ],
    "java": [
        "java developer", "java engineer", "java programmer",
        "spring boot", "spring developer", "spring engineer",
        "j2ee", "jakarta", "hibernate",
        "kotlin backend", "kotlin developer", "kotlin engineer",
        "microservices java", "java backend",
    ],
    "cv": [
        "computer vision", "opencv", "yolo",
        "image processing", "görüntü işleme",
        "deep learning engineer", "derin öğrenme",
        "point cloud", "lidar", "slam",
    ],
}

# Alan Puanlari
FIELD_SCORES = {
    "gamedev": 5,
    "c#": 4,
    "c++": 4,
    "python": 4,
    "mobile": 3,
    "java": 3,
    "cv": 2,
    "yazılım": 2,
    "diğer": 1,
}

# Oncelik sirasi (ilk eslesen kazanir)
FIELD_PRIORITY = ["gamedev", "c#", "c++", "python", "mobile", "java", "cv"]

# ──────────────────────────────────────────────
# Ek Alan Keyword'leri – Genel yazilim tespiti (diger'den biraz iyi)
# ──────────────────────────────────────────────
SOFTWARE_KEYWORDS = [
    # Genel yazilim rolleri
    "software engineer", "software developer", "software architect",
    "yazılım mühendisi", "yazılım geliştirici", "yazılım uzmanı",
    "bilgisayar mühendisi", "computer engineer", "computer scientist",
    # Web
    "full stack", "fullstack", "full-stack",
    "frontend developer", "frontend engineer", "front-end",
    "backend developer", "backend engineer", "back-end",
    "web developer", "web engineer",
    # DevOps / Cloud / Infra
    "devops", "dev ops", "site reliability", "sre",
    "cloud engineer", "cloud architect", "infrastructure engineer",
    "platform engineer", "systems engineer",
    # Data
    "data analyst", "data engineer", "database administrator", "dba",
    "business intelligence", "bi developer", "etl developer",
    # QA / Test
    "qa engineer", "quality assurance", "test engineer", "test automation",
    "sdet", "test mühendisi",
    # Security
    "security engineer", "cybersecurity", "siber güvenlik",
    "information security", "bilgi güvenliği",
    # Genel teknik
    "developer", "engineer", "programmer", "geliştirici", "mühendis",
    "programcı", "coding", "development",
]

# ──────────────────────────────────────────────
# Lokasyon Tanimlari
# ──────────────────────────────────────────────
LOCATION_KEYWORDS = {
    "ankara": ["ankara"],
    "remote": [
        "remote", "uzaktan", "anywhere", "worldwide", "work from home",
        "wfh", "evden", "global", "distributed", "fully remote",
        "remote-first", "work remotely", "home office", "telecommute",
        "location independent", "no location", "remote position",
    ],
    "hybrid_ankara": ["hybrid ankara", "hibrit ankara"],
    "türkiye": [
        "turkey", "türkiye", "turkiye", "tr",
        "türkiye geneli", "tüm türkiye",
    ],
    "istanbul": ["istanbul", "İstanbul"],
    "izmir": ["izmir", "İzmir"],
    "bursa": ["bursa"],
    "avrupa": [
        "europe", "eu", "avrupa", "emea",
        "germany", "netherlands", "uk", "united kingdom",
        "berlin", "amsterdam", "london", "paris", "dublin",
    ],
    "abd": [
        "united states", "usa", "us",
        "new york", "san francisco", "seattle", "austin",
        "california", "texas", "americas",
    ],
}

LOCATION_SCORES = {
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
}

# ──────────────────────────────────────────────
# Level Tanimlari
# ──────────────────────────────────────────────
LEVEL_KEYWORDS = {
    "junior": [
        "junior", "jr.", "jr ",
        "entry level", "entry-level", "entrylevel",
        "yeni mezun", "stajyer", "intern", "internship",
        "0-2 yıl", "0-1 yıl", "1-2 yıl", "0-2 years", "0-1 years",
        "new grad", "graduate", "fresh graduate", "recent graduate",
        "associate", "trainee", "apprentice",
        "i ", "level 1", "level i",
    ],
    "mid": [
        "mid level", "mid-level", "midlevel", "middle", "intermediate",
        "2-5 yıl", "3-5 yıl", "2+ yıl", "3+ yıl",
        "2-5 years", "3-5 years", "2+ years", "3+ years",
        "ii ", "iii", "level 2", "level 3",
        "regular", "experienced",
    ],
    "senior": [
        "senior", "sr.", "sr ",
        "staff", "principal", "kıdemli", "deneyimli",
        "5+ yıl", "7+ yıl", "10+ yıl",
        "5+ years", "7+ years", "10+ years",
        "expert", "specialist", "uzman",
    ],
    "lead": [
        "lead developer", "lead engineer", "lead programmer",
        "tech lead", "team lead", "technical lead",
        "engineering manager", "director of engineering",
        "head of engineering", "head of development",
        "vp engineering", "vp of engineering",
        "cto", "chief technology",
        "takım lideri", "teknik lider", "müdür", "yönetici",
    ],
}

LEVEL_SCORES = {
    "junior": 5,
    "entry": 5,
    "mid": 2,
    "senior": -10,
    "lead": -15,
    "bilinmiyor": 0,
}
