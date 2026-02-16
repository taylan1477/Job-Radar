# Job Radar v0.4

Yazılım / GameDev odaklı iş ilanlarını **4 kaynaktan** otomatik toplayıp skorlayan, Google Sheets'e yazan ve başvuru sürecini hızlandıran bir pipeline.

## 🎯 Hedef

- Ankara / Remote iş bulmak
- GameDev öncelikli (Unity, Unreal, C#, C++)
- Türkçe + İngilizce ilanları birlikte değerlendirmek
- Günlük iş arama süresini **15 dakikaya** düşürmek

## 📡 Veri Kaynakları

| Kaynak | Yöntem | API Kullanımı | Tipik Sonuç |
|--------|--------|---------------|-------------|
| **LinkedIn** | Playwright scraping | ❌ Ücretsiz | ~170 ilan |
| **JSearch** | REST API (RapidAPI) | ✅ 5 call/tarama | ~40 ilan |
| **RSS** | WeWorkRemotely, Himalayas | ❌ Ücretsiz | ~125 ilan |
| **Kariyer.net** | Playwright + Stealth | ❌ Ücretsiz | WAF engelli |

## 📂 Proje Yapısı

```
job-radar/
├── main.py              # İnteraktif menü + pipeline
├── config.py            # Tüm ayarlar (skorlar, keyword'ler, API key)
├── scorer.py            # Alan/Lokasyon/Level tespiti + skor hesaplama
├── linkedin_scraper.py  # LinkedIn public job search (Playwright)
├── kariyer_scraper.py   # Kariyer.net scraper (Playwright + Stealth)
├── jsearch_client.py    # JSearch API client
├── rss_sources.py       # WeWorkRemotely + Himalayas RSS
├── sheets_client.py     # Google Sheets CRUD + tablo düzeltme
├── requirements.txt     # Python bağımlılıkları
└── README.md
```

## 🖥 Kurulum

```bash
# 1. Sanal ortam
python -m venv venv
venv\Scripts\activate

# 2. Paketler
pip install -r requirements.txt

# 3. Playwright tarayıcı
playwright install chromium
```

### Gereksinimler
- Python 3.10+
- Google Cloud Service Account (Sheets API)
- JSearch API key (RapidAPI, ücretsiz tier)

### Ayarlar (`config.py`)
- `CREDENTIALS_FILE` → Google Service Account JSON
- `SPREADSHEET_ID` → Hedef Google Sheet ID
- `JSEARCH_API_KEY` → RapidAPI key

## ▶️ Kullanım

```bash
python main.py
```

İnteraktif menü:

```
1. Tam calistir (tum kaynaklar)           → LinkedIn + JSearch + RSS + Kariyer.net
2. Temiz calistir (SIL + tum kaynaklar)   → Mevcut veriyi sil, sıfırdan çek
3. API'siz calistir (LinkedIn + RSS)      → JSearch kullanmaz, API harcamaz ✨
4. Sadece API (JSearch)                   → Sadece 5 API call kullanır
5. Dry Run (konsola yazdir)               → Sheet'e yazmaz, test amaçlı
6. Tabloyu Duzelt (baslik/sutun/tarih)    → Mevcut veriyi düzeltir + yeniden skorlar
7. Cikis
```

> 💡 **Günlük kullanım için Menü 3 önerilir** — API harcamadan LinkedIn + RSS'ten ~300 ilan çeker. JSearch'e ihtiyaç duyulursa Menü 4 ile sadece 5 call harcanır.

## 📊 Skor Sistemi

```
Toplam = (Alan × 0.3) + (Lokasyon × 0.4) + (Level × 0.3)
```

| Alan | Puan | | Lokasyon | Puan | | Level | Puan |
|------|------|-|----------|------|-|-------|------|
| gamedev | 5 | | ankara | 5 | | junior | 5 |
| c# | 4 | | remote | 5 | | entry | 5 |
| c++ | 4 | | hybrid_ankara | 5 | | mid | 2 |
| python | 4 | | türkiye | 3 | | senior | -10 |
| mobile | 3 | | istanbul | 3 | | lead | -15 |
| java | 3 | | izmir | 2 | | bilinmiyor | 0 |
| cv | 2 | | bursa | 2 | | | |
| yazılım | 2 | | avrupa | 1 | | | |
| diğer | 1 | | abd | 0 | | | |
| | | | diğer | 0 | | | |

### Skor Örnekleri

| İlan | Alan | Lokasyon | Level | Skor |
|------|------|----------|-------|------|
| Junior Unity Dev @ Ankara | gamedev(5) | ankara(5) | junior(5) | **5,0** |
| Game Dev @ Remote | gamedev(5) | remote(5) | ?(0) | 3,5 |
| Python Dev @ Turkey | python(4) | türkiye(3) | mid(2) | **2,8** |
| Senior Java Dev @ Remote | java(3) | remote(5) | senior(-10) | 0,9 |
| Random Job @ Unknown | diğer(1) | diğer(0) | ?(0) | 0,3 |

### Skoru Özelleştirme

1. `config.py`'de ağırlıkları, alan/lokasyon/level puanlarını veya keyword'leri değiştir
2. **Menüden 6** seç → Tüm ilanlar yeniden skorlanır (API call gerektirmez)

## 🔧 Tabloyu Düzelt (Menü 6)

Her çalıştırmada detaylı log gösterir:

```
--- Degisiklik Ozeti ---
Alan    : 15 hucre
Lokasyon: 23 hucre
Level   : 8 hucre
Skor    : 110 hucre
Tarih   : 124 hucre
TOPLAM  : 280 hucre degisti
```

---

## 🗺 Geliştirme Yol Haritası (Roadmap)

### v0.4 — Akıllı Başvuru Hızlandırma *(Sonraki)*

| Özellik | Açıklama | Zorluk |
|---------|----------|--------|
| **Quick-Apply Link Generator** | Skor ≥ 3.0 ilanların "Başvur" linklerini otomatik topla, tek tıkla aç | ⭐ |
| **CV Auto-Fill (Playwright)** | LinkedIn Easy Apply ve benzeri tek tıklalı başvuru formlarını otomatik doldur | ⭐⭐⭐ |
| **Cover Letter Generator** | Her ilana özel, ilan text'i + kendi profilinden otomatik ön yazı üret (LLM) | ⭐⭐ |
| **Başvuru Takip Sütunu** | Sheet'e "Başvuruldu / Görüşme / Red" durumu ekle | ⭐ |

### v0.5 — Otomasyon & Zamanlama

| Özellik | Açıklama | Zorluk |
|---------|----------|--------|
| **Cron / Task Scheduler** | Günlük otomatik tarama (sabah 09:00) | ⭐ |
| **Telegram / Discord Bot** | Yeni yüksek skorlu ilanları anında bildirim | ⭐⭐ |
| **Duplicate Akıllı Tespit** | Aynı ilanın farklı kaynaklarda olduğunu algıla | ⭐⭐ |
| **Dashboard (Streamlit)** | Basit web arayüzü: skorlar, grafikler, kaynaklar | ⭐⭐ |

### v0.6 — Yapay Zeka Entegrasyonu

| Özellik | Açıklama | Zorluk |
|---------|----------|--------|
| **NLP Skor** | İlan açıklamasını LLM ile analiz et, daha akıllı skor | ⭐⭐⭐ |
| **Profil Eşleştirme** | CV'ni parse et ve ilanla uyum yüzdesi hesapla | ⭐⭐⭐ |
| **Otomatik Portfolio Match** | İlan gereksinimlerini projelerinle eşleştir | ⭐⭐⭐ |

### v1.0 — Tam Otonom İş Arama Asistanı

| Özellik | Açıklama | Zorluk |
|---------|----------|--------|
| **End-to-End Pipeline** | Tara → Skorla → Başvur → Takip et → Bildir | ⭐⭐⭐ |
| **A/B Test Cover Letters** | Farklı ön yazı stilleri dene, hangisi daha çok yanıt alıyor? | ⭐⭐⭐ |
| **Interview Prep** | İlanın gereksinimlerine göre mülakat soruları üret | ⭐⭐ |

---

## 🚀 Hızlı ve Otomatik Başvuru Stratejisi

İlanları çekmek ilk adım — asıl zaman kazancı **başvuru sürecini otomasyona** almakta.

### Strateji 1: Quick-Apply Linkleri (En Kolay — Hemen Yapılabilir)
```
Skor >= 3.0 olan ilanlar → Link sütunundan URL'leri topla → Hepsini tarayıcıda aç
```
Bir Python scripti ile yüksek skorlu ilanların linklerini tek seferde açabilirsin. Gözle 5 saniyede karar ver, başvur veya kapat.

### Strateji 2: LinkedIn Easy Apply Bot (Orta Zorluk)
LinkedIn'deki "Easy Apply" butonlu ilanlar için Playwright ile:
1. Profil bilgilerini `config.py`'ye yaz (isim, email, CV path)
2. Bot otomatik formu doldurur ve gönderir
3. Başvurulan ilanları Sheet'te "Başvuruldu" olarak işaretler

> ⚠️ **Risk:** LinkedIn hesabınız kısıtlanabilir. Günlük max 25 başvuru ve rastgele gecikmeler önerilir.

### Strateji 3: AI Cover Letter + Toplu Başvuru (En Etkili)
1. **Gemini/OpenAI API** ile ilan başlığı + açıklamasına özel cover letter üret
2. CV + cover letter'ı otomatik mail gönder (SMTP) veya form doldur
3. Her başvuruyu Sheet'te logla

### Strateji 4: Türk Platformları İçin Form Bot
Kariyer.net, Yenibiris.com gibi siteler için:
1. Profil bilgilerini bir kez kaydet
2. Playwright ile başvuru formlarını otomatik doldur
3. CAPTCHA varsa manual, yoksa tam otomatik

### Önerilen Başlangıç Sırası
```
1. Quick-Apply Links    → 30 dakikada yapılır, hemen verim alırsın
2. Başvuru Takip Sütunu → Sheet'e "Durum" sütunu ekle, el ile takip et
3. LinkedIn Easy Apply  → Playwright bot, en çok zaman kazandırır
4. AI Cover Letter      → Kaliteli ve kişiselleştirilmiş başvurular
```

---

## 📌 Proje Durumu

```
Versiyon  : v0.4
Kaynaklar : LinkedIn + JSearch + RSS (+ Kariyer.net hazır)
Skor      : Rule-based (keyword matching, 8 alan + 10 lokasyon + 6 level)
Keyword   : 200+ keyword (gamedev, yazılım, remote, şehirler, seviyeler)
Türkçe    : Tam destek (virgüllü skor, Türkçe header'lar)
Menü      : 7 seçenek (API'li / API'siz / dry run / düzeltme)
Otomasyon : Yarı-otomatik (günlük çalıştır)
```
