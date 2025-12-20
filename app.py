import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# =====================
# CONFIG
# =====================
st.set_page_config(
    page_title="ASEAN Exchange Rate Analysis",
    layout="wide"
)

st.title("📈 ASEAN Exchange Rate Analysis")
st.markdown("""
Analisis nilai tukar mata uang negara ASEAN terhadap USD (Berdasarkan Yahoo Finance).
Fokus analisis meliputi **level nilai tukar, return harian, volatilitas, dan korelasi**.
""")

st.markdown("""
## 📌 Pendahuluan

Nilai tukar (*exchange rate*) merupakan salah satu indikator makroekonomi yang penting
dalam perekonomian terbuka. Pergerakan nilai tukar memengaruhi stabilitas ekonomi,
perdagangan internasional, arus modal, serta daya saing suatu negara.

Negara-negara ASEAN memiliki keterkaitan ekonomi dan keuangan yang kuat,
sehingga fluktuasi nilai tukar di satu negara dapat berdampak pada negara lainnya.
Dalam dua dekade terakhir, nilai tukar mata uang ASEAN terhadap dolar Amerika Serikat (USD)
mengalami dinamika yang dipengaruhi oleh kebijakan moneter global, krisis keuangan,
serta kondisi ekonomi domestik masing-masing negara.

Proyek ini bertujuan untuk menganalisis pergerakan nilai tukar mata uang
Indonesia (IDR), Malaysia (MYR), Thailand (THB), dan Filipina (PHP)
terhadap USD menggunakan data harian periode jangka panjang.
Analisis dilakukan melalui pendekatan **time series**, yang mencakup:

- Level nilai tukar
- Return harian
- Volatilitas
- Korelasi antar mata uang

Hasil analisis divisualisasikan dalam bentuk aplikasi interaktif berbasis **Streamlit**
sebagai penerapan analisis data dan ekonomi makro.
""")

import os

st.subheader("🗺️ Peta Asia Tenggara")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(BASE_DIR, "images", "asean_map.png")

if os.path.exists(image_path):
    st.image(
        image_path,
        caption="Peta Negara-Negara ASEAN",
        use_container_width=True
    )
else:
    st.error(f"Gambar tidak ditemukan: {image_path}")


st.info("""
📌 Interaksi dilakukan melalui sidebar.  
Peta digunakan sebagai konteks geografis untuk memahami keterkaitan regional ASEAN.
""")

# =====================
# LOAD DATA (AMAN)
# =====================
df = pd.read_csv("data/exchange_rate.csv")

# Jika kolom Date tidak ada, pakai kolom pertama sebagai tanggal
if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df.set_index("Date", inplace=True)
else:
    # anggap kolom pertama adalah tanggal
    df.iloc[:, 0] = pd.to_datetime(df.iloc[:, 0], errors="coerce")
    df.set_index(df.columns[0], inplace=True)

df = df.dropna()

# Pastikan data numerik
df_numeric = df.apply(pd.to_numeric, errors="coerce")

# Hitung log return
return_df = np.log(df_numeric / df_numeric.shift(1)).dropna()

# =====================
# SIDEBAR
# =====================
import streamlit as st

st.set_page_config(
    page_title="Analisis Nilai Tukar ASEAN",
    layout="wide"
)

# =========================
# SIDEBAR - DAFTAR ISI
# =========================
st.sidebar.title("📌 Daftar Isi")

st.sidebar.markdown("""
1. [Pendahuluan](#pendahuluan)  
2. [Data & Metodologi](#data--metodologi)  
3. [Level Nilai Tukar](#level-nilai-tukar)  
4. [Return Harian](#return-harian)  
5. [Volatilitas Nilai Tukar](#volatilitas-nilai-tukar)  
6. [Korelasi Antar Negara](#korelasi-antar-negara)  
7. [Interpretasi Ekonomi](#interpretasi-ekonomi)  
8. [Kesimpulan](#kesimpulan)  
""")

st.sidebar.header("⚙️ Pengaturan")

countries = df_numeric.columns.tolist()

selected_countries = st.sidebar.multiselect(
    "Pilih negara",
    countries,
    default=countries[:3]
)

analysis_type = st.sidebar.radio(
    "Pilih Analisis",
    [
        "Level Nilai Tukar",
        "Return Harian",
        "Volatilitas",
        "Korelasi"
    ]
)

# =====================
# LEVEL NILAI TUKAR
# =====================
st.subheader("📈 Pergerakan Nilai Tukar")

fig, ax = plt.subplots(figsize=(10, 5))
ax.xaxis.set_major_locator(mdates.YearLocator(5))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

for country in selected_countries:
    ax.plot(df_numeric.index, df_numeric[country], label=country)

ax.set_xlabel("Tahun")
ax.set_ylabel("Nilai Tukar")
ax.legend()
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)

# =====================
# RETURN HARIAN
# =====================
if analysis_type == "Return Harian":
    st.subheader("📉 Return Harian Nilai Tukar")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.xaxis.set_major_locator(mdates.YearLocator(5))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    for country in selected_countries:
        ax.plot(return_df.index, return_df[country], label=country)

    ax.axhline(0, linestyle="--", linewidth=1)
    ax.set_xlabel("Tahun")
    ax.set_ylabel("Log Return")
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("""
    **Interpretasi:**
    - Return positif → mata uang **apresiasi**
    - Return negatif → mata uang **depresiasi**
    - Fluktuasi ekstrem → indikasi ketidakstabilan ekonomi
    """)

# =====================
# VOLATILITAS
# =====================
if analysis_type == "Volatilitas":
    st.subheader("📊 Volatilitas Nilai Tukar")

    volatility = return_df[selected_countries].std()

    st.write("Standar deviasi return harian:")
    st.dataframe(volatility)

    fig, ax = plt.subplots(figsize=(8, 5))
    volatility.plot(kind="bar", ax=ax)
    ax.set_ylabel("Volatilitas")
    ax.set_xlabel("Negara")
    ax.set_title("Perbandingan Volatilitas")
    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("""
    **Interpretasi:**
    - Volatilitas tinggi → risiko nilai tukar lebih besar
    - Volatilitas rendah → stabilitas relatif lebih baik
    """)

# =====================
# KORELASI
# =====================
if analysis_type == "Korelasi":
    st.subheader("🔗 Korelasi Return Antar Mata Uang")

    corr_matrix = return_df[selected_countries].corr()
    st.dataframe(corr_matrix)

    fig, ax = plt.subplots(figsize=(7, 6))
    cax = ax.matshow(corr_matrix, cmap="coolwarm")
    fig.colorbar(cax)

    ax.set_xticks(range(len(corr_matrix.columns)))
    ax.set_yticks(range(len(corr_matrix.columns)))
    ax.set_xticklabels(corr_matrix.columns, rotation=45)
    ax.set_yticklabels(corr_matrix.columns)

    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("""
    **Interpretasi:**
    - Korelasi positif tinggi → pergerakan searah
    - Korelasi rendah/negatif → respon ekonomi berbeda
    """)

# =====================
# SUMBER DATA
# =====================
st.markdown("---")
st.caption("""
📌 **Sumber Data**  
Yahoo Finance  
Ticker: IDRUSD=X, MYRUSD=X, THBUSD=X, PHPUSD=X  
Frekuensi: Harian  
Periode: 2005–2025
""")
