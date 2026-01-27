import streamlit as st

# --- 1. KONFIGURACJA STRONY ---
st.set_page_config(
    page_title="Panel Specjalisty",
    page_icon="🔬",
    layout="centered"
)

# --- 2. STYLE CSS ---
st.markdown("""
    <style>
    /* 1. Obniżenie tytułu, żeby nie ucinało ikonki */
    .block-container { 
        padding-top: 3.5rem !important; 
        padding-bottom: 3rem !important; 
    }
    
    /* Nagłówki */
    h1 { color: #00BFFF !important; text-align: center; margin-bottom: 5px !important; font-size: 36px !important; }
    h2 { color: #FFA500 !important; font-size: 24px !important; margin-bottom: 5px !important; }
    
    /* Styl nagłówka 'Materiały pomocnicze' i 'Uzysk' - żeby były identyczne */
    .custom-header {
        font-size: 22px !important;
        font-weight: 600 !important;
        color: white !important;
        margin-bottom: 10px !important;
        padding-top: 10px !important;
    }
    
    /* Zmniejszenie odstępów */
    div[data-testid="stExpander"] { margin-bottom: 5px !important; }
    .stMarkdown { margin-bottom: -5px !important; }
    
    /* Karty wyników */
    .result-box { 
        background-color: #28a745; color: white; padding: 10px; 
        border-radius: 10px; text-align: center; margin-top: 5px; margin-bottom: 5px;
    }
    .result-val { font-size: 30px !important; font-weight: 800; }
    
    /* Styl suwaków i inputów */
    .stNumberInput input { height: 50px !important; font-size: 22px !important; color: #1f77b4 !important; }
    /* Bardzo mały margines pod suwakami */
    .stSlider [data-baseweb="slider"] { margin-bottom: 5px !important; }
    
    /* Przycisk Reset - Efekty */
    div.stButton > button {
        background-color: #FFD700 !important; color: black !important;
        font-size: 20px !important; font-weight: bold !important; border-radius: 12px !important; border: none !important;
        transition: all 0.1s ease-in-out; /* Płynne przejście */
    }
    /* Efekt wciśnięcia */
    div.stButton > button:active {
        transform: scale(0.95) !important; /* Zmniejszenie przycisku */
        background-color: #e6c200 !important; /* Lekkie przyciemnienie */
    }
    
    /* Zakładki */
    .stTabs [data-baseweb="tab-list"] { gap: 5px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #333; border-radius: 10px; color: white; padding: 10px; }
    .stTabs [aria-selected="true"] { background-color: #00BFFF !important; color: black !important; }
    
    hr { margin-top: 5px !important; margin-bottom: 5px !important; border-color: #555; }
    </style>
""", unsafe_allow_html=True)

st.title("🔬 Panel Specjalisty 3.2")

# --- 3. LOGIKA PAMIĘCI ---
if 'topseed_val' not in st.session_state: st.session_state.topseed_val = 8.5
if 'kubek_val' not in st.session_state: st.session_state.kubek_val = 4.0
if 'last_masa' not in st.session_state: st.session_state.last_masa = 1100.0

# --- 4. ZAKŁADKI ---
tab1, tab2 = st.tabs(["⚖️ 1. ZAPRAWA (Mg)", "📊 2. KOREKTA SKŁADU"])

