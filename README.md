# 🎯 Job Radar v0.9

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-Chromium-green?logo=playwright)](https://playwright.dev/)
[![Gemini API](https://img.shields.io/badge/Google%20Gemini-AI%20Powered-orange?logo=google)](https://ai.google.dev/)
[![Status](https://img.shields.io/badge/Status-Active-success)](https://github.com/taylan1477/Job-Radar)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![Clean Code](https://img.shields.io/badge/Clean%20Code-Showcase-blueviolet)](src/utils/showcase.py)

**Job Radar**, yazılım ve GameDev odaklı iş ilanlarını **4 farklı kaynaktan** (LinkedIn, JSearch, RSS, Kariyer.net) toplayan, hibrit **NLP + kural tabanlı skorlama** motoruyla filtreleyen, Google Sheets üzerinde canlı takip eden ve **LinkedIn Easy Apply** ile **İK E-Posta** kanallarından uçtan uca **otonom başvuru & geri dönüş takibi** yapan yeni nesil bir kariyer otomasyon sistemidir.

> [!TIP]
> Bu proje yalnızca bir iş arama aracı değil; **Clean Code**, **SOLID prensipleri**, **Savunmacı Programlama (Defensive Engineering)** ve **Headless/Interactive Tarayıcı Otomasyonu** standartlarını sergileyen kapsamlı bir mühendislik çalışmasıdır.

---

## 🚀 Öne Çıkan Yetenekler

### 1. 📡 Çok Kaynaklı İlan Madenciliği (Multi-Source Scraping)
* **LinkedIn Scraper:** Playwright ile dinamik DOM taraması, oturumsuz hızlı scraping ve Easy Apply etiket tespiti.
* **JSearch API:** RapidAPI REST istemcisi ile küresel yazılım fırsatları.
* **RSS Feeds:** WeWorkRemotely ve Himalayas üzerinden remote ilan taraması.
* **Kariyer.net Scraper:** Yerel pazar için stealth modunda Playwright entegrasyonu.

### 2. 🎯 Hibrit NLP Skorlama & Platform Ağırlığı
* **NLP & Regex Motoru:** `TF-IDF` ve anlamsal kelime analiziyle ilanları teknoloji alanı, lokasyon ve seviyeye (Junior/Mid/Senior) göre puanlar.
* **Platform Önceliği:** Doğrudan Easy Apply imkanı sunan LinkedIn ilanlarına `+1.0` bonus, harici kariyer portallarına (kariyer.net, aggregators vb.) otomatik `-1.0` ceza uygulanır.
* **Dil & Vize Bariyeri:** Yabancı dildeki (İngilizce/Türkçe harici) veya vize kısıtlı ilanlar tespit edilerek elenir.

### 3. 🤖 LinkedIn Easy Apply Otomasyonu (Playwright)
* **Kalıcı Oturum:** `linkedin_state.json` ile tek seferlik giriş ve güvenli cookie oturum yönetimi.
* **Dinamik DOM Çıkarımı:** Obfuscated (karmaşık) LinkedIn CSS sınıflarına takılmayan semantik etiketleme (`_extract_label`).
* **Akıllı Form Yanıtlayıcı:**
  * **Yetkinlik Yılları (Sıfır Engeli):** Bilinen yetkinliklerde (SQL: 3, C#: 3, Unity: 3, Python: 3, .NET Core: 1) tam değer; profil dışı yabancı konularda `1`. **Asla 0 girilmez.**
  * **Maaş Beklentisi:** Sayısal format hatası ve `"Evet"` yanıtını önleyen otomatik `35000` (TL) ve döviz optimizasyonu.
  * **Yabancı Dil Soruları:** Çince, Fransızca vb. bilmediği dillerde otomatik `"None"` / `"Yok"` seçimi.
  * **Ülke Kodu Koruması:** LinkedIn'in seçtiği `Turkey (+90)` değerini korur, alfabetik Andorra gibi hatalı seçimleri engeller.
* **Feed Temizleme (Follow Uncheck):** Şirketlerin takipçi kazanmak için varsayılan seçtiği *"Sayfasından haber almak için takip edin"* kutucuğunun tikini otomatik kaldırarak LinkedIn ana sayfanızın çöplüğe dönmesini engeller.
* **Human-in-the-Loop & Kota:** Oturum başına maks 15 başvuru güvenlik kotası ve son gönderme adımında kullanıcı onayı.

### 4. ✉️ İK E-Posta Başvuru Motoru
* İlan detaylarından İK e-postalarını otomatik regex ve NLP ile ayıklar.
* Google Gemini API ile pozisyona ve adayın profiline özel kişiselleştirilmiş **Cover Letter (Ön Yazı)** üretir.
* SMTP üzerinden CV (`cv.pdf`) ekli e-postayı onayınızla iletir.

### 5. 📬 Gmail IMAP Entegrasyonu & Geri Dönüş Takibi
* Gelen kutusundaki şirket geri bildirimlerini periyodik olarak tarar.
* **Hibrit E-posta Sınıflandırıcı:** Gemini LLM ve regex kuralları ile ret (`Reddedildi`), mülakat daveti (`Görüşmede`) veya otomatik yanıtları sınıflandırır.
* Google Sheets tablosundaki ilgili ilanın **Durum** sütununu anlık günceller.

### 6. 📊 Dinamik Google Sheets Yönetimi
* Koşullu biçimlendirme ile başvuru durumuna göre satır renklendirme (Reddedildi=Kırmızı, Görüşmede=Yeşil, Başvuruldu=Mavi vb.).
* Google Sheets **Smart Chips (Akıllı Açılır Menü)** ve otomatik tarih/format doğrulama.

---

## 📂 Proje Mimarisi

```text
job-radar/
├── src/
│   ├── core/                       # Çekirdek İş Mantığı & AI Modelleri
│   │   ├── application_generator.py # Form soruları yanıtlama, Cover Letter & LLM motoru
│   │   ├── email_classifier.py      # Ret/Mülakat e-postası sınıflandırma servisi
│   │   ├── models.py                # Pydantic veri modelleri ve Enum tipleri
│   │   ├── nlp_processor.py         # Metin temizleme, dil tespiti ve TF-IDF
│   │   ├── scorer.py                # Regex + NLP tabanlı ilan puanlama algoritması
│   │   └── scoring_service.py       # Puanlama servis katmanı (Clean Code Showcase)
│   ├── clients/                    # Dış Servisler, Botlar ve Entegrasyonlar
│   │   ├── easy_apply_client.py     # LinkedIn Easy Apply Playwright otomasyon istemcisi
│   │   ├── email_client.py          # SMTP üzerinden CV ekli e-posta başvuru istemcisi
│   │   ├── gmail_tracker.py         # IMAP ile Gmail gelen kutusu takipçisi
│   │   ├── jsearch_client.py        # JSearch REST API istemcisi
│   │   ├── kariyer_scraper.py       # Kariyer.net Playwright scraper
│   │   ├── linkedin_scraper.py      # LinkedIn Playwright scraper
│   │   ├── rss_sources.py           # WeWorkRemotely & Himalayas RSS istemcisi
│   │   └── sheets_client.py         # Google Sheets API (gspread) okuma/yazma/onarma
│   └── utils/                      # Yardımcı Araçlar ve Yapılandırma
│       ├── config.py                # Puan katsayıları, dosya yolları ve ortam değişkenleri
│       ├── corpus.py                # NLP stop-words ve kelime havuzu
│       ├── logger.py                # Merkezi ve renkli loglama altyapısı
│       ├── text_norm.py             # Türkçe karakter ve Unicode metin normalizasyonu
│       ├── analyze_keywords.py      # İlan metinleri kelime frekans analizörü
│       └── showcase.py              # SOLID ve Clean Code sunum aracı
├── tests/                          # Kapsamlı Pytest Birim Test Paketi (26 test)
│   ├── test_easy_apply.py           # Form yanıtlama, dil, maaş ve deneyim testleri
│   ├── test_email_classifier.py     # E-posta sınıflandırma testleri
│   ├── test_email_client.py         # E-posta gönderim ve ek testleri
│   ├── test_scorer.py               # Platform bonus/ceza ve puan testleri
│   └── ...
├── docs/                           # Proje sunumları ve yardımcı belgeler
├── cv_profile.yaml                 # Aday CV profili, yetkinlik yılları, dil ve maaş tercihleri
├── cv.pdf                          # Başvurularda otomatik eklenen güncel özgeçmiş
├── main.py                         # Merkezi terminal orkestrasyon arayüzü
├── requirements.txt                # Python bağımlılıkları
└── README.md                       # Proje dokümantasyonu
```

---

## 🖥 Kurulum

### 1. Gereksinimler
* Python 3.10 veya üzeri
* Google Cloud Console Servis Hesabı (`credentials.json` - Google Sheets API erişimi için)
* Google Gemini API Anahtarı (Opsiyonel ancak AI ön yazı ve akıllı sınıflandırma için önerilir)

### 2. Adım Adım Kurulum

```bash
# 1. Depoyu klonlayın
git clone https://github.com/taylan1477/Job-Radar.git
cd Job-Radar

# 2. Sanal ortamı oluşturun ve aktif edin
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 3. Bağımlılıkları yükleyin
pip install -r requirements.txt

# 4. Playwright Chromium tarayıcısını kurun
playwright install chromium
```

### 3. Yapılandırma (`.env` & `cv_profile.yaml`)

Proje kök dizininde `.env` dosyasını oluşturun:

```env
# Google Sheets
SPREADSHEET_ID=your_google_sheet_id_here

# AI / LLM
GEMINI_API_KEY=your_gemini_api_key_here

# E-Posta Başvurusu & IMAP Takip (Opsiyonel)
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_specific_password_here
IMAP_SERVER=imap.gmail.com
SMTP_SERVER=smtp.gmail.com
```

Özgeçmiş bilgilerinizi ve başvuru tercihlerinizi [`cv_profile.yaml`](file:///c:/Projeler/PycharmProjects/job-radar/cv_profile.yaml) dosyasından düzenleyin:
* Yetkinlik deneyim yılları (SQL: 3, C#: 3, .NET Core: 1 vb.)
* Maaş beklentisi (`salary_expectation: "35000"`)
* Konuşma dilleri ve vize/ikamet tercihleri

---

## ▶️ Kullanım & Menü Yapısı

Uygulamayı başlatmak için:

```bash
python main.py
```

Merkezi terminal arayüzü sizi karşılar:

```text
=======================================================
  Job Radar v0.9 - Otonom Başvuru & Takip Sistemi
=======================================================

  [TARAMA & VERİ]
  1. Tam çalıştır (Tüm kaynakları tara -> Sheets'e yaz)
  2. Temiz çalıştır (SİL + Tüm kaynakları tara)
  3. API'siz çalıştır (LinkedIn + RSS, JSearch yok)
  4. Sadece API (JSearch)
  5. Dry Run (Konsola yazdır, Sheets'e yazma)
  6. Tabloyu Düzelt (Başlık/Sütun/Tarih/Smart Chips)

  [OTONOM BAŞVURU & TAKİP]
  7. LinkedIn Oturumu Aç (Tek seferlik session kaydet)
  8. Otonom Başvuru Yap (Easy Apply + E-Posta | Onaylı)
  9. E-posta Yanıtlarını Kontrol Et (Gmail IMAP Sync)
  10. Çıkış
```

### 🌟 Önerilen İş Akışı

1. **LinkedIn Girişi (Menü 7):** İlk çalıştırmada açılan Chromium penceresinde LinkedIn hesabınıza giriş yapın. Oturumunuz `linkedin_state.json` olarak şifreli kaydedilir; bir daha şifre sormaz.
2. **İlanları Tarayın (Menü 3):** API harcamadan LinkedIn ve RSS kaynaklarından yüzlerce güncel ilanı çeker ve Sheets tablonuza işler.
3. **Otonom Başvuru (Menü 8):**
   * Skor aralığını belirleyin (Örn: `2.5 - 10.0`).
   * Kanal seçin (1: Tümü, 2: Sadece LinkedIn Easy Apply, 3: Sadece E-Posta).
   * Bot formları profilinize göre eksiksiz doldurur, şirketi takip etme tikini kaldırır ve son adımda ekranı size gösterip onayınızı alarak başvuruyu gönderir.
4. **Sonuç Takibi (Menü 9):** Gün sonunda Gmail gelen kutunuzu tarayarak gelen ret veya mülakat e-postalarını tespit eder ve tablodaki durumları otomatik günceller.

---

## 📊 Skorlama Algoritması

Puanlama sistemi adayın kariyer hedeflerine göre ağırlıklandırılmıştır:

$$\text{Toplam Skor} = (\text{Alan} \times 0.3) + (\text{Lokasyon} \times 0.4) + (\text{Level} \times 0.3) + \text{Platform Bonusu/Cezası}$$

| Alan | Puan | Lokasyon | Puan | Seviye (Level) | Puan | Platform Faktörü | Puan |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **gamedev** | +5.0 | **ankara** | +5.0 | **junior / entry**| +5.0 | **LinkedIn İlanı** | **+1.0** |
| **c# / unity**| +4.0 | **remote** | +5.0 | **mid** | +2.0 | **Harici Platform** | **-1.0** |
| **c++ / python**| +4.0 | **hybrid_ankara**| +5.0 | **senior** | -10.0 | **Dil Bariyeri** | -10.0 |
| **yazılım** | +2.0 | **türkiye** | +3.0 | **lead / manager**| -15.0 | | |

---

## 🧪 Testler ve Kod Kalitesi

Proje, 26 adet kapsamlı Pytest birim testi ile korunmaktadır. Form soru yanıtlayıcı, dil bariyeri, maaş optimizasyonu ve platform skorlama mantığı sürekli test edilir:

```bash
python -m pytest tests/
```

```text
tests\test_easy_apply.py ......          [ 23%]
tests\test_email_classifier.py .....     [ 42%]
tests\test_email_client.py ...           [ 53%]
tests\test_lang.py .                     [ 57%]
tests\test_scorer.py ..                  [ 65%]
tests\test_scoring_service.py .........  [100%]
====================== 26 passed in 3.27s ======================
```

---

## 🗺 Geliştirme Yol Haritası (Roadmap)

- [x] **v0.7: Veri Madenciliği & NLP Skorlama** (LinkedIn, JSearch, RSS, Google Sheets Entegrasyonu)
- [x] **v0.8: LinkedIn Easy Apply & Çift Kanallı Başvuru** (Playwright session, dinamik form doldurma, güvenlik kotası)
- [x] **v0.9: Feedback Loop & AI Destekli Geri Dönüş Takibi** (Gmail IMAP sync, Gemini LLM ret/mülakat sınıflandırma)
- [ ] **v1.0: End-to-End Headless Daemon** (Zamanlanmış otonom tarama, A/B Cover Letter başarı analizi ve Cloud Dashboard)

---

## 📄 Lisans

Bu proje [MIT Lisansı](LICENSE) kapsamında açık kaynak olarak sunulmuştur.
Kişisel kariyer otomasyonu ve portfolyo sunumu amacıyla geliştirilmiştir.
