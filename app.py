import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

import numpy as np

# Hitung log return harian

df_numeric = df.apply(pd.to_numeric, errors="coerce")
return_df = np.log(df_numeric / df_numeric.shift(1)).dropna()


st.sidebar.header("⚙️ Pengaturan")

countries = df.columns.tolist()

selected_countries = st.sidebar.multiselect(
    "Pilih negara",
    countries,
    default=countries[:3]
)

analysis_type = st.sidebar.radio(
    "Pilih Analisis",
    ["Level Nilai Tukar", "Return Harian", "Volatilitas"]
)

st.subheader("Pergerakan Nilai Tukar")

fig, ax = plt.subplots()

for country in selected_countries:
    ax.plot(df_numeric.index, df_numeric[country], label=country)


ax.set_xlabel("Waktu")
ax.set_ylabel("Nilai Tukar")
ax.legend()

st.pyplot(fig)

if analysis_type == "Return Harian":
    st.subheader("📉 Return Harian Nilai Tukar")

    fig, ax = plt.subplots()
    for country in selected_countries:
        ax.plot(return_df.index, return_df[country], label=country)

    ax.legend()
    ax.set_ylabel("Log Return")
    st.pyplot(fig)

if analysis_type == "Volatilitas":
    st.subheader("📊 Volatilitas Nilai Tukar")

    volatility = return_df[selected_countries].std()

    st.write("Standar deviasi return harian:")
    st.dataframe(volatility)

    fig, ax = plt.subplots()
    volatility.plot(kind="bar", ax=ax)
    ax.set_ylabel("Volatilitas")
    st.pyplot(fig)



