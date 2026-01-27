import streamlit as st

# --- 1. LOGIKA PAMIĘCI (Session State) ---
if 'topseed_val' not in st.session_state:
    st.session_state.topseed_val = 8.5
if 'kubek_val' not in st.session_state:
    st.session_state.kubek_val = 4.0
if 'last_masa' not in st.session_state:
    st.session_state.last_masa = 1100.0

# --- 2. LAYOUT I STYLE CSS ---
st.markdown("""
    <style>
    .block-container { padding-top: 3rem !important; padding-bottom: 7rem !important; }
    div[data-testid="stVerticalBlock"] > div { margin-top: -7px !important; padding-top: 0px !important; }
    h1 { font-size: 50px !important; color: #00BFFF !important; text-align: center; margin-bottom: 0px !important; padding-bottom: 15px !important; }
    h3 { font-size: 30px !important; color: white !important; margin-bottom: 0px !important; padding-bottom: 10px !important; padding-top: 10px; }
    html, body, [class*="st-"] { font-size: 20px !important; font-weight: 600; }
    
    /* Styl suwaków dla lepszej widoczności */
    .stSlider [data-baseweb="slider"] { margin-bottom: 20px; }
    
    .stNumberInput input { height: 75px !important; font-size: 32px !important; color: #1f77b4 !important; }
    .result-box { background-color: #28a745; color: white; padding: 15px; border-radius: 15px; text-align: center; margin-bottom: 15px; }
    .result-val { font-size: 50px !important; font-weight: 800; }
    .si-box { background-color: #333333; color: #00ff00; padding: 15px; border-radius: 12px; text-align: center; margin-bottom: 10px; }
    hr { margin-top: 0px !important; margin-bottom: 0px !important; }

    /* ŻÓŁTY PRZYCISK RESETU */
    div.stButton > button {
        width: 100% !important; height: 60px !important; background-color: #FFD700 !important; color: black !important;
        font-size: 22px !important; font-weight: bold !important; border-radius: 15px !important;
        border: none !important; margin-top: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🔬 Panel Specjalisty 2.0")

# --- 3. BAZA DANYCH ---
zaprawy_db = {
    "Zap. FeSiMg - VL 63": {"Mg": 6.5, "Si": 0.45},
    "Zap. FeSiMg - VL 63 (0) - zerówka": {"Mg": 6.5, "Si": 0.47},
    "Zap. FeSiMg - 611A": {"Mg": 6.45, "Si": 0.4505},
    "Zap. NiMg16": {"Mg": 16.63, "Si": 0.0063},
    "Zap. FeSiMg - LAMET 5504": {"Mg": 5.57, "Si": 0.47},
    "Zap. FeSiMg - ELMAG": {"Mg": 9.17, "Si": 0.46}
}

# --- 4. WEJŚCIE DANYCH GŁÓWNYCH ---
masa = st.number_input("Ilość metalu w kadzi [Kg]:", value=1100, step=20)
temp = st.number_input("Temperatura spustu [oC]:", value=1480, step=10)
target_mg = st.number_input("Magnez końcowy [%]:", value=0.045, step=0.005, format="%.3f")
siarka = st.number_input("Siarka techniczna [%]:", value=0.010, step=0.001, format="%.3f")
wybrana = st.selectbox("Wybierz zaprawę:", list(zaprawy_db.keys()))

# --- 10. NOWOŚĆ: SUWAK UZYSKU ---
st.subheader("⚙️ Zakładany Uzysk Procesowy")
uzysk_custom = st.slider("Uzysk Mg [%]:", 45, 75, value=60, step=1)

# --- 5. LOGIKA OBLICZEŃ DOMYŚLNYCH ---
proporcja = masa / 1100
domyslny_topseed = max(4.0, min(12.0, round((8.8 * proporcja) * 2) / 2))
domyslny_kubek = max(1.0, min(6.0, round((4.0 * proporcja) * 2) / 2))

if masa != st.session_state.last_masa:
    st.session_state.topseed_val = domyslny_topseed
    st.session_state.kubek_val = domyslny_kubek
    st.session_state.last_masa = masa

# --- 6. OBLICZENIA METALURGICZNE ---
mg_sklad = zaprawy_db[wybrana]["Mg"]
si_sklad_zap = zaprawy_db[wybrana]["Si"]
komponent_mg = (target_mg + 0.76 * (siarka - 0.01) + 0.007)

# Używamy uzysk_custom z suwaka zamiast stałego 60.0
ilosc_zaprawy = (masa * (komponent_mg / (mg_sklad * uzysk_custom)) * (temp / 1450)) * 100

# --- 7. MATERIAŁY POMOCNICZE (SUWAKI) ---
st.divider()
st.subheader("Materiały pomocnicze (symulacja):")

topseed_kg = st.slider("Topseed [Kg]:", 4.0, 12.0, value=st.session_state.topseed_val, step=0.5)
st.session_state.topseed_val = topseed_kg

kubek_kg = st.slider("Modyfikacja do kubka [Kg]:", 1.0, 6.0, value=st.session_state.kubek_val, step=0.5)
st.session_state.kubek_val = kubek_kg

# --- 8. ŻÓŁTY PRZYCISK RESETU ---
if st.button("🔄 RESETUJ DO USTAWIEŃ DOMYŚLNYCH", use_container_width=True):
    st.session_state.topseed_val = domyslny_topseed
    st.session_state.kubek_val = domyslny_kubek
    st.rerun()

# --- 9. OBLICZENIA KRZEMU I WYNIKI ---
si_z_zaprawy = (ilosc_zaprawy * si_sklad_zap) / masa * 100
si_z_topseed = (topseed_kg * 0.485) / masa * 100
si_z_kubka = (kubek_kg * 0.7496) / masa * 100
total_si_inc = si_z_zaprawy + si_z_topseed + si_z_kubka

st.markdown(f"""
    <div class="result-box">
        <div style="font-size: 25px;">ILOŚĆ ZAPRAWY (Uzysk {uzysk_custom}%)</div>
        <div class="result-val">{ilosc_zaprawy:.1f} kg</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f"""
    <div class="si-box">
        <div style="color: white; font-size: 20px;">PRZEWIDYWANY PRZYROST Si:</div>
        <div style="font-size: 40px; font-weight: 800;">{total_si_inc:.2f} %</div>
    </div>
    """, unsafe_allow_html=True)
