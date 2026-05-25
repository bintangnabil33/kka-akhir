# analisispenjualan
# =========================================
# PRAKTIKUM ANALISIS PERFORMA PENJUALAN
# =========================================

# =========================================
# 1. IMPORT LIBRARY
# =========================================
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import os

# =========================================
# 2. CEK FOLDER AKTIF
# =========================================
print("Folder aktif Python:")
print(os.getcwd())

# =========================================
# 3. MEMBACA DATASET
# =========================================
# PASTIKAN NAMA FILE CSV = data.csv
# DAN BERADA DI FOLDER YANG SAMA DENGAN FILE PYTHON

df = pd.read_csv('data.csv')

# =========================================
# 4. MENAMPILKAN DATA AWAL
# =========================================
print("\n===== DATA AWAL =====")
print(df.head())

# =========================================
# 5. INFORMASI DATA
# =========================================
print("\n===== INFO DATA =====")
print(df.info())

# =========================================
# 6. CEK DATA KOSONG
# =========================================
print("\n===== DATA KOSONG =====")
print(df.isnull().sum())

# =========================================
# 7. UBAH FORMAT TANGGAL
# =========================================
df['Order_Date'] = pd.to_datetime(df['Order_Date'])

# =========================================
# 8. HAPUS HARGA NEGATIF
# =========================================
df = df[df['Price_Per_Unit'] > 0]

# =========================================
# =========================================
# TUGAS 1
# PRODUK UNDERPERFORMER
# =========================================
# =========================================

print("\n===== TUGAS 1 : PRODUK UNDERPERFORMER =====")

# Rata-rata harga
rata_harga = df['Price_Per_Unit'].mean()

print("\nRata-rata Harga:")
print(rata_harga)

# Produk mahal
produk_mahal = df[df['Price_Per_Unit'] > rata_harga]

# Quantity terkecil
underperformer = produk_mahal.sort_values(by='Quantity')

print("\n10 Produk Underperformer:")
print(underperformer.head(10))

# =========================================
# VISUALISASI SCATTER PLOT
# =========================================
plt.figure(figsize=(10,6))

plt.scatter(
    df['Price_Per_Unit'],
    df['Quantity']
)

plt.xlabel('Price Per Unit')
plt.ylabel('Quantity')
plt.title('Produk Mahal vs Quantity')

plt.show()

# =========================================
# =========================================
# TUGAS 2
# RFM ANALYSIS
# =========================================
# =========================================

print("\n===== TUGAS 2 : RFM ANALYSIS =====")

snapshot_date = df['Order_Date'].max() + dt.timedelta(days=1)

rfm = df.groupby('CustomerID').agg({
    'Order_Date': lambda x: (snapshot_date - x.max()).days,
    'Order_ID': 'count',
    'Total_Sales': 'sum'
})

rfm.columns = ['Recency', 'Frequency', 'Monetary']

print("\nHasil RFM:")
print(rfm.head())

# Pelanggan terbaik
rfm_terbaik = rfm.sort_values(by='Monetary', ascending=False)

print("\n10 Pelanggan Terbaik:")
print(rfm_terbaik.head(10))

# =========================================
# =========================================
# TUGAS 3
# EFISIENSI KATEGORI
# =========================================
# =========================================

print("\n===== TUGAS 3 : EFISIENSI KATEGORI =====")

kategori = df.groupby('Product_Category').agg({
    'Total_Sales':'sum',
    'Ad_Budget':'sum'
})

kategori['Efisiensi'] = kategori['Total_Sales'] / kategori['Ad_Budget']

kategori = kategori.sort_values(by='Efisiensi')

print("\nEfisiensi Kategori:")
print(kategori)

# =========================================
# VISUALISASI BAR CHART
# =========================================
kategori['Efisiensi'].plot(
    kind='barh',
    figsize=(10,6)
)

plt.title('Efisiensi Kategori Produk')
plt.xlabel('Efisiensi')
plt.ylabel('Kategori')

plt.show()

# =========================================
# =========================================
# TUGAS 4
# PENGARUH IKLAN
# =========================================
# =========================================

print("\n===== TUGAS 4 : PENGARUH IKLAN =====")

median_iklan = df['Ad_Budget'].median()

print("\nMedian Ad Budget:")
print(median_iklan)

# Kelompok iklan
iklan_tinggi = df[df['Ad_Budget'] > median_iklan]
iklan_rendah = df[df['Ad_Budget'] <= median_iklan]

# Rata-rata penjualan
rata_tinggi = iklan_tinggi['Total_Sales'].mean()
rata_rendah = iklan_rendah['Total_Sales'].mean()

print("\nRata-rata Penjualan Iklan Tinggi:")
print(rata_tinggi)

print("\nRata-rata Penjualan Iklan Rendah:")
print(rata_rendah)

# Kesimpulan sederhana
if rata_tinggi > rata_rendah:
    print("\nKESIMPULAN:")
    print("Iklan tinggi cenderung meningkatkan penjualan.")
else:
    print("\nKESIMPULAN:")
    print("Iklan tinggi belum tentu meningkatkan penjualan.")

# =========================================
# ANALISIS TREN PENJUALAN BULANAN
# =========================================

print("\n===== TREN PENJUALAN BULANAN =====")

df['Month'] = df['Order_Date'].dt.to_period('M').astype(str)

monthly_sales = df.groupby('Month')['Total_Sales'].sum()

print(monthly_sales)

# =========================================
# LINE CHART
# =========================================
plt.figure(figsize=(12,6))

plt.plot(
    monthly_sales.index,
    monthly_sales.values,
    marker='o'
)

plt.title('Tren Penjualan Bulanan')
plt.xlabel('Bulan')
plt.ylabel('Total Sales')

plt.xticks(rotation=45)

plt.show()

# =========================================
# ANALISIS KORELASI
# =========================================

print("\n===== ANALISIS KORELASI =====")

correlation = df[['Total_Sales', 'Ad_Budget', 'Price_Per_Unit']].corr()

print(correlation)

# =========================================
# HEATMAP
# =========================================
plt.figure(figsize=(8,5))

sns.heatmap(
    correlation,
    annot=True,
    cmap='coolwarm'
)

plt.title('Peta Korelasi')

plt.show()

# =========================================
# PROGRAM SELESAI
# =========================================
print("\n===== PROGRAM SELESAI =====")

<img width="1000" height="500" alt="tren_penjualan" src="https://github.com/user-attachments/assets/1d0ba7d3-9008-4841-a35f-86276b4a8796" />
<img width="800" height="600" alt="produk_scatter" src="https://github.com/user-attachments/assets/2e391404-b4e6-4520-af12-f9b6321f1f26" />
<img width="600" height="400" alt="korelasi" src="https://github.com/user-attachments/assets/b758e1d9-c01e-4590-9215-d3155998f11a" />
<img width="800" height="600" alt="kategori_penjualan" src="https://github.com/user-attachments/assets/1850ccf2-a70b-4688-90f4-a7f568ee90b9" />
