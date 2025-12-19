import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# =========================
# Konfigurasi halaman
# =========================
st.set_page_config(
    page_title="ASEAN Exchange Rate Analysis",
    layout="wide"
)

st.title("📈 ASEAN Exchange Rate Analysis")
st.markdown("""
Analisis nilai tukar mata uang negara ASEAN terhadap USD.  
Proyek ini bertujuan untuk menganalisis **pergerakan nilai tukar, return harian,
volatilitas, dan korelasi** sebagai dasar analisis ekonomi makro.
""")

# =========================
# Load data
# =========================
df = pd.read_csv("data/exchange_rate.csv", index_col=0, parse_dates=True)

# Pastikan index adalah datetime
df.index = pd.to_datetime(df.index)

# Pastikan semua data numerik
df = df.apply(pd.to_numeric, errors="coerce")

# =========================
# Sidebar
# =========================
st.sidebar.header("⚙️ Pengaturan")

countries = df.columns.tolist()

selected_countries = st.sidebar.multiselect(
    "Pilih negara",
    countries,
    default=countries
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

# =========================
# Data numerik & return
# =========================
df_numeric = df[selected_countries]

return_df = np.log(df_numeric / df_numeric.shift(1)).dropna()

# =========================
# LEVEL NILAI TUKAR
# =========================
st.subheader("📊 Pergerakan Nilai Tukar")

fig, ax = plt.subplots(figsize=(10,5))
ax.xaxis.set_major_locator(mdates.YearLocator(5))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

for country in selected_countries:
    ax.plot(df_numeric.index, df_numeric[country], label=country)

ax.set_xlabel("Tahun")
ax.set_ylabel("Nilai Tukar terhadap USD")
ax.legend()

plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)

# =========================
# RETURN HARIAN
# =========================
if analysis_type == "Return Harian":
    st.subheader("📉 Return Harian Nilai Tukar")

    fig, ax = plt.subplots(figsize=(10,5))
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
    - Return positif menunjukkan apresiasi mata uang
    - Return negatif menunjukkan depresiasi
    - Lonjakan ekstrem mencerminkan periode krisis atau ketidakstabilan ekonomi
    """)

# =========================
# VOLATILITAS
# =========================
if analysis_type == "Volatilitas":
    st.subheader("📊 Volatilitas Nilai Tukar")

    volatility = return_df.std()

    st.write("Standar deviasi return harian:")
    st.dataframe(volatility)

    fig, ax = plt.subplots(figsize=(8,5))
    volatility.plot(kind="bar", ax=ax)

    ax.set_ylabel("Volatilitas (Std. Dev)")
    ax.set_xlabel("Negara")
    ax.set_title("Perbandingan Volatilitas Nilai Tukar")

    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("""
    **Interpretasi:**
    - Volatilitas tinggi menunjukkan nilai tukar lebih tidak stabil
    - Risiko nilai tukar lebih besar bagi perdagangan dan investasi
    """)

# =========================
# KORELASI
# =========================
if analysis_type == "Korelasi":
    st.subheader("🔗 Korelasi Return Antar Mata Uang")

    corr_matrix = return_df.corr()

    st.write("Matriks korelasi return harian:")
    st.dataframe(corr_matrix)

    fig, ax = plt.subplots(figsize=(7,6))
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
    - Korelasi positif tinggi → pergerakan mata uang searah
    - Korelasi rendah/negatif → respon ekonomi yang berbeda
    - Menggambarkan tingkat integrasi ekonomi regional
    """)

# =========================
# SUMBER DATA
# =========================
st.markdown("---")
st.caption("""
📌 **Sumber Data**  
Data nilai tukar diperoleh dari **Yahoo Finance**  
Ticker: IDRUSD=X, MYRUSD=X, THBUSD=X, PHPUSD=X  
Frekuensi: Harian  
Periode: 2000–2024 (sesuai ketersediaan data)
""")
