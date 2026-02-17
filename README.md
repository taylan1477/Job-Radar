# Job Radar v0.5

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
├── sheets_client.py     # Google Sheets CRUD + fix + smart chips
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
6. Tabloyu Duzelt (baslik/sutun/tarih)    → Tabloyu onarır, Dropdown ekler
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

## 🔧 Tabloyu Düzelt (Menü 6)

Sheet'te yapısal sorunlar veya format bozuklukları olduğunda çalıştırılır:
1.  **Format Düzeltme:** Tarihleri `YYYY-MM-DD` yapar, skorları sayıya çevirir.
2.  **Hyperlink Onarımı:** Türkçe Excel formül yapısına `;` uygun hale getirir.
3.  **Akıllı Çip Ekleme:** "Durum" sütununa `Favori, Başvuruldu, Reddedildi, Görüşmede` seçeneklerini ekler.
4.  **Sütun Temizliği:** Gereksiz "Kaynak" sütununu kaldırır.

---

## 🗺 Geliştirme Yol Haritası (Roadmap)

Görevler zorluk derecelerine göre puanlanmıştır (1=Kolay, 5=Çok Zor).

### v0.5 — Otomasyon & Akıllı Takip *(Şu Anki Hedef)*

| Özellik | Açıklama | Zorluk | Öncelik |
|---------|----------|--------|---------|
| **Quick-Apply Link Generator** | Yüksek skorlu ilanların linklerini topluca açan script | ⭐ (1/5) | Yüksek |
| **Discord Bildirim Botu** | Yeni ≥3.5 puanlı ilan düşünce Discord'a mesaj at | ⭐⭐ (2/5) | Orta |
| **Cron / Task Scheduler** | Scripti her sabah 09:00'da otomatik çalıştır | ⭐ (1/5) | Orta |
| **Duplicate Akıllı Tespit** | Farklı kaynaklardaki aynı ilanı (başlık+firma) yakala | ⭐⭐ (2/5) | Düşük |

### v0.6 — Başvuru Hızlandırıcılar

| Özellik | Açıklama | Zorluk | Öncelik |
|---------|----------|--------|---------|
| **CV Auto-Fill (Playwright)** | LinkedIn Easy Apply formlarını otomatik doldur | ⭐⭐⭐⭐ (4/5) | Yüksek |
| **Cover Letter Generator** | İlan metnine özel ChatGPT tabanlı ön yazı oluştur | ⭐⭐⭐ (3/5) | Orta |
| **Cold DM Generator** | İlan sahibi recruiter için LinkedIn mesaj taslağı hazırla | ⭐⭐ (2/5) | Düşük |

### v0.7 — Analiz & Görselleştirme

| Özellik | Açıklama | Zorluk | Öncelik |
|---------|----------|--------|---------|
| **Streamlit Dashboard** | Skor dağılımı, günlük ilan sayısı grafikleri | ⭐⭐ (2/5) | Düşük |
| **Maaş Tahmini** | Benzer ilanlardan maaş aralığı tahmini (Regresyon) | ⭐⭐⭐ (3/5) | Düşük |
| **Şirket Kara/Beyaz Liste** | İstenmeyen şirketleri blacklist'e ekle, puan düşür | ⭐ (1/5) | Orta |

### v1.0 — Tam Otonom Asistan

| Özellik | Açıklama | Zorluk | Öncelik |
|---------|----------|--------|---------|
| **End-to-End Pipeline** | Tara → Skorla → Başvur → Takip et → Bildir | ⭐⭐⭐⭐⭐ (5/5) | Uzun vade |
| **A/B Test Cover Letters** | Hangi ön yazı daha çok dönüş alıyor analizi | ⭐⭐⭐ (3/5) | Uzun vade |
| **Mülakat Hazırlığı** | İlan requirementlarına göre teknik mülakat sorusu üret | ⭐⭐ (2/5) | Uzun vade |

---

## 📌 Proje Durumu

```
Versiyon  : v0.5
Kaynaklar : LinkedIn + JSearch + RSS (+ Kariyer.net hazır)
Skor      : Rule-based (keyword matching, 8 alan + 10 lokasyon + 6 level)
Sheet     : Akıllı Çip (Dropdown) + Otomatik Formatlama
Keyword   : 200+ keyword
Menü      : 7 seçenek (API'li / API'siz / dry run / düzeltme)
Otomasyon : Yarı-otomatik (günlük çalıştır)
```
