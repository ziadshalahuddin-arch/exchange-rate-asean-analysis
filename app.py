import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

st.set_page_config(
    page_title="ASEAN Exchange Rate Analysis",
    layout="wide"
)

st.title("📈 ASEAN Exchange Rate Analysis")
st.markdown("""
Analisis nilai tukar mata uang negara ASEAN terhadap USD.  
Proyek ini bertujuan untuk melihat **pergerakan, volatilitas, dan return harian**
sebagai dasar analisis ekonomi makro.
""")

df = pd.read_csv("data/exchange_rate.csv", index_col=0, parse_dates=True)

df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)
df_numeric = df[selected_countries]

return_df.index = pd.to_datetime(return_df.index)
# Hitung log return harian

df_numeric = df.apply(pd.to_numeric, errors="coerce")
return_df = np.log(df_numeric / df_numeric.shift(1)).dropna()

corr_matrix = return_df.corr()

st.sidebar.header("⚙️ Pengaturan")

countries = df.columns.tolist()

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

st.subheader("Pergerakan Nilai Tukar")

fig, ax = plt.subplots(figsize=(10,5))
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

if analysis_type == "Return Harian":
    st.subheader("📉 Return Harian Nilai Tukar")

    fig, ax = plt.subplots(figsize=(10,5))
    ax.xaxis.set_major_locator(mdates.YearLocator(5))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    # Format sumbu waktu (tahun)
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

    # Interpretasi singkat (DINILAI DOSEN)
    st.markdown("""
    **Interpretasi Singkat:**
    - Nilai return positif menunjukkan apresiasi mata uang terhadap USD
    - Return negatif mencerminkan depresiasi
    - Lonjakan ekstrem mengindikasikan periode ketidakstabilan atau krisis ekonomi
    """)

if analysis_type == "Volatilitas":
    st.subheader("📊 Volatilitas Nilai Tukar")

    # Hitung volatilitas (std dev return harian)
    volatility = return_df[selected_countries].std()

    st.write("Standar deviasi return harian (indikator volatilitas):")
    st.dataframe(volatility)

    # Visualisasi bar chart
    fig, ax = plt.subplots(figsize=(8,5))
    volatility.plot(kind="bar", ax=ax)
    ax.xaxis.set_major_locator(mdates.YearLocator(5))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    ax.set_ylabel("Volatilitas (Std. Dev)")
    ax.set_xlabel("Negara")
    ax.set_title("Perbandingan Volatilitas Nilai Tukar")

    plt.tight_layout()
    st.pyplot(fig)

    # Interpretasi ekonomi
    st.markdown("""
    **Interpretasi Singkat:**
    - Volatilitas yang lebih tinggi menunjukkan nilai tukar lebih tidak stabil
    - Mata uang dengan volatilitas tinggi memiliki risiko nilai tukar yang lebih besar
    - Stabilitas nilai tukar penting bagi perdagangan internasional dan investasi asing
    """)


if analysis_type == "Korelasi":
    st.subheader("🔗 Korelasi Return Antar Mata Uang")

    corr_matrix = return_df[selected_countries].corr()

    st.write("Matriks korelasi return harian:")
    st.dataframe(corr_matrix)

    fig, ax = plt.subplots(figsize=(7,6))
    cax = ax.matshow(corr_matrix, cmap="coolwarm")
    ax.xaxis.set_major_locator(mdates.YearLocator(5))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    fig.colorbar(cax)

    ax.set_xticks(range(len(corr_matrix.columns)))
    ax.set_yticks(range(len(corr_matrix.columns)))
    ax.set_xticklabels(corr_matrix.columns, rotation=45)
    ax.set_yticklabels(corr_matrix.columns)

    plt.tight_layout()
    st.pyplot(fig)

    # Interpretasi ekonomi
    st.markdown("""
    **Interpretasi Singkat:**
    - Korelasi positif tinggi menunjukkan pergerakan mata uang yang searah
    - Korelasi rendah atau negatif menandakan perbedaan respons terhadap guncangan eksternal
    - Tingkat korelasi mencerminkan integrasi finansial antar negara
    """)

st.markdown("---")
st.caption("""
📌 **Sumber Data**  
Data nilai tukar diperoleh dari **Yahoo Finance**  
(Ticker: IDRUSD=X, MYRUSD=X, THBUSD=X, PHPUSD=X)  
Frekuensi: Harian  
Periode: 2000–2024 (sesuai ketersediaan data)
""")


