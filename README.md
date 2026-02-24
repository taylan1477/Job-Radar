# Job Radar v0.6.5 (UX & Stability Update)

Yazılım / GameDev odaklı iş ilanlarını **4 kaynaktan** otomatik toplayıp skorlayan, Google Sheets'e yazan ve başvuru sürecini hızlandıran bir pipeline. Bu versiyon, Fintech ve kurumsal standartlara uygun **Clean Code Showcase** modülünün yanı sıra, gelişmiş görselleştirme ve stabilite güncellemelerini içerir.

## 🎯 Hedef

- Ankara / Remote iş bulmak
- GameDev öncelikli (Unity, Unreal, C#, C++)
- Türkçe + İngilizce ilanları birlikte değerlendirmek
- Günlük iş arama süresini **15 dakikaya** düşürmek

## 📡 Veri Kaynakları

| Kaynak | Yöntem | API Kullanımı | Tipik Sonuç |
|--------|--------|----------|-------------|
| **LinkedIn** | Playwright scraping | Ücretsiz | ~170 ilan |
| **JSearch** | REST API (RapidAPI) | 5 call/tarama | ~40 ilan |
| **RSS** | WeWorkRemotely, Himalayas | Ücretsiz | ~125 ilan |
| **Kariyer.net** | Playwright + Stealth | Ücretsiz | WAF engelli |

## 🌟 Yenilikler (v0.6.5)

Bu versiyonda kullanıcı deneyimi (UX) ve sistem kararlılığına odaklanıldı:

- **Gelişmiş Görselleştirme:** Google Sheets'teki "Durum" sütununa göre tüm satırı otomatik renklendiren **Koşullu Biçimlendirme** sistemi eklendi (Kırmızı, Yeşil, Sarı, Emerald tonları).
- **NLP Refaktörü:** Metin işleme ve dil tespiti mantığı `nlp_processor.py` ve `corpus.py` modülleriyle profesyonel düzeye taşındı.
- **Genişletilmiş Durumlar:** "Süre Bitti" ve "Ulaşılmaz" (Vatandaşlık vb.) seçenekleriyle başvuru takibi hassaslaştırıldı.
- **Windows Stabilite Fix:** Konsoldaki Türkçe karakter (`UnicodeEncodeError`) ve I/O çakışmaları modern `reconfigure` yöntemiyle çözüldü.

## 📂 Proje Yapısı

```
job-radar/
├── main.py              # İnteraktif menü + pipeline
├── config.py            # Tüm ayarlar (skorlar, keyword'ler, API key)
├── nlp_processor.py     # NLP Motoru: Dil tespiti, Normalizasyon, TF-IDF [YENİ]
├── corpus.py            # NLP Veri Havuzu: Expanded Corpus [YENİ]
├── sheets_client.py     # Google Sheets CRUD + Renklendirme + Smart Chips
├── scorer.py            # Puanlama mantığı (NLP entegreli)
├── models.py            # Pydantic veri modelleri & Enumlar (Showcase)
├── scoring_service.py   # Refaktör edilmiş kurumsal Scoring servisi (Showcase)
├── tests/               # Pytest birim testleri (Showcase)
└── README.md
```

## 🖥 Kurulum

```bash
# 1. Sanal ortam
python -m venv venv
venv\Scripts\activate

# 2. Paketler
pip install -r requirements.txt
pip install pydantic pytest pytest-mock gspread-formatting  # Ek gereksinimler

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

## 🔧 Tablo Otomasyonu (Menü 6)

Sheet'te yapısal sorunlar veya format bozuklukları olduğunda çalıştırılır:
1.  **Format Düzeltme:** Tarihleri `YYYY-MM-DD` yapar, skorları sayıya çevirir.
2.  **Otomatik Renklendirme:** Duruma göre satırları (Reddedildi=Kırmızı, Favori=Sarı vb.) boyar.
3.  **Akıllı Çip Ekleme:** "Durum" sütununa `Favori, Başvuruldu, Reddedildi, Görüşmede, Süre Bitti, Ulaşılmaz` seçeneklerini ekler.

---

## 🗺 Geliştirme Yol Haritası (Roadmap)

### v0.7 — Başvuru Hızlandırıcılar (Aktif Geliştirme)

| Özellik | Açıklama | Zorluk | Öncelik |
|---------|----------|--------|---------|
| **Quick-Apply Link** | İlanın direkt başvuru sayfasına giden akıllı link üretimi | ⭐⭐ (2/5) | Orta |
| **Discord Bot** | Yüksek skorlu (>4.0) ilanlar için anlık bildirim sistemi | ⭐⭐⭐ (3/5) | Orta |
| **Cover Letter Gen** | İlan metnine özel ChatGPT tabanlı ön yazı oluşturma | ⭐⭐⭐ (3/5) | Yüksek |
| **Cold DM Gen** | İlgili recruiter için LinkedIn DM taslağı hazırlama | ⭐⭐ (2/5) | Yüksek |

### v0.8 — Analiz & Gelişmiş Filtreleme

| Özellik | Açıklama | Zorluk | Öncelik |
|---------|----------|--------|---------|
| **Şirket Kara Liste** | Belirli şirketlerin ilanlarını otomatik gizleme/puan kırma | ⭐ (1/5) | Orta |
| **Duplicate Tespit** | Farklı platformlardaki aynı ilanları akıllıca gruplama | ⭐⭐⭐ (3/5) | Düşük |
| **Skill Gap Analizi** | Mevcut CV ile ilan arasındaki eksik yetenekleri listeleme | ⭐⭐⭐⭐ (4/5) | Yüksek |
| **Streamlit Dashboard** | Başvuru süreçlerini izlemek için görsel arayüz | ⭐⭐⭐ (3/5) | Düşük |

### v0.9 — Mülakat Hazırlığı & Market Analizi
| Özellik | Açıklama | Zorluk | Öncelik |
|---------|----------|--------|---------|
| **Interview Prep** | İlan requirementlarına göre teknik mülakat sorusu üretimi | ⭐⭐ (2/5) | Orta |
| **Easy Apply Helper** | LinkedIn Easy Apply için CV auto-fill asistanı | ⭐⭐⭐⭐ (4/5) | Düşük |
| **Maaş Tahmini** | İlan metninden veya benzer ilanlardan maaş skalası tahmini | ⭐⭐⭐ (3/5) | Orta |
| **Market Analytics** | Sektörel trend raporları (Hangi tech daha popüler vb.) | ⭐⭐⭐ (3/5) | Düşük |

### v1.0 — Tam Otonom Asistan

| Özellik | Açıklama | Zorluk | Öncelik |
|---------|----------|--------|---------|
| **End-to-End Pipe** | Tara → Skorla → Başvur → Takip et → Bildir (Tam Otonom) | ⭐⭐⭐⭐⭐ (5/5) | Kritik |
| **A/B Test Engine** | Hangi ön yazı/başvuru metodunun daha çok dönüt aldığı analizi | ⭐⭐⭐ (3/5) | Düşük |
| **Multi-User / DB** | Yerel dosyadan PostgreSQL/Cloud veritabanına geçiş | ⭐⭐⭐⭐ (4/5) | Düşük |

---

## 📌 Proje Durumu

```
Versiyon  : v0.6.5
Kaynaklar : LinkedIn + JSearch + RSS (+ Kariyer.net hazır)
Skor      : NLP (TF-IDF) + Hybrid Regex + Pydantic Validation
Yetenek   : Junior / Game Dev pozisyonları için optimize edildi
```

### 🧠 Akıllı Filtreleme Detayları

1.  **Dil Bariyeri:** Sistem İngilizce (`en`) ve Türkçe (`tr`) harici dillerdeki ilanları otomatik tespit eder ve lokasyonu **"dead"** yapar (-10 Puan).
2.  **Öncelik Kuralları:** Ankara, GameDev ve Junior fırsatları için özel regex + TF-IDF takviyesi ile puanlama yapılır.
3.  **Otomasyon:** İlanlar çekilip tabloya yazıldıktan hemen sonra **Tabloyu Düzelt** fonksiyonu otomatik çalışır.
