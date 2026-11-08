# 🎓 SoloIdle

> 💡 **Eğitici Idle Oyun | SoloRota tarafından geliştiriliyor**

---

## 🧩 1. Temel Bilgiler

| Özellik | Açıklama |
|----------|-----------|
| 🎮 **Oyun Adı** | SoloIdle |
| 📱 **Platformlar** | Android, iOS, WebGL |
| 👶 **Hedef Yaş** | İlkokul, Ortaokul, Lise |
| 🗣️ **Dil** | Türkçe |
| 🏢 **Marka** | SoloRota |
| 🧠 **Tür** | Idle / Incremental / Quiz |

---

## 🧠 2. Core Gameplay (Oynanış Döngüsü)

SoloIdle, klasik **kolej yönetimi** temalı bir **Idle oyunudur**.  
Oyuncu kendi üniversitesini kurar ve **fakülteler**, **bölümler** ve **öğrenci sayısı** arttıkça gelir kazanır.  
Ancak! Bu gelir sadece **soru çözüp** çarpan alarak yeterli bir miktara erişebilir. 🎯

### 🔁 Temel Döngü
1. 💰 Fakülte kur / yükselt
2. 🧮 Gelir üret
3. 🧑‍🏫 API’den gelen soruları çöz
4. ✅ Doğru cevapla gelir çarpanını artır
5. 🔓 Yeni fakülteler & bölümler aç
6. 🏛️ Üniversiteni büyüt ve efsane bir rektör ol 😎

### 🎓 Fakülte Örnekleri
- Fen-Edebiyat Fakültesi 🧪
- Mühendislik Fakültesi ⚙️
- Tıp Fakültesi 💉
- İletişim Fakültesi 🎥
- Spor Bilimleri Fakültesi 🏃
- Hukuk Fakültesi 🎓

Her fakültenin üretim oranı, upgrade sayısı ve “bilgi kalitesi” farklı olacak.

---

## 💰 3. Ekonomi & Progression

### ⚙️ Üretim Sistemi
- Her fakülte, saniye başına “bilgi puanı” üretir.
- Bu puanlar pasif olarak artar (Idle sistem).
- **Soru çözmeden üretim oranı %10**’a kadar düşer.
- **Doğru cevapladıkça x2, x4, x8 çarpan** aktif olur.

### 📊 Gelişim Aşamaları
1. **Küçük Kolej** – 1 fakülte
2. **Bölgesel Üniversite** – 3 fakülte
3. **Ulusal Üniversite** – 5 fakülte
4. **Uluslararası Kampüs** – 8+ fakülte
5. **Efsanevi Akademi** – Max seviye, global sıralama

### 🧱 Upgrade Türleri
| Tür | Açıklama |
|------|-----------|
| 🏗️ Bina Yükseltmesi | Gelir oranını artırır |
| 🧑‍🎓 Öğrenci Sayısı | Üretim hızını artırır |
| 🧠 Akademik Kadro | Soru çözme ödülünü artırır |
| ⚡ Motivasyon Boost | Geçici çarpan sağlar |

---

## 📚 4. Eğitici İçerik & API

Sorular **SoloRota API’si** üzerinden çekilir.  
Her soru:
- 4 şıklı çoktan seçmeli
- Konu, seviye ve kategoriye göre ayrılmış
- Hedef yaş grubuna göre filtrelenmiş

### 🎯 Etkileşim Sistemi
- **Doğru cevap → Çarpan artar (örnek: x2, x4, x8)**
- **Yanlış cevap → Çarpan yok**
- Soru çözmeden ilerlemek imkansız, rastgele cevaplayarak ilerlemek çok zor, **doğru cevap ödüllendirici** olacak.

---

## 🎨 5. Görsel & Atmosfer

| Kategori | Tanım |
|-----------|--------|
| 🎨 **Tarz** | Stylized Cartoon |
| 🏫 **Tema** | Kolej / Kampüs yönetimi |
| 📺 **Kamera** | Dikey |
| 🗺️ **Ana Ekran** | Etkileşilebilir kampüs haritası |
| 🎬 **Animasyon Yoğunluğu** | Orta → Yüksek (ilerleyen buildlerde) |

### 🌆 Görsel Fikir
2D kampüs haritası üzerinde:
- Fakülteler sabit binalar olarak durur
- Binaların üzerinde üretim animasyonları (ışık, baloncuk, vs.)
- Dokunarak upgrade / bilgi toplama yapılır

---

## 🧭 6. UX / UI

- 🎯 **Dikey ekran oryantasyonu**
- 🎞️ UI elementleri animasyonlu olacak
- 🧩 Tüm sistem tek sahnede yönetilecek (Canvas + Manager yapısı)
- 🪄 Navigasyon sade ama tatlı olacak

---

## 🚀 7. Hedefler & Motivasyon

🎯 **Amaç:**  
Oyuncuya *hem ilerleme hissi hem öğrenme tatmini* vermek.

### 🧠 Eğitici Motivasyonlar
- Her doğru cevapta "öğrendiğini hissettirme"
- Fakülte adlarında, bina açıklamalarında küçük mizah ve bilgi parçacıkları

### 💸 Idle Motivasyonlar
- Sürekli yükselen gelir grafiği
- “Büyük rektör olma” hissi
- Yeni fakültelerin kilidini açma tatmini

---

## 🧭 8. Uzun Vadeli Planlar

| Plan | Detay |
|------|--------|
| ☁️ Cloud Save | Hesap bazlı kayıt |
| 🏅 Global Sıralama | En bilgili rektörler listesi |
| 🎨 Karakter Sistemi | Öğrenci, profesör kartları |
| 🌐 Multiplayer Event | Bölümler arası bilgi turnuvaları |
| 🧩 Prestige Sistemi | Tüm üniversiteyi resetleyip bonuslarla yeniden başlama |

---

## ⚙️ 9. Teknik Kısım

| Alan | Detay |
|------|--------|
| 🧰 **Motor** | Unity |
| 🧩 **Template** | Universal 2D |
| 🧠 **Kodlama Dili** | C# |
| 💾 **Kayıt Sistemi** | PlayerPrefs (lokal) → Sonrasında bulut |
| 📡 **Backend / API** | SoloRota API (senkronize) |
| 📺 **Reklam** | Yok |
| 🧍 **Sahne Yapısı** | UI ve oyun state’leri tek sahnede yönetilecek |
---

## 🧾 10. Özet

🎓 SoloIdle, sadece tıklayarak büyüyen bir idle oyunu değil, eğlendirerek soru çözdüren bir öğrenme ekosistemi olacak.
Oyuncular, kendi üniversitelerini kuracak, fakülteler açacak ve bilgileriyle büyüyecekler.

---

👨‍💻 **Geliştirici:** Taylan Özgür Özdemir  
🧠 **Yayıncı / Marka:** SoloRota  
📅 **Durum:** Pre-Production  
📍 **Unity Template:** Universal 2D
