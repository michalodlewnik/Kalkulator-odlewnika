import streamlit as st

# Styl powiększający czcionkę i pola dla wytapiaczy
st.markdown("""
    <style>
    html, body, [class*="st-"] {font-size: 20px !important;}
    input {height: 60px !important; font-size: 25px !important;}
    .stNumberInput div[data-baseweb="input"] {height: 60px !important;}
    </style>
    """, unsafe_allow_html=True)

st.title("⚖️ Kalkulator Zaprawy - Odlewnie Polskie")

# Baza zapraw uzupełniona o 'zerówkę'
zaprawy_db = {
    "Zap. FeSiMg - VL 63": {"Mg": 0.065, "Si": 0.45},
    "Zap. FeSiMg - VL 63 (0) - zerówka": {"Mg": 0.065, "Si": 0.47},
    "Zap. FeSiMg - 611A": {"Mg": 0.0645, "Si": 0.4505},
    "Zap. NiMg16": {"Mg": 0.1663, "Si": 0.0063},
    "Zap. FeSiMg - LAMET 5504": {"Mg": 0.0557, "Si": 0.47}
}

# 1. Dane wejściowe z Twoimi krokami +/-
masa = st.number_input("Masa metalu [kg]:", value=1100, step=5) # Krok 5kg
wybrana = st.selectbox("Rodzaj zaprawy:", list(zaprawy_db.keys()))
temp = st.number_input("Temperatura spustu [°C]:", value=1470, step=10) # Krok 10°C
target_mg = st.number_input("Docelowy Mg końcowy [%]:", value=0.045, step=0.005, format="%.3f") # Krok 0.005
siarka = st.number_input("Siarka techniczna [%]:", value=0.010, step=0.001, format="%.3f") # Krok 0.001
nowa_kadz = st.checkbox("NOWA KADŹ (+10% zaprawy)")

# 2. Logika obliczeń dokładnie z Twojego Excela
# Formuła: Masa * (Mg_target + S_tech) / (Mg_sklad * 0.68)
mg_sklad = zaprawy_db[wybrana]["Mg"]
si_sklad = zaprawy_db[wybrana]["Si"]
uzysk = 0.68 # Przyjęty współczynnik z Twojego arkusza

ilosc_zaprawy = (masa * (target_mg + siarka)) / (mg_sklad * uzysk)
if nowa_kadz:
    ilosc_zaprawy *= 1.1

# Wyniki pomocnicze
proporcja = masa / 1100
topseed = 8.8 * proporcja
kubek = 4.0 * proporcja # Modyfikacja do kubka
przyrost_si = (ilosc_zaprawy * si_sklad) / masa * 100

# 3. Wyświetlanie wyników
st.divider()
st.error(f"ILOŚĆ ZAPRAWY: {ilosc_zaprawy:.2f} kg")

c1, c2 = st.columns(2)
with c1:
    st.metric("Topseed", f"{topseed:.2f} kg")
    st.metric("Przyrost Si", f"{przyrost_si:.2f} %")
with c2:
    st.metric("Mod. do kubka", f"{kubek:.2f} kg") # Dodano zgodnie z Twoją prośbą
