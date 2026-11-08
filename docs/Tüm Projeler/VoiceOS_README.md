# Voice OS (J.A.R.V.I.S.) ⚡🎙️

%100 Yerel, Çevrimdışı (Offline), Sansürsüz ve Otonom Windows Sesli Kontrol İşletim Sistemi Ajanı.

İnternet bağlantısına ihtiyaç duymadan, doğrudan yerel GPU ve CPU üzerinde çalışan yapay zeka modelleriyle Windows'u kontrol eder, oyunlarda ekrana bakıp tavsiye verir, müzik/film arşivinizi yönetir ve klavyenizi kullanarak ekrana yazı yazar.

---

## 🌟 Öne Çıkan Yetenekler

- **🔒 %100 Yerel ve Güvenli:** Verileriniz asla buluta gitmez. Ollama (`qwen2.5:7b` ve `llava:7b`) ile tamamen cihazınızda çalışır.
- **🎙️ Hibrit Ses Motoru (Ear & Mouth):**
  - **Kulak (STT):** `faster-whisper` (Small model, INT8 CPU optimizasyonu).
  - **Ağız (TTS):** İnternet varken kristal netliğinde `edge-tts` (AhmetNeural), internet kesildiğinde anında yerel Windows SAPI5 (`pyttsx3`) motoruna otomatik geçiş. Konuşma sırasında araya girildiğinde ses anında kesilir (Interrupt desteği).
- **👁️ Görsel Analiz (Dual-AI Vision):** Ekranda ne olduğunu inceleyip (oyun arayüzü, masaüstü, logo vb.) tek bir doğal Türkçe cümleyle açıklar (`llava:7b` + `qwen2.5:7b`).
- **🎮 Gamepad & Klavye Kısayolları:**
  - `Ctrl + A + F` veya `Ctrl + Alt + F` ile anında dinleme.
  - Gamepad üzerindeki `Joy9` (Select/Share) tuşuyla tek tıkla tetikleme.
  - Jarvis kapalıyken kısayola basıldığında PowerShell'i açıp kendini otomatik başlatma.
- **🎵 Akıllı Winamp & Medya Yönetimi:** 
  - 1600+ MP3'lük yerel arşivi indeksler, ruh haline veya sanatçıya göre anında playlist oluşturup çalar.
  - "Müziği kapat" dendiğinde anında Winamp'ı kapatır.
  - "Spiderman filmini aç" gibi komutlarda arşivdeki filmleri isim benzerliklerine göre (Fuzzy Matching) bulup oynatır.
- **⌨️ Klavye Yazı Yazdırma (Typewriter):** Mouse ile herhangi bir text alanına tıkladıktan sonra *"Merhaba dünya yaz"* dediğinizde ışık hızında metni ekrana yazar.
- **🔊 Windows Sistem Kontrolü:** Ses açma, kısma, sessize alma (mute/unmute), tüm pencereleri küçültme (Win+D).
- **🗺️ Deterministik AST Bilgi Grafı (Graphify Entegrasyonu):** Kod tabanı `graphify-out/` ve `.graphify/graph.json` ile haritalanmıştır; mimari ve çağrı zincirleri deterministik bilgi grafiği üzerinden izlenir.

---

## 📁 Proje Mimarisi

