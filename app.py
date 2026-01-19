import streamlit as st

# 1. STYLE CSS - MAKSYMALNA CZYTELNOŚĆ I KOLORY
st.markdown("""
    <style>
    html, body, [class*="st-"] { font-size: 22px !important; font-weight: 600; }
    .stNumberInput input { height: 90px !important; font-size: 38px !important; color: #1f77b4 !important; }
    
    /* Zielone tło dla głównego wyniku */
    .result-box { 
        background-color: #28a745; color: white; padding: 25px; 
        border-radius: 15px; text-align: center; margin-bottom: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    .result-val { font-size: 60px !important; font-weight: 800; }
    
    /* Szare tło dla dodatków */
    .detail-box { 
        background-color: #444444; color: #ffffff; padding: 20px; 
        border-radius: 12px; margin: 10px 0; text-align: center;
    }
    .detail-val { font-size: 32px; color: #00ff00; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚖️ Kalkulator zaprawy 1.0")

# 2. BAZA ZAPRAW (Dane z Excela)
zaprawy_db = {
    "Zap. FeSiMg - VL 63": {"Mg": 6.5, "Si": 0.45},
    "Zap. FeSiMg - VL 63 (0) - zerówka": {"Mg": 6.5, "Si": 0.47},
    "Zap. FeSiMg - 611A": {"Mg": 6.45, "Si": 0.4505},
    "Zap. NiMg16": {"Mg": 16.63, "Si": 0.0063},
    "Zap. FeSiMg - LAMET 5504": {"Mg": 5.57, "Si": 0.47}
}

# 3. WEJŚCIE DANYCH - KOLEJNOŚĆ WG PROŚBY
masa = st.number_input("Ilość metalu w kadzi [Kg]:", value=1100, step=5)
temp = st.number_input("Temperatura spustu [oC]:", value=1470, step=10)
target_mg = st.number_input("Magnez końcowy [%]:", value=0.045, step=0.005, format="%.3f")
siarka = st.number_input("Siarka techniczna [%]:", value=0.010, step=0.001, format="%.3f")
wybrana = st.selectbox("Wybierz zaprawę:", list(zaprawy_db.keys()))
nowa_kadz = st.checkbox("🔥 NOWA KADŹ (+10%)")

# 4. LOGIKA I TWOJA FORMUŁA
uzysk = 60.0  # Skalibrowane pod Twój Excel
mg_sklad = zaprawy_db[wybrana]["Mg"]
si_sklad_zap = zaprawy_db[wybrana]["Si"]

# Formuła z Twojej wiadomości
komponent_mg = (target_mg + 0.76 * (siarka - 0.01) + 0.007)
ilosc_zaprawy = (masa * (komponent_mg / (mg_sklad * uzysk)) * (temp / 1450)) * 100

if nowa_kadz:
    ilosc_zaprawy *= 1.1

# Dodatki zaokrąglone do 0.5 kg
proporcja = masa / 1100
topseed_kg = round((8.8 * proporcja) * 2) / 2
kubek_kg = round((4.0 * proporcja) * 2) / 2

# Obliczenie całkowitego przyrostu Si (Zaprawa + Topseed + Kubek)
# Si z Topseed (48.5%) i Kubek (SYBA - 74.96%)
si_z_zaprawy = (ilosc_zaprawy * si_sklad_zap) / masa * 100
si_z_topseed = (topseed_kg * 0.485) / masa * 100
si_z_kubka = (kubek_kg * 0.7496) / masa * 100
total_si_inc = si_z_zaprawy + si_z_topseed + si_z_kubka

# 5. WYNIKI - WIZUALIZACJA
st.markdown(f"""
    <div class="result-box">
        <div>ILOŚĆ ZAPRAWY</div>
        <div class="result-val">{ilosc_zaprawy:.2f} kg</div>
    </div>
    """, unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f'<div class="detail-box">Topseed [Kg]<br><span class="detail-val">{topseed_kg:.1f}</span></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="detail-box">Mod. do kubka [Kg]<br><span class="detail-val">{kubek_kg:.1f}</span></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="detail-box">Przyrost Si [%]<br><span class="detail-val">{total_si_inc:.2f}</span></div>', unsafe_allow_html=True)

# Przycisk do szybkiego czyszczenia/resetu (opcjonalnie)
if st.button("RESETUJ DANE"):
    st.rerun()
