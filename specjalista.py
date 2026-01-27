import streamlit as st

# --- 1. KONFIGURACJA STRONY ---
st.set_page_config(
    page_title="Panel Specjalisty",
    page_icon="🔬",
    layout="centered"
)

# --- 2. STYLE CSS (WSPÓLNE DLA OBU ZAKŁADEK) ---
st.markdown("""
    <style>
    .block-container { padding-top: 2rem !important; padding-bottom: 5rem !important; }
    
    /* Styl nagłówków */
    h1 { color: #00BFFF !important; text-align: center; padding-bottom: 10px; font-size: 40px !important; }
    h2 { color: #FFA500 !important; font-size: 28px !important; padding-top: 10px; }
    h3 { color: white !important; font-size: 22px !important; }
    
    /* Karty wyników */
    .result-box { 
        background-color: #28a745; color: white; padding: 15px; 
        border-radius: 10px; text-align: center; margin-bottom: 10px; margin-top: 10px;
    }
    .result-val { font-size: 35px !important; font-weight: 800; }
    
    /* Styl suwaków i inputów */
    .stNumberInput input { height: 60px !important; font-size: 24px !important; color: #1f77b4 !important; }
    .stSlider [data-baseweb="slider"] { margin-bottom: 20px; }
    
    /* Przycisk Reset */
    div.stButton > button {
        width: 100% !important; height: 50px !important; 
        background-color: #FFD700 !important; color: black !important;
        font-size: 20px !important; font-weight: bold !important; border-radius: 12px !important; border: none !important;
    }
    
    /* Zakładki */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { height: 60px; white-space: pre-wrap; background-color: #333; border-radius: 10px; color: white; }
    .stTabs [aria-selected="true"] { background-color: #00BFFF !important; color: black !important; }
    </style>
""", unsafe_allow_html=True)

st.title("🔬 Panel Specjalisty 3.0")

# --- 3. LOGIKA PAMIĘCI (ZAPRAWA) ---
if 'topseed_val' not in st.session_state: st.session_state.topseed_val = 8.5
if 'kubek_val' not in st.session_state: st.session_state.kubek_val = 4.0
if 'last_masa' not in st.session_state: st.session_state.last_masa = 1100.0

# --- 4. TWORZENIE ZAKŁADEK ---
tab1, tab2 = st.tabs(["⚖️ 1. ZAPRAWA (Mg)", "📊 2. KOREKTA SKŁADU"])

# ==============================================================================
# ZAKŁADKA 1: KALKULATOR ZAPRAWY (TWOJA POPRZEDNIA WERSJA)
# ==============================================================================
with tab1:
    st.header("Modyfikacja i Sferoidyzacja")
    
    # Baza danych zapraw
    zaprawy_db = {
        "Zap. FeSiMg - VL 63": {"Mg": 6.5, "Si": 0.45},
        "Zap. FeSiMg - VL 63 (0) - zerówka": {"Mg": 6.5, "Si": 0.47},
        "Zap. FeSiMg - 611A": {"Mg": 6.45, "Si": 0.4505},
        "Zap. NiMg16": {"Mg": 16.63, "Si": 0.0063},
        "Zap. FeSiMg - LAMET 5504": {"Mg": 5.57, "Si": 0.47},
        "Zap. FeSiMg - ELMAG": {"Mg": 9.17, "Si": 0.46}
    }

    # Wejście danych
    col_a, col_b = st.columns(2)
    with col_a:
        masa = st.number_input("Masa metalu [Kg]:", value=1100, step=50, key="masa_zaprawa")
        temp = st.number_input("Temp. spustu [oC]:", value=1480, step=10, key="temp_zaprawa")
    with col_b:
        target_mg = st.number_input("Cel Mg [%]:", value=0.045, step=0.005, format="%.3f")
        siarka = st.number_input("Siarka [%]:", value=0.010, step=0.001, format="%.3f")
    
    wybrana = st.selectbox("Rodzaj zaprawy:", list(zaprawy_db.keys()))
    uzysk_custom = st.slider("Zakładany Uzysk Mg [%]:", 45, 75, value=60, step=1)

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

    # Suwaki materiałów pomocniczych
    st.markdown("---")
    st.subheader("Materiały pomocnicze:")
    topseed_kg = st.slider("Topseed [Kg]:", 4.0, 12.0, value=st.session_state.topseed_val, step=0.5)
    st.session_state.topseed_val = topseed_kg
    
    kubek_kg = st.slider("Modyfikacja do kubka [Kg]:", 1.0, 6.0, value=st.session_state.kubek_val, step=0.5)
    st.session_state.kubek_val = kubek_kg

    # Przycisk Reset
    if st.button("🔄 RESETUJ SUGEROWANE"):
        st.session_state.topseed_val = domyslny_topseed
        st.session_state.kubek_val = domyslny_kubek
        st.rerun()

    # Wyniki Zaprawy
    si_z_zaprawy = (ilosc_zaprawy * si_sklad_zap) / masa * 100
    si_z_topseed = (topseed_kg * 0.485) / masa * 100
    si_z_kubka = (kubek_kg * 0.7496) / masa * 100
    total_si_inc = si_z_zaprawy + si_z_topseed + si_z_kubka

    st.markdown(f'<div class="result-box"><div style="font-size: 20px;">ILOŚĆ ZAPRAWY (Uzysk {uzysk_custom}%)</div><div class="result-val">{ilosc_zaprawy:.1f} kg</div></div>', unsafe_allow_html=True)
    st.info(f"PRZEWIDYWANY PRZYROST Si: +{total_si_inc:.2f}%")


