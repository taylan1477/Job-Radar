# 🎯 Job Radar v1.0 — Otonom İş Arama, Başvuru ve Takip Sistemi

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-Automation-45ba4b?logo=playwright&logoColor=white)](https://playwright.dev/)
[![Gemini AI](https://img.shields.io/badge/Gemini%20AI-2.5%20Flash-8E75C2?logo=google&logoColor=white)](https://ai.google.dev/)
[![Tests](https://img.shields.io/badge/Tests-26%20Passed-success)](tests/)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen)](https://github.com/taylan1477/Job-Radar)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![Clean Code](https://img.shields.io/badge/Clean%20Code-SOLID%20Standards-blueviolet)](src/core/scoring_service.py)

**Job Radar**, yazılım ve GameDev odaklı iş ilanlarını çoklu kaynaklardan otomatik olarak toplayan, NLP ve kural tabanlı algoritmalarla skorlayan, Google Sheets üzerinde canlı bir dashboard sunan ve **LinkedIn Easy Apply** ile **İK E-posta kanalları** üzerinden uçtan uca **otonom başvuru ve sonuç takibi** gerçekleştiren yeni nesil bir kariyer otomasyon pipeline'ıdır.

> [!IMPORTANT]
> Bu proje; yalnızca bir veri madenciliği aracı değil, aynı zamanda **Playwright tabanlı Web Otomasyonu**, **Gemini LLM Entegrasyonu**, **SOLID Prensipleri**, **Clean Code** ve **Savunmacı Mühendislik (Defensive Engineering)** standartlarını sergileyen kapsamlı bir sistemdir.

---

## 🚀 Öne Çıkan Yetenekler

```
  [Veri Toplama] ───► [NLP Skorlama] ───► [Google Sheets] ───► [Otonom Başvuru] ───► [Gmail Takip]
   LinkedIn / API      TF-IDF + Regex       Smart Chips         Easy Apply / Mail      IMAP + AI Analiz
```

- **Çok Kaynaklı Veri Madenciliği (Multi-Source Aggregation):**
  - **LinkedIn:** Playwright ile stealth modda dinamik web kazıma (~170+ ilan).
  - **JSearch (RapidAPI):** Global aggregator REST API entegrasyonu (~40+ ilan).
  - **RSS Feeds:** WeWorkRemotely ve Himalayas akışları (~125+ ilan).
  - **Kariyer.net:** WAF uyumlu Playwright kazıma altyapısı.
- **Hibrit Skorlama Motoru (NLP + Heuristic Scoring):**
  - Alan (GameDev, C#, Python, C++ vb.), lokasyon (Ankara, Remote, Hibrit) ve tecrübe seviyesine (Junior, Mid, Senior) göre ağırlıklı puanlama.
  - **Dil Bariyeri Kontrolü:** Türkçe ve İngilizce dışındaki ilanları anında eleyen dil tespit filtresi.
  - **Platform Önceliği:** LinkedIn ilanlarına `+1.0` bonus, harici panolara `-1.0` puan kesintisi.
- **Google Sheets Canlı Yönetim Paneli:**
  - Otomatik formül eşitleme, koşullu satır renklendirme ve açılır menülü **Smart Chips** (`Favori, Başvuruldu, Reddedildi, Görüşmede, Süre Bitti, Ulaşılmaz`).
- **Otonom Çift Kanallı Başvuru Motoru (Auto-Apply Pipeline):**
  - **LinkedIn Easy Apply Botu:** Oturumu korunan Chromium ile formları adayın profiline göre otomatik doldurma, CV yükleme ve adım adım ilerleme.
  - **E-Posta İK Başvurusu:** İlan metninden çıkarılan İK iletişim adreslerine Gemini ile üretilmiş kişiselleştirilmiş Cover Letter ve PDF CV ile otomatik başvuru.
  - **Human-in-the-Loop:** Güvenlik kotası (oturum başına maks 15 başvuru) ve son adımda kullanıcı onay mekanizması.
- **Geri Dönüş & Sonuç Takibi (Feedback Loop):**
  - Gmail IMAP üzerinden gelen kutusunu tarama.
  - Gelen şirket e-postalarını Regex + LLM ile sınıflandırma (`Mülakat/Görüşme`, `Reddedildi`, `Alındı`) ve Sheets tablosundaki durumları otomatik senkronize etme.

---

## 🧠 Akıllı Form Yanıtlama ve Başvuru Kuralları

LinkedIn Easy Apply botu, aday profilindeki (`cv_profile.yaml`) parametreleri ve sektör dinamiklerini gözeterek savunmacı kurallarla çalışır:

1. **Deneyim Yılında "Asla 0 Yok" Kuralı:**
   - Adayın bildiği alanlarda (Unity, C#, Python, SQL vb.) otomatik olarak **`3`**,
   - .NET Core / ASP.NET alanında özel talep doğrultusunda **`1`**,
   - Adayın bilmediği / listelenmeyen teknolojilerde (Java, Flutter, Rust vb.) asla 0 değil, minimum **`1`** yıl girilir.
2. **Yabancı Dil Bariyeri:**
   - Profilde bulunmayan dillerde (Çince, Fransızca, İspanyolca vb.) açılır menülerde *"None / Yok / Bilmiyorum"* veya en düşük temel seviye seçilir.
3. **Maaş Beklentisi Optimizasyonu:**
   - Ücret ve maaş sorularına metin hatalarını engelleyecek şekilde net **`35000`** (35.000 TL) girilir.
   - Aralık menülerinde `30.000 - 40.000 TL` bandı seçilir; dövizli ilanlarda aylık `$1500`, yıllık `$25000` atanır.
4. **Feed Koruması (Şirket Takibini Kaldırma):**
   - LinkedIn'in varsayılan olarak seçili getirdiği *"Sayfasından haber almak için ... şirketini takip edin"* kutucuğu otomatik olarak kaldırılır (`uncheck`); adayın akışı yüzlerce şirketin reklamıyla kirlenmez.
   - Zorunlu sözleşme, gizlilik ve onay kutucukları eksiksiz işaretlenir.
5. **Dinamik DOM & Etiket Çıkarımı:**
   - Form elemanlarının etiketleri `aria-label`, `<label for="...">`, parent `fb-dash-form-element` ve `<legend>` katmanlarından okunarak hiçbir soru yanıtsız bırakılmaz.

---

## 📂 Proje Mimarisi

```
job-radar/
├── src/
│   ├── core/                       # Çekirdek İş Mantığı & Modeller
│   │   ├── application_generator.py # Gemini LLM Cover Letter & Easy Apply soru yanıtlayıcı
│   │   ├── email_classifier.py     # E-posta yanıtlarını (Ret/Mülakat) analiz eden motor
│   │   ├── models.py               # Pydantic veri şemaları (Job, Score, Status)
│   │   ├── nlp_processor.py        # TF-IDF, metin temizleme ve dil tespiti
│   │   ├── scorer.py               # Hibrit skorlama algoritması (Regex + NLP)
│   │   └── scoring_service.py      # Servis katmanı ve bağımlılık yönetimi
│   ├── clients/                    # Harici Entegrasyonlar ve Botlar
│   │   ├── easy_apply_client.py    # Playwright LinkedIn Easy Apply otomasyon istemcisi
│   │   ├── email_client.py         # SMTP/IMAP E-posta başvuru ve gelen kutusu istemcisi
│   │   ├── jsearch_client.py       # RapidAPI JSearch REST istemcisi
│   │   ├── kariyer_scraper.py      # Kariyer.net Playwright scraper
│   │   ├── linkedin_scraper.py     # LinkedIn Playwright stealth scraper
│   │   ├── rss_sources.py          # WeWorkRemotely & Himalayas RSS okuyucu
│   │   └── sheets_client.py        # Google Sheets API & Smart Chips yöneticisi
│   └── utils/                      # Yapılandırma ve Yardımcı Araçlar
│       ├── config.py               # Ortam değişkenleri ve katsayılar
│       ├── corpus.py               # NLP durak kelimeler ve anahtar kelime havuzu
│       ├── logger.py               # Türkçe uyumlu merkezi loglama sistemi
│       ├── text_norm.py            # Türkçe karakter (İ/ı, Ş/ş) normalizasyonu
│       └── showcase.py             # Mimari ve SOLID prensipleri sunum aracı
├── tests/                          # 26 Adet Pytest Birim Testi
├── docs/                           # CV ve Dokümantasyon Dosyaları
├── cv_profile.yaml                 # Aday yetkinlik, dil, maaş ve başvuru profili
├── linkedin_state.json             # Oturum çerezleri (Gitignore korumalı)
├── main.py                         # İnteraktif CLI konsol arayüzü
├── requirements.txt                # Python bağımlılıkları
└── README.md
```

---

## ⚙️ Kurulum

### 1. Depoyu Klonlayın ve Sanal Ortam Oluşturun

```bash
git clone https://github.com/taylan1477/Job-Radar.git
cd Job-Radar

# Sanal ortam
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

### 2. Bağımlılıkları ve Tarayıcı Motorunu Yükleyin

```bash
pip install -r requirements.txt
playwright install chromium
```

### 3. Çevre Değişkenlerini Tanımlayın (`.env`)

Proje kök dizininde bir `.env` dosyası oluşturun:

```env
# Google Sheets Entegrasyonu
GOOGLE_SHEETS_CREDENTIALS_FILE=credentials.json
GOOGLE_SHEET_NAME=Job Radar

# Gemini AI (Ön yazı üretimi ve soru yanıtlama için)
GEMINI_API_KEY=your_gemini_api_key

# JSearch API (Opsiyonel)
RAPIDAPI_KEY=your_rapidapi_key

# E-Posta Başvurusu ve Yanıt Takibi (Gmail App Password)
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_gmail_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
IMAP_SERVER=imap.gmail.com
```

### 4. Aday Profilinizi Düzenleyin (`cv_profile.yaml`)

Kendi yetkinliklerinizi, deneyim yıllarınızı, konuşma dillerinizi ve maaş beklentinizi [`cv_profile.yaml`](cv_profile.yaml) dosyasından yapılandırın. CV dosyanızı proje kök dizinine `cv.pdf` olarak ekleyin.

---

## ▶️ Kullanım (İnteraktif Konsol Menüsü)

Uygulamayı başlatın:

```bash
python main.py
```

Açılan konsol menüsü:

```text
=======================================================
  Job Radar v1.0 - Otonom Başvuru & Takip Sistemi
=======================================================

  [TARAMA & VERİ]
  1. Tam çalıştır (Tüm kaynakları tara -> Sheets'e yaz)
  2. Temiz çalıştır (SİL + Tüm kaynakları tara)
  3. API'siz çalıştır (LinkedIn + RSS, JSearch yok) ✨ (Önerilen)
  4. Sadece API (JSearch)
  5. Dry Run (Konsola yazdır, Sheets'e yazma)
  6. Tabloyu Düzelt (Başlık/Sütun/Tarih/Smart Chips)

  [OTONOM BAŞVURU & TAKİP]
  7. LinkedIn Oturumu Aç (Tek seferlik session kaydet)
  8. Otonom Başvuru Yap (Easy Apply + E-Posta | Onaylı)
  9. E-posta Yanıtlarını Kontrol Et (Gmail IMAP Sync)
  10. Çıkış
```

### 🎯 Adım Adım Otonom Başvuru Akışı:

1. **İlk Kurulumda Oturum Açma (Menü 7):**
   - Açılan Chromium penceresinde LinkedIn hesabınıza bir defaya mahsus manuel giriş yapın. Çerezler `linkedin_state.json` içine güvenle kaydedilir; sonraki tüm başvurular bu oturum üzerinden bot engeline takılmadan çalışır.
2. **Başvuru Pipeline'ı (Menü 8):**
   - Hedef Skor Aralığını girin (örn: `2.5 - 10.0` veya `3.0 - 5.0`).
   - Kanal Seçimi yapın (`1. Tümü`, `2. Sadece LinkedIn Easy Apply`, `3. Sadece E-Posta`).
   - Human-in-the-Loop modunda formların dolduruluşunu tarayıcıda canlı inceleyip `E/H` onayı ile gönderin.
3. **Gmail Yanıt Takibi (Menü 9):**
   - Şirketlerden gelen ret, mülakat daveti veya alındı e-postalarını tarayarak Google Sheets üzerindeki Durum sütununu otomatik güncelleyin.

---

## 📊 Skorlama Matrisi

```text
Toplam Skor = (Alan Puanı × 0.3) + (Lokasyon Puanı × 0.4) + (Level Puanı × 0.3) + Platform Bonusu
```

| Alan | Puan | | Lokasyon | Puan | | Level | Puan |
| :--- | :---: | - | :--- | :---: | - | :--- | :---: |
| **gamedev** | 5 | | **ankara** | 5 | | **junior** | 5 |
| **c#** | 4 | | **remote** | 5 | | **entry** | 5 |
| **c++** | 4 | | **hybrid_ankara** | 5 | | **mid** | 2 |
| **python** | 4 | | **türkiye** | 3 | | **senior** | -10 |
| **mobile** | 3 | | **istanbul** | 3 | | **lead** | -15 |
| **yazılım** | 2 | | **avrupa** | 1 | | **bilinmiyor**| 0 |
| **LinkedIn Bonusu** | **+1.0** | | **Harici İlan Cezası** | **-1.0** | | **Yabancı Dil Bariyeri** | **-10 (Dead)** |

---

## 🧪 Testler

Sistemdeki tüm algoritmalar, soru yanıtlayıcılar ve güvenlik bariyerleri Pytest ile doğrulanmaktadır:

```bash
python -m pytest tests/
```

```text
tests/test_easy_apply.py ......                                [ 23%]
tests/test_email_classifier.py .....                           [ 42%]
tests/test_email_client.py ...                                 [ 53%]
tests/test_lang.py .                                           [ 57%]
tests/test_scorer.py ..                                        [ 65%]
tests/test_scoring_service.py .........                        [100%]

============================= 26 passed in 3.27s =============================
```

---

## 🛠 Kullanılan Teknolojiler

- **Programlama:** Python 3.10+ (Type Hinting, Dataclasses)
- **Web Otomasyonu:** Playwright (Chromium Stealth, Multi-step Form Handling)
- **Yapay Zeka (LLM):** Google Gemini 2.5 Flash (`google-genai` SDK)
- **NLP & Metin Analizi:** Scikit-learn (TF-IDF), Regular Expressions, Pandas
- **Entegrasyonlar:** Google Sheets API (`gspread`), Gmail IMAP / SMTP
- **Veri Doğrulama & Test:** Pydantic v2, Pytest

---

## 📄 Lisans

Bu proje [MIT Lisansı](LICENSE) kapsamında lisanslanmıştır. Kendi iş arama süreçleriniz için serbestçe çatallayabilir ve geliştirebilirsiniz.
