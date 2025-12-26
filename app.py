import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px

# ======================
# CONFIG
# ======================
st.set_page_config(
    page_title="ASEAN Exchange Rate Analysis",
    layout="wide"
)

st.title("📈 ASEAN Exchange Rate Analysis")
st.markdown("""
Aplikasi ini menampilkan **analisis nilai tukar negara ASEAN terhadap USD**  
menggunakan data **real-time dari Yahoo Finance**.

Fitur:
- Data otomatis update sampai hari ini  
- Pilih negara  
- Pilih periode waktu  
- Pilih frekuensi (harian / bulanan / tahunan)  
- Grafik interaktif  
- Return, volatilitas, dan korelasi  
""")

# ======================
# TICKER LIST
# ======================
tickers = {
    "Indonesia (IDR)": "IDRUSD=X",
    "Malaysia (MYR)": "MYRUSD=X",
    "Thailand (THB)": "THBUSD=X",
    "Philippines (PHP)": "PHPUSD=X"
}

# ======================
# SIDEBAR
# ======================
st.sidebar.header("⚙️ Pengaturan")

selected_countries = st.sidebar.multiselect(
    "Pilih negara:",
    list(tickers.keys()),
    default=list(tickers.keys())[:3]
)

period = st.sidebar.selectbox(
    "Pilih rentang waktu:",
    ["1y", "3y", "5y", "10y", "max"],
    index=2
)

frequency = st.sidebar.radio(
    "Frekuensi data:",
    ["Harian", "Bulanan", "Tahunan"]
)

analysis_type = st.sidebar.radio(
    "Jenis Analisis:",
    [
        "Level Nilai Tukar",
        "Return",
        "Volatilitas",
        "Korelasi",
        "Tabel Data"
    ]
)

# ======================
# DOWNLOAD DATA
# ======================
@st.cache_data
def load_data(tickers, period):
    data = yf.download(
        list(tickers.values()),
        period=period,
        auto_adjust=True
    )["Close"]
    return data

raw_df = load_data(tickers, period)

# Rename kolom ke nama negara
raw_df.columns = list(tickers.keys())

# ======================
# RESAMPLING
# ======================
if frequency == "Bulanan":
    df = raw_df.resample("M").last()
elif frequency == "Tahunan":
    df = raw_df.resample("Y").last()
else:
    df = raw_df.copy()

# ======================
# HITUNG RETURN
# ======================
return_df = np.log(df / df.shift(1))

# ======================
# ======================
# OUTPUT VISUAL
# ======================
# ======================

# ===== LEVEL NILAI TUKAR =====
if analysis_type == "Level Nilai Tukar":
    st.subheader("📊 Level Nilai Tukar terhadap USD")

    fig = px.line(
        df[selected_countries],
        title="Pergerakan Nilai Tukar",
        labels={
            "value": "Nilai Tukar",
            "index": "Waktu",
            "variable": "Negara"
        }
    )

    fig.update_layout(hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

    st.info("""
📘 **Cara membaca grafik:**
- Garis naik → depresiasi terhadap USD  
- Garis turun → apresiasi  
- Perbedaan level menunjukkan kekuatan relatif mata uang  
""")

# ===== RETURN =====
elif analysis_type == "Return":
    st.subheader("📉 Return Nilai Tukar")

    fig = px.line(
        return_df[selected_countries],
        title="Return Nilai Tukar",
        labels={
            "value": "Log Return",
            "index": "Waktu",
            "variable": "Negara"
        }
    )

    fig.add_hline(y=0, line_dash="dash")
    fig.update_layout(hovermode="x unified")

    st.plotly_chart(fig, use_container_width=True)

    st.info("""
📘 **Interpretasi Return:**
- Return > 0 → mata uang melemah (depresiasi)
- Return < 0 → mata uang menguat (apresiasi)
- Fluktuasi tajam → ketidakstabilan ekonomi / shock eksternal
""")

# ===== VOLATILITAS =====
elif analysis_type == "Volatilitas":
    st.subheader("📊 Volatilitas Nilai Tukar")

    volatility = return_df[selected_countries].std()

    vol_df = pd.DataFrame({
        "Negara": volatility.index,
        "Volatilitas": volatility.values
    })

    fig = px.bar(
        vol_df,
        x="Negara",
        y="Volatilitas",
        title="Perbandingan Volatilitas Nilai Tukar"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(vol_df)

    st.info("""
📘 **Makna volatilitas:**
- Semakin besar → nilai tukar makin tidak stabil  
- Risiko ekonomi & investasi lebih tinggi  
""")

# ===== KORELASI =====
elif analysis_type == "Korelasi":
    st.subheader("🔗 Korelasi Return Antar Negara")

    corr = return_df[selected_countries].corr()

    fig = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale="RdBu",
        title="Matriks Korelasi Return"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(corr)

    st.info("""
📘 **Makna korelasi:**
- Mendekati +1 → pergerakan searah  
- Mendekati -1 → berlawanan arah  
- Mendekati 0 → tidak berkaitan  
""")

# ===== TABEL DATA =====
elif analysis_type == "Tabel Data":
    st.subheader("📋 Data Nilai Tukar")

    st.dataframe(df[selected_countries])

    st.caption("Data bersumber dari Yahoo Finance dan diperbarui otomatis.")
