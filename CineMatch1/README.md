# 🎬 CineMatch — Kişiselleştirilmiş Film Öneri Sistemi
MovieLens ml-32m (32 milyon puanlama) ile eğitilmiş KNN tabanlı film öneri sistemi.

## 🚀 Kurulum (3 adım)

```bash
# 1. Bağımlılıkları yükle
pip install -r requirements.txt

# 2. Uygulamayı başlat
streamlit run app.py
```

✅ cache/ klasörü zaten hazır — herhangi bir veri işleme gerekmez!

## 📁 Yapı

```
CineMatch_Final/
├── app.py                         ← Ana uygulama
├── requirements.txt               ← Bağımlılıklar
├── CineMatch_Akademik_Raporu.docx ← Proje raporu
├── README.md
└── cache/                         ← Hazır model ve veri
    ├── knn_model.pkl              ← Eğitilmiş KNN (K=20)
    ├── movie_stats.csv            ← 7,702 film + IMDb URL
    ├── pivot_sparse.npz           ← CSR sparse matris
    └── ...
```

## 🤖 Algoritma

- **KNN** (K=20, Cosine Similarity)
- **Hibrit skor:** 0.65 × Bayesian + 0.35 × KNN_sim
- **Sparse matris:** 7702×31204 → 12 MB (CSR)

## ✨ Özellikler

- Netflix kart tasarımı + hover efekti
- Her film için IMDb ve TMDB bağlantısı
- "Neden önerildi?" açıklaması
- Veri pipeline görselleştirme
- Gerçek 32M veri istatistikleri