# ==============================================================================
# ZAKŁADKA 1: KALKULATOR ZAPRAWY
# ==============================================================================
with tab1:
    zaprawy_db = {
        "Zap. FeSiMg - VL 63": {"Mg": 6.5, "Si": 0.45},
        "Zap. FeSiMg - VL 63 (0) - zerówka": {"Mg": 6.5, "Si": 0.47},
        "Zap. FeSiMg - 611A": {"Mg": 6.45, "Si": 0.4505},
        "Zap. NiMg16": {"Mg": 16.63, "Si": 0.0063},
        "Zap. FeSiMg - LAMET 5504": {"Mg": 5.57, "Si": 0.47},
        "Zap. FeSiMg - ELMAG": {"Mg": 9.17, "Si": 0.46}
    }

    col_a, col_b = st.columns(2)
    with col_a:
        masa = st.number_input("Masa metalu [Kg]:", value=1100, step=50, key="masa_zaprawa")
        temp = st.number_input("Temp. spustu [oC]:", value=1480, step=10, key="temp_zaprawa")
    with col_b:
        target_mg = st.number_input("Cel Mg [%]:", value=0.045, step=0.005, format="%.3f")
        siarka = st.number_input("Siarka [%]:", value=0.010, step=0.001, format="%.3f")
    
    wybrana = st.selectbox("Rodzaj zaprawy:", list(zaprawy_db.keys()))
    
    # Ujednolicony nagłówek dla Uzysku
    st.markdown('<div class="custom-header">Zakładany Uzysk Mg [%]:</div>', unsafe_allow_html=True)
    uzysk_custom = st.slider("", 45, 75, value=60, step=1, label_visibility="collapsed")

    # Logika resetu
    proporcja = masa / 1100
    domyslny_topseed = max(4.0, min(12.0, round((8.8 * proporcja) * 2) / 2))
    domyslny_kubek = max(1.0, min(6.0, round((4.0 * proporcja) * 2) / 2))

    if masa != st.session_state.last_masa:
        st.session_state.topseed_val = domyslny_topseed
        st.session_state.kubek_val = domyslny_kubek
        st.session_state.last_masa = masa

    # Obliczenia
    mg_sklad = zaprawy_db[wybrana]["Mg"]
    si_sklad_zap = zaprawy_db[wybrana]["Si"]
    komponent_mg = (target_mg + 0.76 * (siarka - 0.01) + 0.007)
    ilosc_zaprawy = (masa * (komponent_mg / (mg_sklad * uzysk_custom)) * (temp / 1450)) * 100

    st.markdown("---")
    
    # Ujednolicony nagłówek dla Materiałów
    st.markdown('<div class="custom-header">Materiały pomocnicze:</div>', unsafe_allow_html=True)
    
    topseed_kg = st.slider("Topseed [Kg]:", 4.0, 12.0, value=st.session_state.topseed_val, step=0.5)
    st.session_state.topseed_val = topseed_kg
    
    kubek_kg = st.slider("Modyfikacja do kubka [Kg]:", 1.0, 6.0, value=st.session_state.kubek_val, step=0.5)
    st.session_state.kubek_val = kubek_kg

    # Przycisk na całą szerokość z efektem wciśnięcia
    if st.button("🔄 RESETUJ SUGEROWANE", use_container_width=True):
        st.session_state.topseed_val = domyslny_topseed
        st.session_state.kubek_val = domyslny_kubek
        st.rerun()

    si_z_zaprawy = (ilosc_zaprawy * si_sklad_zap) / masa * 100
    si_z_topseed = (topseed_kg * 0.485) / masa * 100
    si_z_kubka = (kubek_kg * 0.7496) / masa * 100
    total_si_inc = si_z_zaprawy + si_z_topseed + si_z_kubka

    st.markdown(f'<div class="result-box"><div style="font-size: 20px;">ILOŚĆ ZAPRAWY (Uzysk {uzysk_custom}%)</div><div class="result-val">{ilosc_zaprawy:.1f} kg</div></div>', unsafe_allow_html=True)
    st.info(f"PRZEWIDYWANY PRZYROST Si: +{total_si_inc:.2f}%")


