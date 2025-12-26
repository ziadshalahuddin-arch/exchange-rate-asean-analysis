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
## 📌 Pendahuluan
Aplikasi ini menampilkan **analisis nilai tukar negara ASEAN terhadap USD**  
menggunakan data **real-time dari Yahoo Finance**.

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
- Data otomatis update sampai hari ini  
- Pilih negara  
- Pilih periode waktu  
- Pilih frekuensi (harian / bulanan / tahunan)  
- Grafik interaktif  
- Return, volatilitas, dan korelasi  
""")

import plotly.express as px

st.subheader("🗺️ Peta Interaktif Negara ASEAN")

# Data koordinat + nama negara ASEAN
asean_map_data = {
    "country": [
        "Indonesia", "Malaysia", "Thailand", "Philippines",
        "Vietnam", "Singapore", "Cambodia",
        "Laos", "Myanmar", "Brunei"
    ],
    "lat": [ -2.5, 4.2, 15.8, 12.8, 14.1, 1.35, 12.6, 19.8, 21.9, 4.5 ],
    "lon": [118.0, 102.0, 100.9, 121.8, 108.3, 103.8, 104.9, 102.6, 95.9, 114.7]
}

map_df = pd.DataFrame(asean_map_data)

fig_map = px.scatter_geo(
    map_df,
    lat="lat",
    lon="lon",
    text="country",
    hover_name="country",
    scope="asia",
    projection="natural earth",
)

fig_map.update_traces(marker=dict(size=12, color="red"))
fig_map.update_layout(
    height=500,
    margin=dict(l=0, r=0, t=0, b=0),
)

st.plotly_chart(fig_map, use_container_width=True)

# ======================
# TICKER LIST
# ======================
tickers = {
    "Indonesia 
    import plotly.express as px

st.subheader("🗺️ Peta Interaktif Negara ASEAN")

# Data koordinat + nama negara ASEAN
asean_map_data = {
    "country": [
        "Indonesia", "Malaysia", "Thailand", "Philippines",
        "Vietnam", "Singapore", "Cambodia",
        "Laos", "Myanmar", "Brunei"
    ],
    "lat": [ -2.5, 4.2, 15.8, 12.8, 14.1, 1.35, 12.6, 19.8, 21.9, 4.5 ],
    "lon": [118.0, 102.0, 100.9, 121.8, 108.3, 103.8, 104.9, 102.6, 95.9, 114.7]
}

map_df = pd.DataFrame(asean_map_data)

fig_map = px.scatter_geo(
    map_df,
    lat="lat",
    lon="lon",
    text="country",
    hover_name="country",
    scope="asia",
    projection="natural earth",
)

fig_map.update_traces(marker=dict(size=12, color="red"))
fig_map.update_layout(
    height=500,
    margin=dict(l=0, r=0, t=0, b=0),
)

st.plotly_chart(fig_map, use_container_width=True)
(IDR)": "IDRUSD=X",
    "Malaysia (MYR)": "MYRUSD=X",
    "Thailand (THB)": "THBUSD=X",
    "Philippines (PHP)": "PHPUSD=X"
}

# ======================
# SIDEBAR
# ======================
if section == "Pendahuluan":
    st.header("📌 Pendahuluan")
    st.write("""
    Aplikasi ini menyajikan analisis nilai tukar negara-negara ASEAN
    terhadap USD menggunakan data harian dari Yahoo Finance.
    """)

elif section == "Peta ASEAN":
    st.header("🗺️ Peta Negara ASEAN")
    # ⬅ tempel kode MAP INTERAKTIF DI SINI

elif section == "Level Nilai Tukar":
    st.header("📈 Level Nilai Tukar")
    # grafik level

elif section == "Return Harian":
    st.header("📉 Return Harian")
    # grafik return

elif section == "Volatilitas":
    st.header("📊 Volatilitas")
    # grafik volatilitas

elif section == "Korelasi":
    st.header("🔗 Korelasi")
    # heatmap korelasi

elif section == "Tabel Data":
    st.header("📋 Data Nilai Tukar")
    st.dataframe(df)

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
