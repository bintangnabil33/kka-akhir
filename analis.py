import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt

# ===============================
# 1. LOAD DATA
# ===============================
df = pd.read_csv('data_praktikum_analisis_data.csv')

print("=== DATA AWAL ===")
print(df.head())

# ===============================
# 2. DATA CLEANING
# ===============================
print("\n=== INFO DATA ===")
print(df.info())

print("\n=== DATA KOSONG ===")
print(df.isnull().sum())

# Hapus data kosong
df = df.dropna()

# Ubah tipe tanggal
df['Order_Date'] = pd.to_datetime(df['Order_Date'])

# Hapus nilai tidak valid
df = df[df['Price_Per_Unit'] > 0]

# Tambah kolom bulan
df['Month'] = df['Order_Date'].dt.to_period('M').astype(str)

print("\n=== DATA SETELAH CLEANING ===")
print(df.head())

# ===============================
# 3. ANALISIS TREN PENJUALAN
# ===============================
monthly_sales = df.groupby('Month')['Total_Sales'].sum()

plt.figure(figsize=(10,5))
plt.plot(monthly_sales.index, monthly_sales.values, marker='o')
plt.title('Tren Penjualan Bulanan')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('tren_penjualan.png')
plt.show()

# ===============================
# 4. ANALISIS PRODUK (SCATTER)
# ===============================
product_sales = df.groupby('Product_Category').agg({
    'Quantity': 'sum',
    'Total_Sales': 'sum'
}).reset_index()

plt.figure(figsize=(8,6))
plt.scatter(product_sales['Quantity'], product_sales['Total_Sales'])

for i, txt in enumerate(product_sales['Product_Category']):
    plt.annotate(txt, (product_sales['Quantity'][i], product_sales['Total_Sales'][i]))

plt.xlabel('Jumlah Terjual')
plt.ylabel('Total Penjualan')
plt.title('Analisis Produk')
plt.tight_layout()
plt.savefig('produk_scatter.png')
plt.show()

# ===============================
# 5. RFM ANALYSIS
# ===============================
snapshot_date = df['Order_Date'].max() + dt.timedelta(days=1)

rfm = df.groupby('CustomerID').agg({
    'Order_Date': lambda x: (snapshot_date - x.max()).days,
    'Order_ID': 'count',
    'Total_Sales': 'sum'
})

rfm.columns = ['Recency', 'Frequency', 'Monetary']

# Skor RFM
rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5,4,3,2,1])
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1,2,3,4,5])
rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1,2,3,4,5])

rfm['RFM_Group'] = (
    rfm['R_Score'].astype(str) +
    rfm['F_Score'].astype(str) +
    rfm['M_Score'].astype(str)
)

print("\n=== HASIL RFM ===")
print(rfm.head())

# ===============================
# 6. ANALISIS KATEGORI
# ===============================
category_sales = df.groupby('Product_Category')['Total_Sales'].sum().sort_values()

plt.figure(figsize=(8,6))
category_sales.plot(kind='barh')
plt.title('Total Penjualan per Kategori')
plt.tight_layout()
plt.savefig('kategori_penjualan.png')
plt.show()

# ===============================
# 7. ANALISIS IKLAN (KORELASI)
# ===============================
correlation = df[['Total_Sales', 'Ad_Budget']].corr()

plt.figure(figsize=(6,4))
sns.heatmap(correlation, annot=True)
plt.title('Korelasi Iklan vs Penjualan')
plt.tight_layout()
plt.savefig('korelasi.png')
plt.show()

# ===============================
# 8. SIMPAN HASIL RFM KE FILE
# ===============================
rfm.to_csv('hasil_rfm.csv')

print("\n=== ANALISIS SELESAI ===")
print("File grafik dan hasil sudah tersimpan.")