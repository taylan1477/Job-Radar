# 🎯 Master CV & Kariyer Profili (Master Profile)

> **Not:** Bu dosya senin tüm ham kariyer verilerinin, 11 teknik projendeki mimari detayların ve sektörel anahtar kelimelerinin **tek gerçek kaynağıdır (Single Source of Truth)**. Buradaki veriler asla silinmez; CV oluştururken hedeflenen sektöre göre buradan cerrahi olarak çekilir.

---

## 1. 👤 Kişisel Bilgiler & İletişim

* **Ad Soyad:** Taylan Özgür Özdemir
* **Unvan / Rol Seçenekleri:**
  * *Rol A (Game/Sim):* Game Developer & Simulation Systems Engineer
  * *Rol B (Automation/AI):* Software Engineer — Automation, AI & Systems
  * *Rol C (Core Software):* Software Engineer (C# / Java & Media Systems)
* **E-posta:** taylan147701@gmail.com
* **Telefon:** +90 541 262 3184
* **Konum:** Ankara, Türkiye (Açık: Yerinde / Hibrit / Remote)
* **Askerlik Durumu:** Muaf / Tamamlandı
* **Sürücü Belgesi:** B

---

## 2. 🌐 Linkler & Portfolyo

* **LinkedIn:** [linkedin.com/in/taylan1477](https://linkedin.com/in/taylan1477)
* **GitHub:** [github.com/taylan1477](https://github.com/taylan1477)
* **Portfolyo / Proje Deposu:** [github.com/taylan1477/Job-Radar](https://github.com/taylan1477/Job-Radar)

---

## 3. 🎓 Eğitim Bilgileri

* **Üniversite:** İnönü Üniversitesi
* **Bölüm:** Bilgisayar Mühendisliği (Computer Engineering)
* **Tarihler:** Eylül 2021 – Haziran 2025
* **Not Ortalaması (GPA):** 3.09 / 4.00
* **Öne Çıkan Alanlar:** Veri Yapıları ve Algoritmalar, Nesne Yönelimli Programlama (OOP), Bilgisayarlı Görü (Computer Vision), Dağıtık Sistemler, İşletim Sistemleri

---

## 4. 💼 Profesyonel İş Deneyimi

### Game Developer — SoloRota
* **Çalışma Türü:** Tam Zamanlı
* **Konum:** Ankara (Yerinde)
* **Tarih:** Temmuz 2025 – Ocak 2026 (6 Ay)
* **Kullanılan Teknolojiler:** Unity (2D/3D), C#, REST APIs, Git, Android SDK, iOS Xcode, Profiler
* **Geliştirilen Ürünler:** 7 Farklı Eğitici Mobil Oyun (Android & iOS)
* **Mühendislik Katkıları & Çözülen Problemler (Google X-Y-Z Formatında):**
  * **Çekirdek Mekanikler & Mimari:** 7 farklı eğitici mobil oyunun prototipten yayın aşamasına kadar olan temel oynanış döngülerini (core gameplay loops), state machine yapılarını ve UI/UX sistemlerini C# ile inşa etti.
  * **Veri & API Entegrasyonu:** Oyun içi dinamik soru-cevap ve içerik akışını harici SoloRota REST API servisleri üzerinden asenkron olarak çeken, JSON serileştirme ve hata toleranslı veri katmanını tasarladı.
  * **Performans Optimizasyonu:** Unity Profiler ve Frame Debugger kullanarak bellek sızıntılarını (memory leaks), draw call'ları ve GC yükünü optimize etti; orta segment Android cihazlarda akıcı 60 FPS stabilizasyonu sağladı.
  * **Modüler Ekonomi & Buff Sistemi:** `ScriptableObject` mimarisiyle kod bağımlılığını en aza indiren modüler ilerleme, çarpan ve kalıcı kayıt (persistence) altyapısını kurdu.

---

## 5. 🚀 11 Teknik Projenin Derinlemesine Dökümü (Master Proje Havuzu)

---

### [Proje 1] AEGIS FORGE — Taktiksel Arazi Dönüştürme Çok Oyunculu Nişancı Oyunu
* **Teknolojiler:** Unity, C#, Hybrid Architecture (OOP + DOP/DOTS), Unity Job System, Burst Compiler, `NativeArray`, FishNet, Linux Headless Dedicated Server.
* **Hedef Sektörler:** Savunma Sanayii (Simülasyon / Taktik Modelleme), Oyun Stüdyoları, Sistem Entegrasyonu.
* **Mühendislik & Mimari Detayları:**
  * **Hibrit OOP + DOP Mimarisi:** Oyun durum makinesi ve yetenekleri esnek OOP ile kurarken; binlerce arazi hücresini CPU cache dostu `NativeArray` dizilerinde saklayarak Data-Oriented (DOP) prensipleriyle yönetti.
  * **Çok Çekirdekli Hesaplama (Multi-threading):** Arazi deformasyonu ve yükseklik simülasyonunu Unity C# Job System ve Burst Compiler ile vektörize makine koduna dönüştürerek 10.000+ tile modifikasyonunda alt-milisaniye işlem süresi yakaladı.
  * **Deterministik Event Sourcing (Headless Linux):** Ağ yükünü minimize etmek için ham mesh senkronizasyonu yerine deterministik `TerrainEvent` mimarisi kurdu; komutlar Linux Dedicated Server üzerinde doğrulanıp istemcilere broadcast edilerek yerel re-simulation ile senkronize edildi.

---

### [Proje 2] MassVideoCutter (MassVCutter) — Toplu Akıllı Video Kırpma & Masaüstü Analiz Paketi
* **Teknolojiler:** Java 23, JavaFX 23, Spring Boot 4, PostgreSQL 15, Flyway, FFmpeg / FFprobe, Multi-threading.
* **Hedef Sektörler:** Medya & Streaming, Kurumsal Masaüstü Yazılım, Masaüstü/Backend Mühendisliği.
* **Mühendislik & Mimari Detayları:**
  * **Asenkron FFmpeg Boru Hattı:** Dizi ve video arşivlerinden intro/outro bölümlerini ayıklamak için FFmpeg CLI wrapper mimarisi ve Java multi-threading iş parçacığı yöneticisi geliştirdi.
  * **Akıllı Ses Analizi (`astats`):** Ses frekansı ve desibel dalgalanmalarını (`VolumeAnalyzer`, `AudioAnalyzer`) analiz ederek video başı/sonu jeneriklerini otomatik tespit eden algoritmalar kurdu.
  * **Tasarım Kalıpları:** Genişletilebilir kırpma yöntemleri için `Strategy` ve karmaşık video analiz akışını soyutlamak için `Facade` tasarım desenlerini uyguladı.
  * **TrimDB Veritabanı:** Spring Boot 4 ve PostgreSQL ile toplu kırpma tariflerini (.trimrecipe) bulutta paylaşan ve derecelendiren REST API servisi entegre etti.

---

### [Proje 3] CineNode — Sıfır Donanımsal Transcode (Direct Play) 4K Medya Sunucusu & Botu
* **Teknolojiler:** Python, Docker, Telegram Bot API, Plex Media Server, qBittorrent-nox, Radarr, Prowlarr, Linux/Windows.
* **Hedef Sektörler:** Sistem & Altyapı Yönetimi, NOC Mühendisliği, SRE, Medya & Dağıtık Sistemler.
* **Mühendislik & Mimari Detayları:**
  * **Sıfır Transcode (Direct Play) Politikası:** Donanım maliyetini ve CPU yükünü ortadan kaldıran, kullanıcı bant genişliğini zaman paylaşımı (Time-Sharing) ve cron scheduler ile dengeleyen medya akış mimarisi tasarladı.
  * **%25 Swarm Seeder Analiz Motoru:** Torrent takipçilerindeki aktif eşleri gerçekçi modelleyen (`eff_seeders = round(seeders * 0.25)`) formül geliştirerek ölü ve bant genişliğini tıkayan indirmeleri engelleyen otomatik koruma mekanizması kurdu.
  * **Dockerized Servis Kümesi:** Plex, qBittorrent, Radarr ve Prowlarr servislerini izole Docker konteynerleri olarak yapılandırıp tek merkezden Telegram Botu ile otomatize etti (canlı hız, anlık iptal, disk temizliği).

---

### [Proje 4] Job-Radar — Otonom İş Arama, Web Kazıma & Puanlama Motoru
* **Teknolojiler:** Python, Playwright, Selenium, Pydantic, Scikit-learn, Google Sheets API, Excel.
* **Hedef Sektörler:** Web Scraping / Veri Madenciliği, E-Ticaret, Otomasyon & Süreç Mühendisliği.
* **Mühendislik & Mimari Detayları:**
  * **Anti-Bot & Dinamik DOM Kazıma:** LinkedIn ve iş portallarındaki dinamik tek sayfa uygulamalarını (SPA) Playwright ile simüle eden, bot tespitlerini ve hız limitlerini yöneten robust web kazıma motoru inşa etti.
  * **Akıllı Puanlama & Eşleştirme:** İlan metinlerini TF-IDF / NLP filtreleriyle aday profilinin yetkinlik matrisiyle kıyaslayan, alakasız ilanları eleyen deterministik puanlama algoritması tasarladı.
  * **Otomatik Başvuru & Tablo Entegrasyonu:** Taranan verileri Pydantic şemaları ile doğrulayıp Google Sheets ve Excel üzerinde otomatik sınıflandıran ve başvuru süreçlerini izleyen boru hattı geliştirdi.

---

### [Proje 5] VoiceOS (Jarvis) — Çevrimdışı Otonom Sesli İşletim Sistemi Ajanı
* **Teknolojiler:** Python, Ollama (Qwen 2.5 7B, LLaVA 7B), Faster-Whisper, Edge-TTS, SAPI5, AutoHotkey v2, Graphify.
* **Hedef Sektörler:** Yapay Zeka Mühendisliği, Masaüstü Otomasyonu, Sistem Entegrasyonu.
* **Mühendislik & Mimari Detayları:**
  * **%100 Yerel / Çevrimdışı Edge AI:** Bulut bağımlılığı olmadan, GPU üzerinde kuantize LLM ve Faster-Whisper (INT8) çalıştırarak sıfır veri sızıntılı sesli asistan mimarisi geliştirdi.
  * **Hibrit Çift-Yapay Zeka Görsel Analiz (Dual-Vision):** LLaVA ile ekran görüntüsü piksellerini analiz edip Qwen ile doğal dilde özetleyen masaüstü kontrol yeteneği sağladı.
  * **Interrupt-Destekli Ses Motoru:** Kullanıcı konuşmaya başladığı anda çalan sesi milisaniyeler içinde kesen (barge-in / interrupt) asenkron STT/TTS döngüsü kurdu.
  * **Deterministik AST Kod Grafiği:** Kod tabanının mimarisini ve çağrı zincirlerini Graphify ile haritalayarak otonom modül çağırma güvenliği sağladı.

---

### [Proje 6] AgentSwarm (Project Jarvis Dev Swarm) — Çok Ajanlı Otonom Geliştirme Platformu
* **Teknolojiler:** Gemini 3.1 Pro via AI Studio, WSL2 (Ubuntu 24.04), Docker, PostgreSQL, Model Context Protocol (MCP), JetBrains Rider, AHK v2.
* **Hedef Sektörler:** AI Platform Mühendisliği, DevOps, Yazılım Araçları & Altyapı.
* **Mühendislik & Mimari Detayları:**
  * **Çok Ajanlı (Multi-Agent) Paralel Yürütme:** JetBrains Rider kokpiti altında, WSL2 üzerinde çalışan izole CLI worker ajanlarını (tmux) Gemini 3.1 Pro ile orkestre etti.
  * **Model Context Protocol (MCP) Bellek Katmanı:** Dockerize edilmiş yerel PostgreSQL üzerinde çalışan özel bir Python MCP sunucusu geliştirerek ajanlar arası ortak bellek ve kronolojik bağlam senkronizasyonu kurdu.
  * **Masaüstü Entegrasyonu:** Windows - WSL2 arası komut ve prompt enjeksiyonunu AutoHotkey v2 betikleriyle hızlandırdı.

---

### [Proje 7] KidneySegmentation — Medikal BT Görüntü Segmentasyonu (Klasik CV vs Derin Öğrenme)
* **Teknolojiler:** Python, PyTorch, OpenCV, ScaleNorm-UNet, BRISQUE, AMOS Dataset, Google Colab.
* **Hedef Sektörler:** Bilgisayarlı Görü (Computer Vision), Biyomedikal AI, Veri Bilimi & Araştırma.
* **Mühendislik & Mimari Detayları:**
  * **Çift Yaklaşımlı Mimari:** Tıbbi CT taramalarında böbrek bölgesi tespiti için geleneksel özellik mühendisliği (SIFT, HOG, CoHOG, LBP, Sobel) ile modern derin öğrenmeyi (ScaleNorm-UNet) akademik standartlarda kıyasladı.
  * **Ön İşleme & Kalite Filtresi:** Referanssız görüntü kalite değerlendiricisi (BRISQUE) ile düşük gürültülü kesitleri otomatik filtreleyen, NL-Means ve Gamma dönüşümlü ön işleme pipeline'ı inşa etti.
  * **Piksel Düzeyinde Doğruluk:** Derin öğrenme segmentasyon modelini Dice Loss ve IoU metrikleriyle optimize ederek klinik düzeyde sınır tespiti elde etti.

---

### [Proje 8] FitConnect — Antrenör-Danışan Yönetim & Canlı Antrenman Mobil Ekosistemi
* **Teknolojiler:** React Native, Expo SDK 57, TypeScript, Supabase (PostgreSQL), Edge Functions (Deno), QR Scanning, Tanita PDF Vault.
* **Hedef Sektörler:** Mobil Yazılım Geliştirme (iOS/Android), Fullstack SaaS, Bulut Tabanlı Sistemler.
* **Mühendislik & Mimari Detayları:**
  * **Rol Tabanlı Güvenlik (RBAC & RLS):** Supabase Row Level Security ve Deno Edge Functions ile antrenör ve danışan oturumlarını izole eden, güvenli yetkilendirme katmanı kurdu.
  * **Canlı Tonaj Hesaplama Motoru:** Antrenman sırasında dinamik ağırlık/tekrar setlerinden toplam tonajı anlık hesaplayan performans izleme mekanizması geliştirdi.
  * **Dinamik Sahtecilik Önleyici QR:** Zaman damgalı anlık QR kod üretimi ve kamera okuyucusu ile antrenör-danışan seans düşümlerini milisaniyeler içinde onaylayan modül kodladı.

---

### [Proje 9] EvoluCat — 2D Metroidvania Platform Oyunu
* **Teknolojiler:** Unity 2D, C#, Hiyerarşik State Machines, JSON/Binary Serialization, Physics2D.
* **Hedef Sektörler:** Oyun Geliştirme (PC / Konsol / Indie).
* **Mühendislik & Mimari Detayları:**
  * **State Machine Karakter Kontrolörü:** Telekinezi, duvardan atlama ve bulmaca çözme gibi kompleks karakter mekaniklerini modüler ve hatasız durum makineleri ile inşa etti.
  * **Çoklu Slot Kalıcı Kayıt Sistemi (Save/Load):** Oyun durumunu, kazanılan yetenekleri ve oda geçişlerini serialize eden, veri kaybını önleyen dosya yönetim altyapısı kurdu.

---

### [Proje 10] SoloIdle — Eğitici Idle & Kampüs Yönetim Oyunu (SoloRota)
* **Teknolojiler:** Unity 2D, C#, ScriptableObjects, REST API, JSON, Android/iOS.
* **Hedef Sektörler:** Mobil Oyun Geliştirme, EdTech, Simülasyon.
* **Mühendislik & Mimari Detayları:**
  * **Matematiksel İlerleme & Çarpan Motoru:** Fakültelerin saniyelik bilgi puanı üretimini soru-cevap doğruluğuna bağlayan logaritmik çarpan algoritması tasarladı.
  * **ScriptableObject Veri Mimarisi:** Fakülte seviyelerini, bonusları ve yükseltme ağaçlarını koddan bağımsız veri konteynerleri olarak kurguladı.

---

### [Proje 11] MuzikManager — Stüdyo Standardında 48kHz Opus Ses Boru Hattı
* **Teknolojiler:** Python, FFmpeg, Opus Codec, Deezer / Apple Music REST APIs, Mutagen (VorbisComment).
* **Hedef Sektörler:** Medya & Ses Mühendisliği, Ses Veri Boru Hatları, Otomasyon.
* **Mühendislik & Mimari Detayları:**
  * **Stüdyo Kalitesinde Normalizasyon:** 1.600+ ses dosyasını kayıpsız 48 kHz stereo 192 kbps Opus formatına dönüştüren, FFmpeg `volumedetect` ile -14 dB LUFS stüdyo seviyesinde dengeleyen pipeline geliştirdi.
  * **Otomatik Metadata & Kapak Enjeksiyonu:** Deezer ve Apple Music API üzerinden 1000x1000 piksel kapakları FLAC Picture formatında VorbisComment bloklarına gömen metadata senkronizasyonu sağladı.

---

## 6. 🛠️ Teknik Yetenekler Havuzu (Kategorik & ATS Formatında)

* **Programlama Dilleri:** C#, Python, Java, C++, TypeScript/JavaScript, SQL, Bash/PowerShell
* **Oyun & Simülasyon Motorları:** Unity Engine (2D/3D), DOTS (C# Job System, Burst Compiler), Unreal Engine (Temel C++/Blueprints), FishNet, Physics
* **Masaüstü, Web & Backend:** JavaFX, Spring Boot, .NET / ASP.NET Core, React Native (Expo), Supabase, RESTful APIs, Multi-threading
* **Yapay Zeka & Bilgisayarlı Görü:** PyTorch, OpenCV, ScaleNorm-UNet, Ollama (Yerel LLM'ler), Faster-Whisper, Scikit-learn
* **Medya, Streaming & Araçlar:** FFmpeg, Docker, Git / GitHub, Linux (Ubuntu/WSL2), PostgreSQL, Playwright, AutoHotkey
