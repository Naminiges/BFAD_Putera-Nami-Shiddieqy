# Proyek Analisis Data: E-Commerce Public Dataset 🛒

## Deskripsi

Proyek ini merupakan analisis data dari **E-Commerce Public Dataset** Brasil yang mencakup informasi pesanan, produk, pelanggan, pembayaran, dan review dari tahun 2016 hingga 2018. Proyek ini dibuat sebagai tugas akhir kelas **Belajar Analisis Data dengan Python** di Dicoding.

## Pertanyaan Bisnis

1. **Bagaimana tren jumlah pesanan dan total pendapatan per bulan?** Apakah terdapat pola musiman atau tren pertumbuhan/penurunan dari waktu ke waktu?
2. **Apa saja kategori produk yang paling banyak dibeli dan yang menghasilkan pendapatan terbesar?** Apakah kategori terpopuler juga merupakan yang menghasilkan revenue tertinggi?

## Struktur Direktori

```
BFAD_Putera-Nami-Shiddieqy/
├── dashboard/
│   ├── main_data.csv          # Dataset yang sudah diolah untuk dashboard
│   └── dashboard.py           # Script dashboard Streamlit
├── data/
│   ├── customers_dataset.csv
│   ├── orders_dataset.csv
│   ├── order_items_dataset.csv
│   ├── order_payments_dataset.csv
│   ├── order_reviews_dataset.csv
│   ├── products_dataset.csv
│   ├── sellers_dataset.csv
│   ├── geolocation_dataset.csv
│   └── product_category_name_translation.csv
├── notebook.ipynb             # Jupyter Notebook analisis data
├── README.md                  # Dokumentasi proyek
├── requirements.txt           # Daftar library yang digunakan
└── url.txt                    # Link dashboard (jika di-deploy)
```

## Instalasi

### 1. Clone Repository

```bash
git clone https://github.com/username/BFAD_Putera-Nami-Shiddieqy.git
cd BFAD_Putera-Nami-Shiddieqy
```

### 2. Buat Virtual Environment (Opsional tapi Disarankan)

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Menjalankan Notebook

Buka file `notebook.ipynb` menggunakan Jupyter Notebook atau Google Colab, lalu jalankan seluruh cell secara berurutan.

```bash
jupyter notebook notebook.ipynb
```

> **Catatan:** Pastikan untuk menjalankan seluruh cell di notebook terlebih dahulu agar file `dashboard/main_data.csv` ter-generate.

## Menjalankan Dashboard

Setelah file `dashboard/main_data.csv` tersedia, jalankan dashboard dengan perintah:

```bash
streamlit run dashboard/dashboard.py
```

Dashboard akan terbuka di browser pada `http://localhost:8501`.

### Fitur Dashboard

- 📊 **Metric Cards** – Total pesanan, pendapatan, pelanggan, dan rata-rata review
- 📈 **Tren Bulanan** – Grafik tren jumlah pesanan dan pendapatan per bulan
- 🏆 **Kategori Terpopuler** – Top 10 kategori berdasarkan pesanan dan pendapatan
- 🗺️ **Distribusi State** – Sebaran pelanggan per state Brasil
- 👥 **RFM Analysis** – Segmentasi pelanggan (Best, Loyal, At Risk, Lost, dll.)
- ⭐ **Review Score** – Distribusi score dan rata-rata per kategori
- 🔍 **Date Filter** – Filter data berdasarkan rentang tanggal

## Teknik Analisis Lanjutan

Proyek ini menerapkan **RFM (Recency, Frequency, Monetary) Analysis** untuk mengelompokkan pelanggan berdasarkan perilaku pembelian mereka:

| Metrik | Deskripsi |
|--------|-----------|
| **Recency** | Jumlah hari sejak pembelian terakhir pelanggan |
| **Frequency** | Jumlah transaksi unik yang dilakukan pelanggan |
| **Monetary** | Total pengeluaran pelanggan |

Segmen pelanggan yang dihasilkan:
- 🟢 **Best Customers** – R, F, M tinggi
- 🔵 **Loyal Customers** – Frekuensi tinggi, pembelian baru-baru ini
- 🟠 **Big Spenders** – Pengeluaran tinggi
- 🟣 **Recent Customers** – Baru melakukan pembelian
- 🔴 **At Risk** – Belum bertransaksi dalam waktu lama
- 🟤 **Lost Customers** – Semua metrik rendah

## Informasi Pembuat

- **Nama:** Putera Nami Shiddieqy
- **Email:** puteranami1150@gmail.com
- **ID Dicoding:** puteranami