# ==============================================================================
# ZAKŁADKA 2: KOREKTA SKŁADU
# ==============================================================================
with tab2:
    st.markdown("### 1. Parametry wsadu")
    masa_korekta = st.number_input("Aktualna masa metalu w piecu/kadzi [Kg]:", value=2300, step=50, key="masa_kor")
    
    def oblicz_korkte(masa, obecna, cel, sklad_dodatku):
        if cel == obecna: return 0.0
        if sklad_dodatku == cel: return 0.0
        wynik = masa * (cel - obecna) / (sklad_dodatku - cel)
        return wynik

    st.markdown("---")
    st.markdown("### 2. Wybierz korektę")

    with st.expander("⚫ WĘGIEL (C) - Nawęglanie", expanded=False):
        c1, c2, c3 = st.columns(3)
        obecne_c = c1.number_input("Obecny C [%]:", 0.00, 5.00, 3.64, 0.01, format="%.2f")
        cel_c = c2.number_input("Cel C [%]:", 0.00, 5.00, 3.70, 0.01, format="%.2f")
        wsad_c = c3.number_input("C w dodatku [%]:", 0.0, 100.0, 70.0, 1.0)
        
        if cel_c > obecne_c:
            wynik_c = oblicz_korkte(masa_korekta, obecne_c, cel_c, wsad_c)
            st.markdown(f'<div class="result-box">DODAJ NAWĘGLACZA:<br><span class="result-val">{wynik_c:.2f} kg</span></div>', unsafe_allow_html=True)
        elif cel_c < obecne_c:
            st.warning("Cel mniejszy niż obecna! Zjedź niżej do sekcji 'Zbijanie Węgla'.")
        else:
            st.success("Skład OK.")

    with st.expander("🪨 KRZEM (Si) - Żelazokrzem", expanded=False):
        s1, s2, s3 = st.columns(3)
        obecne_si = s1.number_input("Obecny Si [%]:", 0.00, 5.00, 1.80, 0.05, format="%.2f")
        cel_si = s2.number_input("Cel Si [%]:", 0.00, 5.00, 2.00, 0.05, format="%.2f")
        wsad_si = s3.number_input("Si w dodatku [%]:", 0.0, 100.0, 75.0, 1.0)
        
        if cel_si > obecne_si:
            wynik_si = oblicz_korkte(masa_korekta, obecne_si, cel_si, wsad_si)
            st.markdown(f'<div class="result-box">DODAJ FeSi:<br><span class="result-val">{wynik_si:.2f} kg</span></div>', unsafe_allow_html=True)
        else:
            st.info("Skład OK.")

    with st.expander("🟠 MIEDŹ (Cu)", expanded=False):
        col1, col2, col3 = st.columns(3)
        cu_curr = col1.number_input("Obecna Cu [%]:", 0.00, 2.00, 0.06, 0.01)
        cu_dest = col2.number_input("Cel Cu [%]:", 0.00, 2.00, 0.72, 0.01)
        cu_cont = col3.number_input("Cu w dodatku [%]:", 0.0, 100.0, 99.0, 1.0)
        
        if cu_dest > cu_curr:
            res_cu = oblicz_korkte(masa_korekta, cu_curr, cu_dest, cu_cont)
            st.markdown(f'<div class="result-box">DODAJ MIEDZI:<br><span class="result-val">{res_cu:.2f} kg</span></div>', unsafe_allow_html=True)
        else:
            st.success("Skład OK.")

    with st.expander("⚪ NIKIEL (Ni)", expanded=False):
        col1, col2, col3 = st.columns(3)
        ni_curr = col1.number_input("Obecny Ni [%]:", 0.00, 5.00, 2.13, 0.01)
        ni_dest = col2.number_input("Cel Ni [%]:", 0.00, 5.00, 2.40, 0.01)
        ni_cont = col3.number_input("Ni w dodatku [%]:", 0.0, 100.0, 99.0, 1.0)
        
        if ni_dest > ni_curr:
            res_ni = oblicz_korkte(masa_korekta, ni_curr, ni_dest, ni_cont)
            st.markdown(f'<div class="result-box">DODAJ NIKLU:<br><span class="result-val">{res_ni:.2f} kg</span></div>', unsafe_allow_html=True)
        else:
            st.success("Skład OK.")

    with st.expander("🟣 MOLIBDEN (Mo)", expanded=False):
        col1, col2, col3 = st.columns(3)
        mo_curr = col1.number_input("Obecny Mo [%]:", 0.00, 5.00, 0.00, 0.01)
        mo_dest = col2.number_input("Cel Mo [%]:", 0.00, 5.00, 0.20, 0.01)
        mo_cont = col3.number_input("Mo w dodatku [%]:", 0.0, 100.0, 69.0, 1.0)
        
        if mo_dest > mo_curr:
            res_mo = oblicz_korkte(masa_korekta, mo_curr, mo_dest, mo_cont)
            st.markdown(f'<div class="result-box">DODAJ FeMo:<br><span class="result-val">{res_mo:.2f} kg</span></div>', unsafe_allow_html=True)
        else:
            st.success("Skład OK.")

    st.markdown("---")
    
    with st.expander("📉 ZBIJANIE WĘGLA (Dodatek Stali)", expanded=False):
        c1, c2, c3 = st.columns(3)
        c_zb_curr = c1.number_input("Aktualny C [%]:", 0.0, 5.0, 3.90, 0.01, key="czb_cur")
        c_zb_dest = c2.number_input("Cel C [%]:", 0.0, 5.0, 3.73, 0.01, key="czb_dest")
        c_zb_stal = c3.number_input("C w Złomie [%]:", 0.0, 2.0, 0.10, 0.01, key="czb_stal")
        
        if c_zb_dest < c_zb_curr:
            res_stal = oblicz_korkte(masa_korekta, c_zb_curr, c_zb_dest, c_zb_stal)
            st.markdown(f'<div class="result-box" style="background-color: #dc3545;">DODAJ STALI:<br><span class="result-val">{res_stal:.1f} kg</span></div>', unsafe_allow_html=True)
        else:
            st.info("Aby podnieść węgiel, użyj pierwszej sekcji (Nawęglanie).")

    st.markdown("---")
    
    with st.expander("🔄 SYMULACJA MIESZANIA (Średnia ważona)", expanded=False):
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            m1_mass = st.number_input("Masa 1 [kg]:", 0, 10000, 1000)
            m1_pct = st.number_input("Skład 1 [%]:", 0.0, 100.0, 3.5, key="m1p")
        with col_m2:
            m2_mass = st.number_input("Masa 2 [kg]:", 0, 10000, 500)
            m2_pct = st.number_input("Skład 2 [%]:", 0.0, 100.0, 3.8, key="m2p")
            
        if (m1_mass + m2_mass) > 0:
            wynik_mix = (m1_mass * m1_pct + m2_mass * m2_pct) / (m1_mass + m2_mass)
            st.markdown(f"**Wynikowy skład chemiczny:**")
            st.markdown(f'<div style="font-size: 40px; color: yellow; text-align: center; font-weight: bold;">{wynik_mix:.3f} %</div>', unsafe_allow_html=True)
