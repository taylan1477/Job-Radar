# 🎯 Job Radar v0.6.7

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Active-success)](https://github.com/taylan1477/Job-Radar)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![Clean Code](https://img.shields.io/badge/Clean%20Code-Showcase-blueviolet)](showcase.py)

**Job Radar**, yazılım ve GameDev odaklı iş ilanlarını **4 farklı kaynaktan** (LinkedIn, JSearch, RSS, Kariyer.net) otomatik olarak toplayan, NLP (Doğal Dil İşleme) tabanlı bir skorlama algoritmasıyla değerlendiren ve sonuçları dinamik bir Google Sheets tablosuna aktaran profesyonel bir iş arama otomasyonudur.

> [!TIP]
> Bu proje, sadece bir iş arama aracı değil, aynı zamanda **Clean Code**, **SOLID prensipleri** ve **Modern Mimari** yaklaşımlarını sergileyen bir portfolyo çalışmasıdır.

## 🚀 Öne Çıkan Özellikler

- **Multi-Source Aggregation:** LinkedIn (Scraping), JSearch (API), RSS ve Kariyer.net entegrasyonu.
- **NLP Powered Scoring:** TF-IDF ve gelişmiş Regex kullanarak ilanları teknoloji, lokasyon ve seviyeye göre puanlar.
- **Smart Google Sheets Entegrasyonu:** Koşullu biçimlendirme, dinamik sütunlar ve "Smart Chips" ile başvuru takibi.
- **Clean Code Showcase:** Pydantic veri modelleri, servis tabanlı mimari ve kapsamlı birim testleri.
- **Erişilebilirlik:** Windows Unicode ve I/O çakışmaları için optimize edilmiş kararlı çalışma.

## 🎯 Hedef ve Kapsam

Projeyi özellikle şu kriterlere odaklı ilanları bulmak için geliştirdim:

- **Odak:** GameDev (Unity, Unreal, C#, C++) & Yazılım Geliştirme.
- **Lokasyon:** Ankara, Remote veya Hibrit fırsatları.
- **Verimlilik:** Günlük iş tarama ve takip süresini manuel süreçlerden **15 dakikaya** indirgemek.

## 📡 Veri Kaynakları

| Kaynak | Yöntem | API Kullanımı | Tipik Sonuç |
| -------- | -------- | ---------- | ------------- |
| **LinkedIn** | Playwright scraping | Ücretsiz | ~170 ilan |
| **JSearch** | REST API (RapidAPI) | 5 call/tarama | ~40 ilan |
| **RSS** | WeWorkRemotely, Himalayas | Ücretsiz | ~125 ilan |
| **Kariyer.net** | Playwright + Stealth | Ücretsiz | WAF engelli |

## 🌟 Yenilikler (v0.6.7)

Bu versiyonda projenin modüler mimarisi tamamlandı ve kod kalitesi standartları yükseltildi:

- **Modüler Mimari:** Tüm modüller `src` altına taşınarak `core`, `clients` ve `utils` şeklinde profesyonelce gruplandırıldı.
- **Root Temizliği:** Dokümantasyonlar `docs/`, testler `tests/` klasörlerine taşınarak proje kök dizini düzenlendi.
- **Merkezi Loglama:** `src/utils/logger.py` ile tüm sistem genelinde standart ve Türkçe karakter uyumlu loglama sağlandı.
- **Kod İyileştirmesi:** `main.py` ve diğer modüllerdeki Duplicate Code ve Shadowing uyarıları giderildi, `requirements.txt` güncellendi.
- **Gelişmiş Görselleştirme:** Google Sheets'teki "Durum" sütununa göre dinamik satır renklendirme ve Smart Chips sistemi optimize edildi.

## 📂 Proje Yapısı

```
job-radar/
├── src/
│   ├── core/               # Ana İş Mantığı ve Modeller
│   │   ├── models.py       # Pydantic veri modelleri ve Enum tanımları
│   │   ├── nlp_processor.py # Metin temizleme, dil tespiti ve TF-IDF işlemleri
│   │   ├── scorer.py       # İlan puanlama algoritması (Regex + NLP)
│   │   └── scoring_service.py # Puanlama mantığının servis katmanı (Showcase)
│   ├── clients/            # Dış Entegrasyonlar ve Botlar
│   │   ├── jsearch_client.py # JSearch API istemcisi
│   │   ├── kariyer_scraper.py # Kariyer.net için Playwright scraper
│   │   ├── linkedin_scraper.py # LinkedIn için Playwright scraper
│   │   ├── rss_sources.py  # RSS kaynakları (WWR, Himalayas)
│   │   └── sheets_client.py # Google Sheets API ve tablo işlemleri
│   └── utils/              # Yardımcı Araçlar ve Yapılandırma
│       ├── config.py       # Puan ağırlıkları ve API ayarları
│       ├── corpus.py       # NLP veri havuzu
│       ├── logger.py       # Merkezi loglama sistemi
│       ├── analyze_keywords.py # Kelime frekans analiz aracı
│       └── showcase.py     # Clean Code sunum scripti
├── tests/                  # Pytest birim testleri
├── docs/                   # Proje sunum ve dokümantasyon dosyaları
├── main.py                 # Uygulama giriş noktası
├── requirements.txt        # Bağımlılıklar
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
6. Tabloyu Duzelt (Format/Renk/Sutun)     → Tabloyu onarır, Renklendirmeyi uygular
7. Cikis
```

> 💡 **Günlük kullanım için Menü 3 önerilir** — API harcamadan LinkedIn + RSS'ten ~300 ilan çeker. JSearch'e ihtiyaç duyulursa Menü 4 ile sadece 5 call harcanır.

## 📊 Skor Sistemi

```
Toplam = (Alan × 0.3) + (Lokasyon × 0.4) + (Level × 0.3)
```

| Alan | Puan | | Lokasyon | Puan | | Level | Puan |
| ------ | ------ | - | ---------- | ------ | - | ------- | ------ |
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

## 🔧 Tablo Otomasyonu (Menü 6)

Sheet'te yapısal sorunlar veya format bozuklukları olduğunda çalıştırılır:

1. **Format Düzeltme:** Tarihleri `YYYY-MM-DD` yapar, skorları sayıya çevirir.
2. **Otomatik Renklendirme:** Duruma göre satırları (Reddedildi=Kırmızı, Favori=Sarı vb.) boyar.
3. **Akıllı Çip Ekleme:** "Durum" sütununa `Favori, Başvuruldu, Reddedildi, Görüşmede, Süre Bitti, Ulaşılmaz` seçeneklerini ekler.

---

## 🛠 Teknolojiler ve Araçlar

- **Backend:** Python 3.10+
- **Veri Toplama:** Playwright (Web Scraping), BeautifulSoup4, REST APIs
- **NLP & İşleme:** Scikit-learn (TF-IDF), Regex, Pandas
- **Entegrasyon:** Google Sheets API, Gspread
- **Kalite & Standart:** Pydantic (Validation), Pytest (Testing)

---

## 🏗 Mimari ve Clean Code

Proje, genişletilebilir ve bakımı kolay bir yapı için modüler bir mimari üzerine kurulmuştur:

- **Showcase Modülü:** `scoring_service.py` ve `models.py` dosyaları, profesyonel yazılım geliştirme standartlarını (Type Hinting, Dependency Injection, Validation) temsil eder.
- **NLP Motoru:** `nlp_processor.py`, ham metin verilerini normalize eder ve dil tespiti yaparak puanlamayı etkileyen anlamsal çıkarımlarda bulunur.
- **Data Integrity:** `sheets_client.py`, Google Sheets ile senkronize çalışırken veri kaybını önleyen ve tabloyu otomatik biçimlendiren gelişmiş bir katmandır.

---

## 🗺 Geliştirme Yol Haritası (Roadmap)

### v0.7 — Başvuru Hazırlığı & AI Asistanı

| Özellik | Açıklama | Zorluk | Öncelik |
| --------- | ---------- | -------- | --------- |
| **Quick-Apply & İK Mail Parser** | İlan metninden direkt başvuru linki ve İK e-postalarını çekme | ⭐⭐ (2/5) | Yüksek |
| **CV Profile Engine** | Yerel yapılandırılmış profil (cv_profile.yaml) ile aday verisi yönetimi | ⭐⭐ (2/5) | Yüksek |
| **Cover Letter Gen** | İlan gereksinimlerine özel LLM tabanlı kişiselleştirilmiş ön yazı üretimi | ⭐⭐⭐ (3/5) | Yüksek |
| **Cold DM & Mail Gen** | İlgili recruiter için dinamik e-posta/DM taslağı hazırlama | ⭐⭐ (2/5) | Yüksek |

### v0.8 — Çift Kanallı Otomatik Başvuru (Auto-Apply)

| Özellik | Açıklama | Zorluk | Öncelik |
| --------- | ---------- | -------- | --------- |
| **LinkedIn Easy Apply Botu** | Playwright ile form doldurma, CV yükleme ve soru yanıtlama | ⭐⭐⭐⭐ (4/5) | Kritik |
| **Otomatik E-Posta Başvurusu** | İK e-postalarına dinamik cover letter ve CV PDF ekli otomatik başvuru | ⭐⭐ (2/5) | Yüksek |
| **Şirket Kara Liste** | Belirli şirketlerin ilanlarını otomatik gizleme/puan kırma | ⭐ (1/5) | Düşük |
| **Rate Limiter & Safety** | İnsan benzeri bekleme süreleri ve günlük başvuru kotası | ⭐⭐ (2/5) | Yüksek |

### v0.9 — Geri Dönüş & Sonuç Takibi (Feedback Loop)

| Özellik | Açıklama | Zorluk | Öncelik |
| --------- | ---------- | -------- | --------- |
| **Gmail API Entegrasyonu** | Gelen kutusundaki şirket ve başvuru yanıtlarını otomatik tarama | ⭐⭐⭐ (3/5) | Yüksek |
| **Hibrit E-Posta Sınıflandırıcı** | Regex + LLM ile ret/mülakat/görüşme durumlarını tespit etme | ⭐⭐⭐ (3/5) | Yüksek |
| **Google Sheets Otomatik Senkron** | Gelen yanıtlara göre tablodaki 'Durum' sütununu otomatik güncelleme | ⭐⭐ (2/5) | Yüksek |

### v1.0 — Tam Otonom Asistan (End-to-End)

| Özellik | Açıklama | Zorluk | Öncelik |
| --------- | ---------- | -------- | --------- |
| **End-to-End Pipeline** | Tara → Skorla → Başvur (Easy Apply / Mail) → Sonuçları Oku (Gmail) → Güncelle | ⭐⭐⭐⭐⭐ (5/5) | Kritik |
| **A/B Test Engine** | Hangi ön yazı/başvuru metodunun daha çok dönüt aldığı analizi | ⭐⭐⭐ (3/5) | Düşük |
| **Multi-User / DB** | Yerel dosyadan PostgreSQL/Cloud veritabanına geçiş | ⭐⭐⭐⭐ (4/5) | Düşük |

---

## 📌 Proje Durumu

```
Versiyon  : v0.6.7
Kaynaklar : LinkedIn + JSearch + RSS (+ Kariyer.net hazır)
Skor      : NLP (TF-IDF) + Hybrid Regex + Pydantic Validation
Yetenek   : Junior / Game Dev pozisyonları için optimize edildi
```

### 🧠 Akıllı Filtreleme Detayları

1. **Dil Bariyeri:** Sistem İngilizce (`en`) ve Türkçe (`tr`) harici dillerdeki ilanları otomatik tespit eder ve lokasyonu **"dead"** yapar (-10 Puan).
2. **Öncelik Kuralları:** Ankara, GameDev ve Junior fırsatları için özel regex + TF-IDF takviyesi ile puanlama yapılır.
3. **Otomasyon:** İlanlar çekilip tabloya yazıldıktan hemen sonra **Tabloyu Düzelt** fonksiyonu otomatik çalışır.
