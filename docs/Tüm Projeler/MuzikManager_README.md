# Opus Music Library Manager & Studio Audio Pipeline

Bu proje, müzik arşivini en yüksek ses kalitesi ve titiz metadata disipliniyle yöneten; parçaları **48 kHz Opus (192 kbps)** formatında stüdyo sesleri, **1000x1000 piksel** albüm kapakları ve standardize edilmiş etiketlerle senkronize eden profesyonel bir müzik yönetim ve indirme sistemidir.

---

## 🌟 Çekirdek Standartlar ve Özellikler

### 1. 🎵 Yüksek Kaliteli Ses ve Stüdyo Doğruluğu
* **Saf 48 kHz Opus:** YouTube ve resmi kaynaklardan doğrudan çekilen veya kayıpsız ffmpeg ile 48.000 Hz stereo 192 kbps Opus formatına dönüştürülen ses akışları.
* **Tam Stüdyo Kayıtları:** Klip introsu, video diyalogları veya skeç sesleri içeren video sesleri elenmiş; doğrudan plak şirketleri ("Provided to YouTube by...") ve resmi stüdyo master akışları kullanılmıştır.
* **Tam Süre Doğrulaması:** Anime açılış/kapanışlarında 1-1.5 dakikalık kısa "TV-size" sürümler yerine 3-5 dakikalık tam stüdyo parçaları tercih edilmiştir.
* **Loop / Uzatılmış Sürüm Temizliği:** 10-30 dakikalık döngü (loop) dosyaları elenerek parçaların orijinal stüdyo süreleri konumlandırılmıştır.
* **Ses Seviyesi (Loudness) Dengesi:** Kısık sesli parçalar ffmpeg `volumedetect` ile taranarak stüdyo standartlarında (-12 dB ~ -14 dB ortalama ses, 0 dB peak) normalleştirilmiştir.

### 2. 🎨 Kapak Sanatı (Artwork)
* Her parçanın içerisine Deezer ve Apple Music API üzerinden çekilen orijinal **1000x1000 piksel** yüksek çözünürlüklü kare albüm kapakları VorbisComment `metadata_block_picture` (FLAC Picture formatı) olarak gömülmüştür.

### 3. 🏷️ Cerrahi Dosya İsimlendirme Kuralları
* **Standart Şablon:** `[Sanatçı] - [Şarkı İsmi] [(feat. Sanatçı)].opus`
* **Sürüm Eklerinin Ayıklanması:** Dosya adlarında bulunan gereksiz `(Remastered)`, `(2023 Remaster)`, `(Live...)`, `(Edit)` gibi ekler cerrahi olarak temizlenmiş; ancak şarkının resmi adına dahil olan remiks ve `(feat. ...)` bilgileri korunmuştur.
* Şarkı içi Vorbis `title` etiketleri ile dosya adları kusursuz senkronize tutulmuştur.

### 4. 🗂️ Akıllı Albüm Metadata Disiplini
* **Tekil / İkili Şarkılar:** Kütüphanede yalnızca 1 veya 2 parçası bulunan sanatçı/albüm kayıtlarının `album` etiketi temizlenmiştir (kütüphane oynatıcılarında binlerce tek şarkılık gereksiz albüm listesi oluşması engellenmiştir).
* **Gerçek Stüdyo Albümleri:** Kütüphanede 3 veya daha fazla şarkısı bulunan stüdyo albümleri (Pink Floyd, Radiohead, Eminem, Red Hot Chili Peppers vb.) albüm adı ve orijinal kapaklarıyla eksiksiz korunmuştur.

---

## 📊 Kütüphane Durumu ve İstatistikler

* **Konum:** `C:\Users\taycore\Music`
* **Toplam Opus Parça Sayısı:** 1.623 adet
* **Toplam Klasör Sayısı:** 67 adet
* **Kapak Görseli Korunan Şarkılar:** %100 (1000x1000 JPEG)
* **Özel Koleksiyon Klasörleri:**
  * `Themes`: Film, dizi ve ikonik oyun müzikleri (The Last Waltz, Blade, Evil Morty, FTL vb.)
  * `Anime Openings`: Full anime açılış ve kapanışları (One Piece, Naruto, Death Note vb.)
  * `Sift Heads`: Flash oyun serisi orijinal soundtrack koleksiyonu
  * `Attack on Titan`, `Fallout`, `Ghost in the Shell`, `Hotline Miami`, `Welcome to NHK`, `Mehter` vb.

---

## 📁 Proje Dizin Yapısı

```text
c:\Projeler\Music Olayı\
├── config.py           # Dizin yolları, FFmpeg/Node yolları ve YouTube ayarları
├── catalog.py          # Kütüphane tarama, katalog oluşturma ve eşleştirme
├── downloader.py       # yt-dlp tabanlı güvenli indirme ve dönüştürme motoru
├── metadata.py         # Deezer/iTunes API entegrasyonu ve mutagen etiketleme
├── main.py             # CLI komut arayüzü
├── data/
│   ├── catalog.json    # Parça eşleştirmeleri ve indirme durumu veritabanı
│   ├── cache/          # Geçici indirme ve önbellek dosyaları
│   └── covers/         # İndirilen yüksek çözünürlüklü kapaklar
└── README.md           # Proje dokümantasyonu
```

---

## 🚀 Komutlar ve Kullanım

```powershell
# 1. Kütüphaneyi tara ve kataloğu güncelle
python main.py scan

# 2. Deneme amaçlı 5 parça indir ve etiketle
python main.py test 5

# 3. İndirme ve senkronizasyon sürecini başlat
python main.py run

# 4. Belirli bir kota ile çalıştır (ör. 50 şarkı)
python main.py run --limit 50

# 5. Kütüphane istatistiklerini ve ilerlemeyi gör
python main.py stats

# 6. Hata veren / eksik kalan parçaları yeniden dene
python main.py run --retry-failed
```

---

## 🛡️ Çalışma Anı ve Güvenlik Mekanizmaları

* **Edge Browser Cookies & Node.js EJS Runtime:** YouTube bot engellerini ve "Sign in to confirm you're not a bot" uyarılarını aşmak için oturum çerezleri ve JavaScript yorumlayıcısı ile entegre çalışır.
* **Kesinti Koruması (Checkpoints):** İndirilen ve dönüştürülen her parça anında doğrulanır; işlem yarıda kalsa bile `catalog.json` sayesinde kaldığı yerden güvenle devam eder.
* **Winamp & Süreç Kilidi Koruması:** Oynatıcılar tarafından açık tutulan dosyalarda çökmeyi önleyen güvenli geçici dosya takas (atomic file swap) mekanizması bulunur.
