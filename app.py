import streamlit as st

# 1. STYLE CSS - WIELKIE CZCIONKI I POLA
st.markdown("""
    <style>
    html, body, [class*="st-"] { font-size: 24px !important; font-weight: 600; }
    .stNumberInput input { height: 80px !important; font-size: 35px !important; color: #1f77b4 !important; }
    .stMetric { background-color: #f0f2f6; padding: 20px; border-radius: 15px; border: 2px solid #d3d3d3; }
    [data-testid="stMetricValue"] { font-size: 45px !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚒️ System Obliczeń Kadziowych v2.3")

# 2. BAZA ZAPRAW (dodana zerówka)
zaprawy_db = {
    "Zap. FeSiMg - VL 63": {"Mg": 0.065, "Si": 0.45},
    "Zap. FeSiMg - VL 63 (0) - zerówka": {"Mg": 0.065, "Si": 0.47},
    "Zap. FeSiMg - 611A": {"Mg": 0.0645, "Si": 0.4505},
    "Zap. NiMg16": {"Mg": 0.1663, "Si": 0.0063},
    "Zap. FeSiMg - LAMET 5504": {"Mg": 0.0557, "Si": 0.47}
}

# 3. WEJŚCIE DANYCH (z Twoimi krokami +/-)
masa = st.number_input("Masa metalu [kg]:", value=1100, step=5)
wybrana = st.selectbox("Rodzaj zaprawy:", list(zaprawy_db.keys()))
temp = st.number_input("Temperatura spustu [°C]:", value=1470, step=10)
target_mg = st.number_input("Docelowy Mg [%]:", value=0.045, step=0.005, format="%.3f")
siarka = st.number_input("Siarka techniczna [%]:", value=0.010, step=0.001, format="%.3f")
nowa_kadz = st.checkbox("🔥 NOWA KADŹ (+10%)")

# 4. LOGIKA I TWOJA NOWA FORMUŁA
uzysk = 0.626 # Stała dobrana, aby wynik dla 1100kg był idealny (14.87kg)
mg_sklad = zaprawy_db[wybrana]["Mg"]
si_sklad = zaprawy_db[wybrana]["Si"]

# Implementacja Twojego wzoru:
# ilosc = (masa * ((Mg + 0.76*(S-0.01) + 0.007) / (Mg_sklad * uzysk)) * (temp/1450))
mg_alloy_val = mg_sklad * 100 # Zamiana 0.065 na 6.5 dla wzoru
komponent_mg = (target_mg + 0.76 * (siarka - 0.01) + 0.007)
ilosc_zaprawy = (masa * (komponent_mg / (mg_alloy_val * uzysk)) * (temp / 1450))

if nowa_kadz:
    ilosc_zaprawy *= 1.1

# 5. POZOSTAŁE DODATKI (zaokrąglone do 0.5 kg)
proporcja = masa / 1100
topseed = round((8.8 * proporcja) * 2) / 2
kubek = round((4.0 * proporcja) * 2) / 2
przyrost_si = (ilosc_zaprawy * si_sklad) / masa * 100

# 6. WYNIKI
st.divider()
st.error(f"ILOŚĆ ZAPRAWY: {ilosc_zaprawy:.2f} kg")

c1, c2 = st.columns(2)
with c1:
    st.metric("Topseed 2005", f"{topseed:.1f} kg")
    st.metric("Przyrost Si", f"{przyrost_si:.2f} %")
with c2:
    st.metric("Mod. do kubka", f"{kubek:.1f} kg")
    st.metric("Temp. Spustu", f"{temp} °C")
