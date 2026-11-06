"""
Dashboard Analisis E-Commerce Olist
Dicoding - Proyek Akhir Analisis Data dengan Python
Menjalankan: streamlit run dashboard.py
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set_theme(style="whitegrid")

# ---------------------------------------------------------------- CONFIG
st.set_page_config(page_title="Dashboard E-Commerce Olist", page_icon="🛒", layout="wide")


# ---------------------------------------------------------------- DATA LOADER
@st.cache_data
def load_data():
    here = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(here, "main_data.csv"),
        os.path.join(os.getcwd(), "main_data.csv"),
        os.path.join(os.getcwd(), "dashboard", "main_data.csv"),
    ]
    path = next((p for p in candidates if os.path.exists(p)), candidates[0])
    df = pd.read_csv(path)
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    df["order_delivered_customer_date"] = pd.to_datetime(df["order_delivered_customer_date"])
    return df


df = load_data()

# ---------------------------------------------------------------- SIDEBAR FILTER
st.sidebar.title("🛒 Filter Data")
st.sidebar.markdown("Gunakan filter di bawah untuk menyaring periode & wilayah.")

min_date = df["order_purchase_timestamp"].min().date()
max_date = df["order_purchase_timestamp"].max().date()
date_range = st.sidebar.date_input(
    "Rentang Tanggal Pembelian",
    value=[min_date, max_date], min_value=min_date, max_value=max_date,
)
if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

states = sorted(df["customer_state"].dropna().unique().tolist())
sel_states = st.sidebar.multiselect("Provinsi (State)", states, default=states)

mask = (
    (df["order_purchase_timestamp"].dt.date >= start_date)
    & (df["order_purchase_timestamp"].dt.date <= end_date)
    & (df["customer_state"].isin(sel_states))
)
d = df[mask].copy()

st.sidebar.markdown("---")
st.sidebar.caption(f"Menampilkan **{len(d):,}** order terfilter dari total **{len(df):,}**.")

# ---------------------------------------------------------------- HEADER + KPI
st.title("🛒 Dashboard Analisis E-Commerce Olist")
st.markdown(
    "Analisis order **delivered** marketplace Olist (Brazil, 2016–2018): "
    "kinerja kategori & pembayaran, hubungan kecepatan pengiriman dengan kepuasan, "
    "serta segmentasi pelanggan (RFM)."
)

if len(d) == 0:
    st.warning("Tidak ada data pada filter yang dipilih. Longgarkan filter di sidebar.")
    st.stop()

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Order", f"{len(d):,}")
k2.metric("Total Pendapatan", f"R$ {d['payment_value'].sum()/1e6:,.2f} jt")
k3.metric("Rata-rata Skor Review", f"{d['review_score'].mean():.2f} / 5")
k4.metric("Rata-rata Lama Kirim", f"{d['delivery_days'].mean():.1f} hari")

st.markdown("---")

# ---------------------------------------------------------------- Q1
st.header("Pertanyaan 1 — Kategori Produk & Metode Pembayaran")
c1, c2 = st.columns(2)

with c1:
    st.subheader("Top 10 Kategori berdasarkan Pendapatan")
    cat = (d.groupby("product_category_name_english")["order_price"]
           .sum().sort_values(ascending=False).head(10).sort_values())
    fig, ax = plt.subplots(figsize=(7, 5))
    colors = ["#bdbdbd"] * len(cat); colors[-1] = "#1f77b4"
    ax.barh(cat.index, cat.values / 1e6, color=colors)
    ax.set_xlabel("Pendapatan (juta BRL)")
    ax.bar_label(ax.containers[0], fmt="%.2f", padding=3, fontsize=8)
    st.pyplot(fig); plt.close(fig)

with c2:
    st.subheader("Nilai Transaksi per Metode Pembayaran")
    pay = (d.groupby("payment_type")["payment_value"].sum()
           .sort_values())
    pay = pay[pay.index != "not_defined"]
    fig, ax = plt.subplots(figsize=(7, 5))
    colors = ["#bdbdbd"] * len(pay); colors[-1] = "#2ca02c"
    ax.barh(pay.index, pay.values / 1e6, color=colors)
    ax.set_xlabel("Nilai Transaksi (juta BRL)")
    ax.bar_label(ax.containers[0], fmt="%.2f", padding=3, fontsize=8)
    st.pyplot(fig); plt.close(fig)

st.info(
    "**Insight:** Kategori *health_beauty*, *watches_gifts*, dan *bed_bath_table* "
    "menjadi penyumbang pendapatan terbesar, sementara **kartu kredit** mendominasi "
    "nilai transaksi (±80%)."
)

st.markdown("---")

# ---------------------------------------------------------------- Q2
st.header("Pertanyaan 2 — Lama Pengiriman vs Kepuasan Pelanggan")
c3, c4 = st.columns(2)

with c3:
    st.subheader("Rata-rata Lama Pengiriman per Skor Review")
    dd = d[(d["delivery_days"] >= 0) & (d["delivery_days"] <= 365)].dropna(subset=["review_score"])
    md = dd.groupby("review_score")["delivery_days"].mean()
    fig, ax = plt.subplots(figsize=(7, 5))
    palette = ["#d62728", "#ff7f0e", "#ffbb78", "#98df8a", "#2ca02c"]
    bars = ax.bar(md.index.astype(int).astype(str), md.values,
                  color=palette[:len(md)])
    ax.set_xlabel("Skor Review (bintang)"); ax.set_ylabel("Rata-rata Hari Kirim")
    ax.bar_label(bars, fmt="%.1f", padding=3)
    st.pyplot(fig); plt.close(fig)

with c4:
    st.subheader("10 Provinsi dengan Keterlambatan Tertinggi")
    sl = (dd.groupby("customer_state")
          .agg(orders=("order_id", "count"), late_rate=("is_late", "mean")))
    sl = sl[sl["orders"] >= 50].sort_values("late_rate", ascending=False).head(10).sort_values("late_rate")
    fig, ax = plt.subplots(figsize=(7, 5))
    colors = ["#bdbdbd"] * len(sl); 
    if len(sl): colors[-1] = "#d62728"
    ax.barh(sl.index, sl["late_rate"] * 100, color=colors)
    ax.set_xlabel("Order Terlambat dari Estimasi (%)")
    if len(sl):
        ax.bar_label(ax.containers[0], fmt="%.1f%%", padding=3, fontsize=8)
    st.pyplot(fig); plt.close(fig)

corr = dd["delivery_days"].corr(dd["review_score"]) if len(dd) else float("nan")
st.info(
    f"**Insight:** Korelasi lama pengiriman vs skor review = **{corr:.2f}** (negatif) — "
    "makin lama pengiriman, makin rendah kepuasan. Keterlambatan menumpuk di provinsi "
    "Timur Laut yang jauh dari pusat logistik São Paulo."
)

st.markdown("---")

# ---------------------------------------------------------------- ADVANCED: RFM + binning
st.header("Analisis Lanjutan")
c5, c6 = st.columns(2)

with c5:
    st.subheader("Segmentasi Pelanggan (RFM)")
    seg_order = ["Champions", "Loyal", "Potential", "At Risk", "Hibernating"]
    seg = (d.dropna(subset=["segment"])
           .drop_duplicates("customer_unique_id")["segment"]
           .value_counts().reindex(seg_order).dropna())
    fig, ax = plt.subplots(figsize=(7, 5))
    pal = {"Champions": "#2ca02c", "Loyal": "#98df8a", "Potential": "#bdbdbd",
           "At Risk": "#ff7f0e", "Hibernating": "#d62728"}
    bars = ax.bar(seg.index, seg.values, color=[pal[s] for s in seg.index])
    ax.set_ylabel("Jumlah Pelanggan")
    ax.bar_label(bars, fmt="%d", padding=3, fontsize=8)
    plt.setp(ax.get_xticklabels(), rotation=20, ha="right")
    st.pyplot(fig); plt.close(fig)

with c6:
    st.subheader("Skor Review per Kelompok Kecepatan Kirim (Binning)")
    dd2 = d[(d["delivery_days"] >= 0) & (d["delivery_days"] <= 400)].dropna(subset=["review_score"]).copy()
    dd2["bucket"] = pd.cut(dd2["delivery_days"], bins=[-0.1, 3, 7, 14, 30, 400],
                           labels=["<=3d", "4-7d", "8-14d", "15-30d", ">30d"])
    b = dd2.groupby("bucket", observed=True)["review_score"].mean()
    fig, ax = plt.subplots(figsize=(7, 5))
    norm = plt.Normalize(b.min(), b.max())
    bars = ax.bar(b.index.astype(str), b.values, color=plt.cm.RdYlGn(norm(b.values)))
    ax.set_ylim(0, 5); ax.set_ylabel("Rata-rata Skor Review")
    ax.bar_label(bars, fmt="%.2f", padding=3, fontsize=8)
    st.pyplot(fig); plt.close(fig)

st.info(
    "**Insight:** Mayoritas pelanggan di segmen *Potential* & *Loyal* dengan kelompok "
    "*Champions* bernilai tinggi. Skor review anjlok tajam saat pengiriman melewati 14 hari "
    "(≤3 hari ≈ 4,5 vs >30 hari ≈ 2,3)."
)

st.markdown("---")
st.caption("Proyek Analisis Data — Dicoding | Dataset: E-Commerce Public Dataset (Olist Brazil)")
