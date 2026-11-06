# Proyek Analisis Data: E-Commerce Public Dataset (Olist)

Proyek akhir kelas **Belajar Analisis Data dengan Python (Dicoding)**. Menganalisis
dataset marketplace **Olist (Brazil, 2016–2018)** untuk menjawab dua pertanyaan
bisnis seputar kinerja kategori/pembayaran dan hubungan kecepatan pengiriman
dengan kepuasan pelanggan, dilengkapi dashboard interaktif Streamlit.

## Pertanyaan Bisnis
1. Kategori produk apa dan metode pembayaran apa yang menyumbang nilai transaksi
   tertinggi pada order `delivered` sepanjang periode data?
2. Bagaimana hubungan lama pengiriman terhadap skor review pelanggan, dan di
   provinsi mana keterlambatan paling tinggi?

## Struktur Direktori
```
submission/
├── dashboard/
│   ├── dashboard.py        # aplikasi Streamlit
│   └── main_data.csv       # dataset gabungan hasil wrangling (dipakai dashboard)
├── data/                   # 9 berkas CSV dataset Olist mentah
├── notebook.ipynb          # notebook analisis (sudah dijalankan)
├── README.md               # berkas ini
├── requirements.txt        # daftar dependency
├── url.txt                 # tautan dashboard Streamlit Cloud
└── PANDUAN_DEPLOY_STREAMLIT_CLOUD.md  # panduan deploy ke cloud
```

## Cara Menjalankan

### 1. Siapkan environment
Gunakan Python 3.10–3.12 (direkomendasikan). Buat virtual environment dan pasang
dependency:

```bash
# buat & aktifkan virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# pasang dependency
pip install -r requirements.txt
```

### 2. Menjalankan notebook analisis
```bash
jupyter notebook notebook.ipynb
# atau buka di VS Code / Google Colab
```

### 3. Menjalankan dashboard Streamlit (lokal)
```bash
cd dashboard
streamlit run dashboard.py
```
Dashboard akan terbuka otomatis di browser pada `http://localhost:8501`.
Gunakan filter **rentang tanggal** dan **provinsi** di sidebar untuk menyaring data.

## Fitur Dashboard
- **KPI ringkas:** total order, total pendapatan, rata-rata skor review, rata-rata lama kirim.
- **Pertanyaan 1:** Top 10 kategori pendapatan & komposisi metode pembayaran.
- **Pertanyaan 2:** rata-rata lama kirim per skor review & provinsi dengan keterlambatan tertinggi.
- **Analisis lanjutan:** segmentasi pelanggan RFM & binning kecepatan pengiriman.
- **Filter interaktif:** rentang tanggal pembelian dan pemilihan provinsi.

## Teknik Analisis Lanjutan (tanpa Machine Learning)
- **RFM Analysis** — segmentasi pelanggan berdasarkan Recency, Frequency, Monetary.
- **Geospatial Analysis** — pemetaan sebaran order per provinsi dengan koordinat.
- **Manual Clustering (Binning)** — pengelompokan kecepatan pengiriman dengan `pd.cut`.

## Sumber Dataset
E-Commerce Public Dataset (Olist) — disediakan oleh Dicoding
([sumber asli: Kaggle - Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)).
