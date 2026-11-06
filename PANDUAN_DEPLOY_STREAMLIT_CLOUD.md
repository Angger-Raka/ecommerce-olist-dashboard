# Panduan Deploy Dashboard ke Streamlit Community Cloud

Dashboard sudah berjalan lancar di lokal (syarat wajib terpenuhi). Men-deploy ke
Streamlit Cloud adalah **saran ke-3 Dicoding** untuk menaikkan nilai ke Bintang 5.
Ikuti langkah berikut.

## Prasyarat
- Akun **GitHub** (gratis).
- Akun **Streamlit Community Cloud** — daftar gratis di [share.streamlit.io](https://share.streamlit.io) menggunakan akun GitHub.

## Langkah 1 — Siapkan Repository GitHub
1. Buat repository baru di GitHub, misalnya `ecommerce-olist-dashboard` (boleh public).
2. Unggah **seluruh isi folder `submission/`** ke repository tersebut. Struktur
   penting yang harus ada di repo:
   ```
   dashboard/dashboard.py
   dashboard/main_data.csv
   requirements.txt
   ```
   > Catatan: `requirements.txt` **wajib** berada di root repository agar
   > Streamlit Cloud dapat memasang dependency.

   Contoh via terminal:
   ```bash
   cd submission
   git init
   git add .
   git commit -m "Submission dashboard Olist e-commerce"
   git branch -M main
   git remote add origin https://github.com/<username>/ecommerce-olist-dashboard.git
   git push -u origin main
   ```

## Langkah 2 — Deploy di Streamlit Cloud
1. Buka [share.streamlit.io](https://share.streamlit.io) lalu login dengan GitHub.
2. Klik tombol **"Create app"** → **"Deploy a public app from GitHub"**.
3. Isi form:
   - **Repository:** `<username>/ecommerce-olist-dashboard`
   - **Branch:** `main`
   - **Main file path:** `dashboard/dashboard.py`
4. Klik **"Deploy"**. Streamlit akan memasang dependency dari `requirements.txt`
   lalu menjalankan aplikasi (proses 2–5 menit pada build pertama).

## Langkah 3 — Ambil URL & Isi url.txt
1. Setelah status menjadi **"Your app is live!"**, salin URL aplikasi, formatnya:
   ```
   https://<nama-app-anda>.streamlit.app
   ```
2. Tempel URL tersebut ke berkas `url.txt` (ganti baris placeholder).

## Troubleshooting
- **Build gagal / error dependency:** pastikan versi di `requirements.txt` cocok.
  Versi yang sudah diuji pada proyek ini: `pandas==2.2.3`, `numpy==2.2.6`,
  `matplotlib==3.11.2`, `seaborn==0.13.2`, `streamlit==1.66.1`.
- **`FileNotFoundError: main_data.csv`:** pastikan `dashboard/main_data.csv`
  ikut ter-commit ke GitHub (file ini wajib ada di repo, bukan hanya di lokal).
  Loader di `dashboard.py` sudah mencari file relatif terhadap lokasi skrip,
  jadi struktur `dashboard/` yang utuh sudah cukup.
- **App "sleeping":** app gratis bisa tertidur jika lama tak diakses — cukup buka
  URL-nya dan tunggu beberapa detik untuk membangunkannya kembali.

## Ringkas
| Item | Nilai |
|------|-------|
| Main file path | `dashboard/dashboard.py` |
| Python version | 3.10 – 3.12 |
| Dependency | `requirements.txt` di root repo |
| Output | URL `https://<nama>.streamlit.app` → tulis ke `url.txt` |
