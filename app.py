import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ======================
# LOAD DATA
# ======================
df = pd.read_csv(
    "data/exchange_rate.csv",
    index_col=0,
    parse_dates=True
)

df = df.apply(pd.to_numeric, errors="coerce")
returns = df.pct_change() * 100

# ======================
# UI
# ======================
st.title("Analisis Nilai Tukar Harian ASEAN terhadap USD (2000–2024)")

# ⬅️ COUNTRY HARUS DI SINI
country = st.selectbox(
    "Pilih Negara",
    df.columns.tolist()
)

# ======================
# GRAFIK LEVEL
# ======================
st.subheader(f"Pergerakan Nilai Tukar {country}")

fig, ax = plt.subplots()
ax.plot(df.index, df[country])
ax.set_xlabel("Tanggal")
ax.set_ylabel("Nilai Tukar terhadap USD")
st.pyplot(fig)

# ======================
# GRAFIK RETURN
# ======================
st.subheader(f"Return Harian {country}")

fig2, ax2 = plt.subplots()
ax2.plot(returns.index, returns[country])
ax2.axhline(0)
ax2.set_ylabel("Return (%)")
st.pyplot(fig2)

# ======================
# INTERPRETASI
# ======================
st.markdown("""
### Interpretasi Ekonomi

- **Kenaikan nilai tukar** menunjukkan depresiasi mata uang domestik terhadap USD  
- **Lonjakan return** mencerminkan meningkatnya volatilitas, terutama saat krisis global  
- Negara dengan **volatilitas rendah** cenderung memiliki stabilitas makroekonomi yang lebih baik
""")
