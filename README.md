# Job Radar – RSS + Skor + Google Sheets Pipeline

Bu proje, yazılım / game development odaklı iş ilanlarını RSS kaynaklarından çekerek
önceliklendiren, skorlayan ve Google Sheets’e otomatik ekleyen bir sistemdir.

Amaç:
- Sabah tek komut çalıştırmak
- Yeni ilanları otomatik toplamak
- Ankara / Remote öncelikli filtrelemek
- GameDev ağırlıklı skorlamak
- Tek bir Sheet üzerinden karar vermek

---

# 🎯 Hedef

- Ankara veya Remote iş bulmak
- GameDev öncelikli
- Alternatif olarak C#, Python, Java, Mobile, CV
- İngilizce ve Türkçe ilanları birlikte değerlendirmek
- Manuel iş arama süresini 1 saate değil 10-15 dakikaya düşürmek

---

# 🏗 Sistem Mimarisi

RSS Kaynakları
        ↓
İlan Parse (Başlık + Açıklama)
        ↓
Alan Tespiti (Keyword)
        ↓
Lokasyon Analizi
        ↓
Level Analizi
        ↓
Skor Hesaplama
        ↓
Duplicate Kontrol
        ↓
Google Sheets’e Ekle

Script her sabah manuel çalıştırılır.

---

# 📂 Proje Yapısı

```
job-radar/
│
├── main.py
├── config.py
├── scorer.py
├── rss_sources.py
├── sheets_client.py
├── requirements.txt
└── README.md
```

---

# 📡 RSS Kaynakları

İlk versiyon için:

- Indeed
- WeWorkRemotely
- Hitmarker
- Remotive

Sadece RSS kullandığımız için:
- Ban riski yok
- Scraping yapılmaz
- Stabil çalışır

---

# 📊 Google Sheets Yapısı

Kolonlar:

| Tarih | Firma | Pozisyon | Şehir | Remote | Kaynak | Link | Alan | Level | Alan Skoru | Lokasyon Skoru | Level Skoru | Toplam Skor | Başvuru | DM | Not |

---

# 🧠 Skor Sistemi

## 1️⃣ Alan Skoru (Ağırlık %50)

| Alan | Puan |
|------|------|
| gamedev | 5 |
| c# | 4 |
| python | 3 |
| mobile | 3 |
| java | 2 |
| cv | 2 |
| diğer | 1 |

---

## 2️⃣ Lokasyon Skoru (Ağırlık %30)

| Durum | Puan |
|--------|------|
| Ankara | 5 |
| Remote | 5 |
| Hybrid Ankara | 4 |
| Türkiye | 3 |
| İstanbul | 1 |
| Diğer | 0 |

---

## 3️⃣ Level Skoru (Ağırlık %20)

| Seviye | Puan |
|--------|------|
| Junior | 5 |
| Entry | 5 |
| Mid | 3 |
| Senior | -5 |
| Lead | -10 |

---

## 🎯 Final Formül

```
Toplam Skor = (Alan*0.5 + Lokasyon*0.3 + Level*0.2)
```

---

# 🌍 Türkçe + İngilizce Desteği

Keyword listeleri çift dillidir.

Örnek:

GameDev:
- unity
- unreal
- game
- oyun
- gameplay
- mobile game

Junior:
- junior
- entry
- yeni mezun
- 0-2 yıl

Remote:
- remote
- uzaktan

Ankara:
- ankara

Bu sayede TR ve EN ilanlar birlikte değerlendirilir.

---

# 🔍 Alan Tespiti Mantığı

İlan başlığı + açıklaması lowercase yapılır.
Keyword eşleşmesine göre alan belirlenir.

Öncelik sırası:
1. gamedev
2. c#
3. python
4. mobile
5. java
6. cv
7. diğer

---

# 🔁 Duplicate Önleme

Google Sheet’e eklemeden önce:

- Aynı link var mı?
- Aynı firma + pozisyon var mı?

Kontrol edilir.

---

# 🖥 Kurulum (Windows)

## 1️⃣ Sanal ortam oluştur

```
python -m venv venv
venv\Scripts\activate
```

## 2️⃣ Paketleri yükle

```
pip install feedparser
pip install gspread
pip install google-auth
pip install pandas
```

requirements.txt oluşturulabilir.

---

# 🔐 Google Sheets API Kurulumu

1. Google Cloud Console → yeni proje
2. Service Account oluştur
3. JSON key indir
4. Sheet’i service account maili ile paylaş
5. JSON dosyasını proje içine koy

---

# ▶️ Çalıştırma

```
python main.py
```

Script:
- RSS’leri çeker
- Filtreler
- Skorlar
- Yeni ilanları Sheet’e ekler

---

# 🧪 Gelecek Upgrade Planı

Bu MVP sürümdür.

İleride eklenecekler:

- LinkedIn email parse
- Kariyer.net email parse
- TF-IDF skorlama
- NLP benzerlik analizi
- Otomatik DM önerisi
- Mini dashboard

---

# 🚀 Günlük Kullanım Akışı

Sabah:

1. python main.py
2. Google Sheet aç
3. Skora göre sırala
4. 3.5 üstü ilanlara başvur
5. HR bul → yarı otomatik DM gönder

Toplam süre: 15-20 dakika

---

# 💡 Stratejik Not

Amaç çok ilana başvurmak değil,
yüksek eşleşmeli ilanlara hızlı ve düzenli başvurmaktır.

Bu sistem:
- Duygusal başvuru yapmayı engeller
- Ankara + Remote önceliğini korur
- GameDev odağını kaybetmez
- Global ilanları kaçırmaz

---

# 📌 Proje Durumu

Versiyon: v0.1 (RSS + Rule-Based Skor)

```
Durum: MVP
Ban Riski: Yok
Otomasyon Seviyesi: Yarı Otomatik
Karar Kontrolü: Manuel
```

---

# 🔥 Nihai Amaç

Ankara’da yaşayabilecek maaş sağlayan
PC mühendisliği ile alakalı
GameDev veya yazılım işi bulmak.

Remote opsiyonu her zaman açık.

Bu sistem o hedefe sistematik yaklaşmak için tasarlanmıştır.
