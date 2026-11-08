# 🫀 Medical Image Segmentation — Böbrek CT Segmentasyonu

> **Biyomedikal Yapay Zeka Projesi** | PyTorch · Computer Vision · Medical Imaging

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.x-EE4C2C?logo=pytorch)](https://pytorch.org)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-5C3EE8?logo=opencv)](https://opencv.org)
[![Platform](https://img.shields.io/badge/Platform-Google%20Colab-F9AB00?logo=googlecolab)](https://colab.research.google.com)
[![Domain](https://img.shields.io/badge/Domain-Medical%20AI-critical)](.)

---

## 🎯 Proje Özeti

Bu proje, tıbbi CT (Bilgisayarlı Tomografi) görüntülerinden böbrek bölgesini otomatik olarak segmente eden uçtan uca bir **medikal yapay zeka sistemi** geliştirmeyi hedeflemektedir.

Proje iki paralel yaklaşımı birlikte uygulayıp karşılaştırmaktadır:

| Yaklaşım | Yöntemler | Amaç |
|---|---|---|
| **Geleneksel Görüntü İşleme** | Kenar tespiti, HOG, SIFT, LBP, CoHOG | İnterpretable özellik mühendisliği |
| **Derin Öğrenme (DL)** | ScaleNorm-UNet (PyTorch) | Uçtan uca piksel düzeyinde segmentasyon |

> 💡 Her iki yaklaşımın bir arada uygulanması, akademik literatürdeki "classical vs. deep learning" karşılaştırma metodolojisini yansıtmaktadır.

---

## 🏥 Medikal Bağlam ve Motivasyon

Böbrek segmentasyonu, klinik pratikte kritik bir adımdır:
- **Tümör tespiti** ve hacim ölçümü
- **Radyasyon planlaması** öncesi organ sınır belirleme
- **Kronik böbrek hastalığı** takibinde morfometrik analiz

Bu proje, **AMOS** (*Abdominal Multi-Organ Segmentation*) ve özel **KidneySegmentation** veri setleri üzerinde geliştirilmiştir.

---

## 📁 Proje Yapısı

```
Biyomed/
│
├── Onislem.ipynb            # Veri kalitesi değerlendirme & ön işleme pipeline'ları
├── KenarDeseniKodla.ipynb   # Kenar tespiti & çok ölçekli desen kodlama
├── Modelleme.ipynb          # Özellik mühendisliği: SIFT · HOG · CoHOG · LBP
└── yapayZeka.ipynb          # ScaleNormUNet eğitimi, doğrulama & test (PyTorch)
```

---

## 🔬 Teknik Detaylar

### 1. Veri Kalitesi Değerlendirme ve Ön İşleme

**`Onislem.ipynb`**

Gerçek dünya medikal veri setleri gürültülü ve düzensiz dağılımlı görüntüler içerir. Bu aşamada standart bir **ön işleme pipeline'ı** geliştirilerek model giriş kalitesi güvence altına alınmıştır.

**Görüntü Kalitesi Değerlendirme:**
- **BRISQUE** (*Blind/Referenceless Image Spatial Quality Evaluator*) skoru ile referanssız görüntü kalite ölçümü
- En kaliteli görüntüler düşük BRISQUE skoru (~14.46) ile seçilmesi

**Ön İşleme Pipeline'ları:**

```
Pipeline 1 (Kenar-Odaklı):
  Min-Max Normalizasyon
      ↓
  Sobel Keskinleştirme        ← Yatay + Dikey gradyan
      ↓
  NL-Means / Median Denoising ← Gürültü baskılama
      ↓
  Histogram Eşitleme
      ↓
  Gamma Dönüşümü              ← Parlaklık/kontrast ayarı

Pipeline 2 (Kontrast-Odaklı):
  Unsharp Masking → Histogram Stretching → Brightness/Contrast Adjustment
```

**Öne Çıkan Teknik Katkılar:**
- Farklı pipeline kombinasyonları nesnel BRISQUE skoru ile karşılaştırıldı
- Büyük medikal veri setinde otomatik görüntü kalitesi sıralama

---

### 2. Kenar Tespiti ve Çok Ölçekli Desen Kodlama

**`KenarDeseniKodla.ipynb`**

Böbrek sınırının geometrik temsilini öğrenmek için geliştirilen desen kodlama modülüdür. MATLAB'daki `bwboundary` fonksiyonunun Python implementasyonu dahil olmak üzere özgün algoritmalar içerir.

**Eğitim Aşaması — Label Görüntüsü Üzerinde:**

| Bileşen | Yöntem | Teknik Detay |
|---|---|---|
| **Kenar Tespiti** | `bwboundary` (Python impl.) | 8-bağlantılı komşuluk, ikili dolgu |
| **Çizgi Özelliği** | `extract_lines` | 8 yönde X uzunluğunda çizgiler, açı örnekleme |
| **Patch Özelliği** | `extract_patches` | Her kenar pikselinde m×m yamalar |
| **Morfolojik Genişletme** | `dilate_boundary` | Disk yapısal element ile sınır toleransı |
| **Çok Ölçekli Temsil** | Gauss Piramidi (4 seviye) | Farklı çözünürlüklerde özellik kodlama |

**Test Aşaması:**

| Bileşen | Yöntem | Sonuç |
|---|---|---|
| Kenar çıkarım | Canny (threshold: 100/200) | Test görüntüsü kenar haritası |
| Final segmentasyon | Morfolojik genişletme (disk=2) | İkili segmentasyon maskesi |

---

### 3. Özellik Mühendisliği ve Modelleme

**`Modelleme.ipynb`** *(En kapsamlı notebook)*

Geleneksel bilgisayarlı görü literatüründen alınan birden fazla özellik tanımlayıcı sistematik biçimde uygulanmış ve karşılaştırılmıştır.

#### 3.1 Anahtar Nokta Tanımlayıcıları

| Algoritma | Özellik | Neden Karşılaştırıldı? |
|---|---|---|
| **SIFT** | Ölçek + Rotasyon değişmezliği | CT dilimleri arası ölçek farkları için |
| **ORB** | Hız-odaklı, ikili tanımlayıcı | Gerçek zamanlı uygulamalar için |
| **AKAZE** | Yerel, doğrusal olmayan | Doku değişkenliği için |

> ✅ **Sonuç:** SIFT, medikal görüntülerdeki düşük kontrastlı yapılarda en kararlı anahtar nokta eşleşmesini sağladı.

#### 3.2 Bölge Tabanlı Özellik Tanımlayıcılar

| Yöntem | Açıklama | Uygulama |
|---|---|---|
| **HOG** (Histogram of Oriented Gradients) | Gradyan yönü histogramları | Tüm görüntü patch'leri |
| **HOG-Kidney** | Sadece böbrek pikselleri | Label maskesi ile filtrelenmiş bölge |
| **CoHOG** | HOG hücreleri arası co-occurrence | Yapısal doku ilişkisi |
| **LBP + CoHOG** | LBP dönüşümünden CoHOG | Mikro-doku analizi |
| **Erosion + HOG** | Erozyon → Patch → HOG | Sınır artefaktlarını elimine eden saflaştırılmış bölge özelliği |

**Benzerlik Tabanlı Segmentasyon:**
- Eğitimde çıkarılan HOG vektörleri `.npy` formatında disk'e kaydedildi
- Test görüntüsünden alınan patch özellikleri kaydedilmiş vektörlerle Öklidyen uzaklık ile karşılaştırıldı
- Ayarlanabilir benzerlik eşiği (`similarity_threshold`) ile segmentasyon kararı

---

### 4. ScaleNormUNet — Derin Öğrenme ile Segmentasyon

**`yapayZeka.ipynb`**

**PyTorch** ile sıfırdan geliştirilen `ScaleNormUNet`, UNet mimarisine *BatchNormalization* ve *Scale Normalization* entegre eden medikal segmentasyon modelidir.

#### Mimari

```
Giriş: 512×512×3 (RGB CT dilimi)
│
├── Encoder (Aşağı Örnekleme)
│   ├── CBR Block: Conv2D → BatchNorm2D → ReLU → Conv2D → BN → ReLU
│   ├── MaxPool2D (×4)
│   └── Feature maps: 64 → 128 → 256 → 512
│
├── Bottleneck: 1024 kanal
│
├── Decoder (Yukarı Örnekleme)
│   ├── TransposedConv2D + Skip Connection (Encoder'dan)
│   └── CBR Block (×4)
│
└── Çıkış: 512×512×1 (İkili Segmentasyon Maskesi)
```

#### Eğitim Pipeline'ı

| Adım | Detay |
|---|---|
| **Veri Bölme** | %60 eğitim / %20 doğrulama / %20 test (`sklearn.train_test_split`) |
| **Normalizasyon** | Kanal bazlı ortalama-std hesaplama (veri setinden hesaplanır) |
| **Dataset Sınıfı** | `SegmentationDataset(Dataset)` — özel PyTorch Dataset implementasyonu |
| **DataLoader** | Batch tabanlı yükleme, shuffle |
| **Kayıp Fonksiyonu** | Binary Cross-Entropy |
| **Optimizer** | Adam |
| **Erken Durdurma** | `EarlyStopping` sınıfı — `patience=3`, `delta=0.0` |
| **Model Kaydetme** | `best_model.pth` — en düşük doğrulama kaybında checkpoint |

#### Değerlendirme ve Görselleştirme

- 📉 Eğitim / Doğrulama **Loss** ve **Accuracy** eğrileri
- 🏆 En iyi tahmin — en kötü tahmin karşılaştırmalı görselleştirme
- 🔍 3 rastgele test örneği: Ham Görüntü | Gerçek Maske | Tahmin Maskesi

---

## 🛠 Teknoloji Yığını

### Derin Öğrenme
| | Kütüphane | Kullanım Amacı |
|---|---|---|
| 🔴 | **PyTorch 2.x** | ScaleNormUNet modeli, eğitim/test döngüsü, GPU desteği |
| 📦 | **torchvision** | Görüntü dönüşüm pipeline'ı |
| 📊 | **scikit-learn** | Stratified veri bölme, model değerlendirme |

### Bilgisayarlı Görü & Görüntü İşleme
| | Kütüphane | Kullanım Amacı |
|---|---|---|
| 👁 | **OpenCV 4.x** | Görüntü okuma, Canny, Sobel, morfolojik operasyonlar, SIFT/ORB/AKAZE |
| 🔬 | **scikit-image 0.19.3** | HOG, LBP, Gauss piramidi, kontur tespiti, GLCM |
| 🧮 | **NumPy** | Matris işlemleri, vektör hesaplamaları |
| 📐 | **SciPy** | Morfolojik dolgu (`binary_fill_holes`) |
| 🌀 | **Shapely** | Geometrik kontur işlemleri |

### Veri Kalitesi
| | Kütüphane | Kullanım Amacı |
|---|---|---|
| 📏 | **BRISQUE** | Referanssız görüntü kalitesi değerlendirmesi |

---

## 📊 Veri Seti

| Özellik | Detay |
|---|---|
| **Kaynak 1** | AMOS — Abdominal Multi-Organ Segmentation (sol böbrek dilimleri) |
| **Kaynak 2** | KidneySegmentation — özel böbrek CT veri seti |
| **Format** | 2D PNG dilimleri (grayscale + RGB) |
| **Etiketler** | El ile oluşturulmuş ikili segmentasyon maskeleri |
| **Platform** | Google Shared Drive üzerinden Google Colab erişimi |
| **Ön işleme** | BRISQUE ile kalite filtrelemesi + çok aşamalı pipeline |

---

## 🔄 Sistem Mimarisi

```
Medikal CT Görüntü Arşivi (AMOS + KidneySegmentation)
                    │
        ┌───────────▼───────────┐
        │   Veri Kalite Filtresi │ ← BRISQUE skoru ile otomatik seçim
        │   (Onislem.ipynb)      │   ve çok aşamalı ön işleme
        └───────────┬───────────┘
                    │
      ┌─────────────┴─────────────┐
      │                           │
┌─────▼──────────────────┐  ┌────▼─────────────────────┐
│  Geleneksel CV Pipeline │  │  Derin Öğrenme Pipeline   │
│                        │  │                           │
│  Kenar Tespiti         │  │  ScaleNormUNet (PyTorch)  │
│  (KenarDeseniKodla)    │  │  • Encoder-Decoder        │
│  • bwboundary          │  │  • Skip Connections       │
│  • Gauss Piramidi      │  │  • BatchNorm + ReLU       │
│  • Patch/Çizgi         │  │  • Early Stopping         │
│                        │  │  • GPU Destekli Eğitim   │
│  Özellik Mühendisliği  │  └────────────┬─────────────┘
│  (Modelleme.ipynb)     │               │
│  • SIFT (tercih edilen)│               │
│  • HOG / CoHOG / LBP  │               │
│  • Benzerlik eşiği     │               │
└────────────┬───────────┘               │
             │                           │
             └─────────────┬─────────────┘
                           │
               ┌───────────▼───────────┐
               │  Böbrek Segmentasyon   │
               │       Maskesi          │
               └───────────────────────┘
```

---

## 🚀 Kurulum ve Çalıştırma

### Bağımlılıklar

```bash
pip install torch torchvision
pip install opencv-python
pip install scikit-image==0.19.3
pip install scikit-learn
pip install brisque
pip install shapely
pip install matplotlib numpy scipy tqdm
```

### Google Colab'da Çalıştırma

1. Notebook'ları Google Drive'a yükleyin
2. Veri yollarını kendi Drive yapınıza göre güncelleyin:

```python
# yapayZeka.ipynb — veri yolları
x_data = sorted(glob.glob("/content/drive/Shareddrives/<DRIVE_ADINIZ>/DB/images/*"))
y_data = sorted(glob.glob("/content/drive/Shareddrives/<DRIVE_ADINIZ>/DB/labels/*"))
```

3. **Çalıştırma sırası:**

```
① Onislem.ipynb          → Ön işleme & kalite seçimi
② KenarDeseniKodla.ipynb → Kenar & desen kodlama (geleneksel yol)
③ Modelleme.ipynb        → Özellik çıkarma & karşılaştırma
④ yapayZeka.ipynb        → UNet eğitimi & değerlendirme (DL yolu)
```

---

## 📈 Temel Bulgular

| Bulgu | Detay |
|---|---|
| **BRISQUE filtresi** ile veri kalitesi artırıldı | Ortalama skor: ~14.46 (düşük = kaliteli) |
| **SIFT**, tıbbi görüntülerde en kararlı tanımlayıcı | ORB ve AKAZE'ye kıyasla daha az yanlış eşleşme |
| **Erosion + HOG** en saf böbrek bölgesi özelliklerini üretiyor | Sınır artefaktları erozyon ile giderildi |
| **ScaleNormUNet** erken durdurma ile aşırı öğrenme önlendi | `patience=3`, `best_model.pth` checkpoint |
| **İki yaklaşım karşılaştırması** yorumlanabilirlik vs. doğruluk trade-off'unu ortaya koydu | |

---

## 🎓 Kapsanan Teknik Yetkinlikler

Bu proje, aşağıdaki alanlardaki uygulamalı deneyimi kapsamaktadır:

- ✅ **Medikal yapay zeka** — CT görüntüsü segmentasyonu, klinik veri işleme
- ✅ **Derin öğrenme** — PyTorch ile model tasarımı, eğitim, hyperparameter ayarı
- ✅ **Bilgisayarlı görü** — Segmentasyon, kenar tespiti, özellik çıkarma
- ✅ **Veri kalitesi iyileştirme** — BRISQUE tabanlı otomatik filtreleme pipeline'ı
- ✅ **Model optimizasyonu** — Early Stopping, normalizasyon, veri bölme stratejileri
- ✅ **Büyük veri seti yönetimi** — Google Drive entegrasyonu, batch tabanlı yükleme
- ✅ **Akademik metodoloji** — Klasik vs. derin öğrenme karşılaştırmalı analiz
- ✅ **Python yetkinliği** — OOP (Dataset sınıfı), fonksiyonel programlama, bilimsel kütüphaneler

---

## 📚 Referanslar ve Akademik Bağlam

| Kaynak | Kullanım |
|---|---|
| Ronneberger et al. (2015) — *U-Net: Biomedical Image Segmentation* | Temel mimari |
| Dalal & Triggs (2005) — *HOG for Human Detection* | HOG özellik tanımlayıcı |
| Lowe (2004) — *SIFT: Scale-Invariant Keypoints* | Anahtar nokta yöntemi |
| Mittal et al. (2012) — *BRISQUE: Blind Image Quality* | Veri kalitesi değerlendirme |
| Ji et al. (2022) — *AMOS: Abdominal Multi-Organ Segmentation* | Veri seti |