# ==============================================================================
# ZAKŁADKA 2: KOREKTA SKŁADU CHEMICZNEGO (NOWOŚĆ WG EXCELA)
# ==============================================================================
with tab2:
    st.header("Korekta Składu Chemicznego")
    
    # 1. Globalna masa dla korekty (niezależna od zaprawy)
    st.markdown("### 1. Parametry wsadu")
    masa_korekta = st.number_input("Aktualna masa metalu w piecu/kadzi [Kg]:", value=2300, step=50, key="masa_kor")
    
    # Funkcja licząca dokładny wzór z Excela (z uwzględnieniem rozcieńczenia)
    def oblicz_korkte(masa, obecna, cel, sklad_dodatku):
        if cel == obecna: return 0.0
        if sklad_dodatku == cel: return 0.0 # Zabezpieczenie przed dzieleniem przez 0
        
        # Wzór: Masa * (Cel - Obecna) / (Skład_Dodatku - Cel)
        # Ten wzór uwzględnia, że dodając materiał zwiększamy masę całkowitą
        wynik = masa * (cel - obecna) / (sklad_dodatku - cel)
        return wynik

    st.markdown("---")
    st.markdown("### 2. Wybierz korektę")

    # --- WĘGIEL (C) ---
    with st.expander("⚫ WĘGIEL (C) - Nawęglanie", expanded=False):
        c1, c2, c3 = st.columns(3)
        obecne_c = c1.number_input("Obecny C [%]:", 3.00, 4.50, 3.64, 0.01, format="%.2f")
        cel_c = c2.number_input("Cel C [%]:", 3.00, 4.50, 3.70, 0.01, format="%.2f")
        wsad_c = c3.number_input("C w nawęglaczu [%]:", 50.0, 100.0, 70.0, 1.0) # Wg Excela 70
        
        if cel_c > obecne_c:
            wynik_c = oblicz_korkte(masa_korekta, obecne_c, cel_c, wsad_c)
            st.markdown(f'<div class="result-box">DODAJ NAWĘGLACZA:<br><span class="result-val">{wynik_c:.2f} kg</span></div>', unsafe_allow_html=True)
        elif cel_c < obecne_c:
            st.warning("Cel mniejszy niż obecna wartość! Użyj sekcji 'Zbijanie Węgla' poniżej.")
        else:
            st.success("Skład zgodny.")

    # --- KRZEM (Si) ---
    with st.expander("🪨 KRZEM (Si) - Żelazokrzem", expanded=False):
        s1, s2, s3 = st.columns(3)
        obecne_si = s1.number_input("Obecny Si [%]:", 0.00, 4.00, 1.80, 0.05, format="%.2f")
        cel_si = s2.number_input("Cel Si [%]:", 0.00, 4.00, 2.00, 0.05, format="%.2f")
        wsad_si = s3.number_input("Si w żelazokrzemie [%]:", 40.0, 80.0, 75.0, 1.0) # Wg Excela 75
        
        if cel_si > obecne_si:
            wynik_si = oblicz_korkte(masa_korekta, obecne_si, cel_si, wsad_si)
            st.markdown(f'<div class="result-box">DODAJ FeSi:<br><span class="result-val">{wynik_si:.2f} kg</span></div>', unsafe_allow_html=True)
        else:
            st.info("Obecny Krzem jest wyższy lub równy celowi.")

    # --- INNE STOPY (Cu, Ni, Mo) ---
    with st.expander("🔩 DODATKI STOPOWE (Cu, Ni, Mo)", expanded=False):
        tab_cu, tab_ni, tab_mo = st.tabs(["Miedź (Cu)", "Nikiel (Ni)", "Molibden (Mo)"])
        
        # Miedź
        with tab_cu:
            cu_curr = st.number_input("Obecna Cu [%]:", 0.00, 2.00, 0.06, 0.01)
            cu_dest = st.number_input("Cel Cu [%]:", 0.00, 2.00, 0.72, 0.01)
            cu_cont = st.number_input("Cu w materiale [%]:", 50.0, 100.0, 99.0, 1.0)
            if cu_dest > cu_curr:
                res_cu = oblicz_korkte(masa_korekta, cu_curr, cu_dest, cu_cont)
                st.markdown(f"**Dodaj Miedzi:** {res_cu:.2f} kg")

        # Nikiel
        with tab_ni:
            ni_curr = st.number_input("Obecny Ni [%]:", 0.00, 5.00, 2.13, 0.01)
            ni_dest = st.number_input("Cel Ni [%]:", 0.00, 5.00, 2.40, 0.01)
            ni_cont = st.number_input("Ni w materiale [%]:", 50.0, 100.0, 99.0, 1.0)
            if ni_dest > ni_curr:
                res_ni = oblicz_korkte(masa_korekta, ni_curr, ni_dest, ni_cont)
                st.markdown(f"**Dodaj Niklu:** {res_ni:.2f} kg")

        # Molibden
        with tab_mo:
            mo_curr = st.number_input("Obecny Mo [%]:", 0.00, 5.00, 0.00, 0.01)
            mo_dest = st.number_input("Cel Mo [%]:", 0.00, 5.00, 0.20, 0.01)
            mo_cont = st.number_input("Mo w FeMo [%]:", 40.0, 80.0, 69.0, 1.0) # Wg Excela 69
            if mo_dest > mo_curr:
                res_mo = oblicz_korkte(masa_korekta, mo_curr, mo_dest, mo_cont)
                st.markdown(f"**Dodaj FeMo:** {res_mo:.2f} kg")

    # --- ZBIJANIE WĘGLA (STAL) ---
    with st.expander("📉 ZBIJANIE WĘGLA (Dodatek Stali)", expanded=False):
        st.write("Obliczanie ilości stali potrzebnej do obniżenia węgla.")
        c_zb_curr = st.number_input("Aktualny Węgiel [%]:", 3.0, 4.5, 3.90, 0.01)
        c_zb_dest = st.number_input("Cel Węgiel [%]:", 3.0, 4.5, 3.73, 0.01)
        c_zb_stal = st.number_input("Węgiel w Stali (Złom) [%]:", 0.0, 1.0, 0.10, 0.01)
        
        if c_zb_dest < c_zb_curr:
            # Tutaj wzór też działa, wynik wyjdzie dodatni bo licznik i mianownik będą ujemne
            res_stal = oblicz_korkte(masa_korekta, c_zb_curr, c_zb_dest, c_zb_stal)
            st.markdown(f'<div class="result-box" style="background-color: #dc3545;">DODAJ STALI:<br><span class="result-val">{res_stal:.1f} kg</span></div>', unsafe_allow_html=True)
        else:
            st.info("Aktualny węgiel jest niższy niż cel - trzeba nawęglać (Sekcja 1).")

    st.markdown("---")
    
    # --- MIESZANIE KADZI ---
    with st.expander("🔄 SYMULACJA MIESZANIA (Średnia ważona)", expanded=False):
        st.write("Oblicz wynikowy skład po zmieszaniu dwóch objętości.")
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