```text
Voice-OS/
├── .graphify/           # Deterministik AST çağrı grafiği (graph.json)
├── core/                # Beyin (NLP Router/LLM) ve Ses Motoru (STT/TTS)
│   ├── brain.py         # Türkçe normalizasyonlu niyet ayrıştırıcı & Ollama bağlantısı
│   └── voice_engine.py  # Faster-Whisper + Hibrit TTS (Interrupt destekli)
├── docs/                # Proje bağlamı ve yol haritası (PROJECT_CONTEXT, PLAN_SMART)
├── graphify-out/        # Görsel HTML grafiği (graph.html) ve analiz raporu (GRAPH_REPORT.md)
├── skills/              # Yetenek modülleri
│   ├── media_skill.py   # Film arşivi ve bulanık arama (Fuzzy match)
│   ├── system_skill.py  # Ses kontrolü, Win+D, klavye ile yazdırma
│   ├── vision_skill.py  # Çift LLM (Dual-AI) ekran görüntüsü analizi
│   └── winamp_skill.py  # Yerel MP3 arşivi indeksleyici ve Winamp yöneticisi
├── tests/               # STT ve ses donanımı test betikleri
├── jarvis_hotkey.ahk    # AHK v2 kısayol dinleyicisi (Klavye & Gamepad Joy9)
├── main.py              # Ana olay döngüsü, HTTP dinleyici ve ses işlem kuyruğu
├── Modelfile            # Özel Jarvis Ollama sistem promptu
├── music_index.json     # Yerel müzik kütüphanesi önbelleği
├── Jarvis.bat           # Tek tıkla tam başlatıcı (Ollama + AHK + Jarvis)
├── Jarvis_Kapat.bat     # Jarvis ve Ollama süreçlerini sonlandırıp belleği temizleme
├── Ollama_Baslat.bat    # Ollama'yı arka planda (gizli pencere) başlatma
├── Ollama_Kapat.bat     # Sadece Ollama servisini durdurma
├── README.md            # Bu belge
└── .gitignore
```

---

## 🛠️ Kurulum ve Gereksinimler

### 1. Sistem Gereksinimleri
- Windows 10 / 11 (64-bit)
- Python 3.10+
- [AutoHotkey v2](https://www.autohotkey.com/v2/)
- [Ollama for Windows](https://ollama.com/)

### 2. Gerekli Python Paketleri
```bash
pip install sounddevice numpy faster-whisper edge-tts pygame pyttsx3 pycaw pyautogui pyperclip mutagen requests graphifyy
```

### 3. Yerel Modellerin Hazırlanması
```bash
# Ollama modellerini indirin
ollama pull qwen2.5:7b
ollama pull llava:7b

# Özel Jarvis kişiliğini derleyin
ollama create jarvis -f Modelfile
```

---

## 🚀 Çalıştırma Seçenekleri

### Yöntem A: Hızlı Başlatıcı (Önerilen)
Masaüstündeki veya proje kökündeki **`Jarvis.bat`** dosyasına çift tıklayın:
1. Ollama çalışmıyorsa arka planda otomatik başlatır.
2. AHK kısayol dinleyicisini kontrol edip gerekirse devreye alır.
3. Voice OS konsolunu açar.

### Yöntem B: Manuel Başlatma
1. `Ollama_Baslat.bat` ile veya `ollama serve` komutuyla yapay zeka servisini açın.
2. `jarvis_hotkey.ahk` betiğini çalıştırın.
3. Konsoldan ana uygulamayı başlatın:
```powershell
python main.py
```

### 🛑 Kapatma & Bellek Boşaltma
İşiniz bittiğinde veya oyunlara girmeden önce RAM/VRAM'i tamamen serbest bırakmak için:
- **`Jarvis_Kapat.bat`** dosyasını çalıştırın (Ollama ve arka plan alt süreçlerini tek tıkla sonlandırır).
- Sadece Ollama'yı kapatmak isterseniz **`Ollama_Kapat.bat`** betiğini kullanabilirsiniz.

---

## 🎮 Kullanım Kılavuzu

Uygulama çalışırken:
- **Klavye:** `Ctrl + A + F` veya `Ctrl + Alt + F`
- **Gamepad:** `Joy9` (Select/Share tuşu)
- **Konsol:** `ENTER` tuşuna basarak mikrofona konuşun veya doğrudan metin yazıp `ENTER`'layın.
- **Konuşmayı Kesme (Interrupt):** Jarvis konuşurken kısayola tekrar basıldığında ses anında susar ve yeni komutu dinler.
- **Çıkış:** Konsola `q` yazıp çıkabilirsiniz.
