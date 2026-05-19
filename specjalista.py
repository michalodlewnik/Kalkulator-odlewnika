import streamlit as st
import math

# --- 1. KONFIGURACJA STRONY ---
st.set_page_config(
    page_title="Panel Specjalisty",
    page_icon="🔬",
    layout="wide"
)

# --- 2. STYLE CSS ---
st.markdown("""
    <style>
    .block-container { padding-top: 3.5rem !important; padding-bottom: 3rem !important; }
    h1 { color: #00BFFF !important; text-align: center; margin-bottom: 5px !important; font-size: 36px !important; }
    h2 { color: #FFA500 !important; font-size: 24px !important; margin-bottom: 5px !important; }
    
    .custom-header { font-size: 22px !important; font-weight: 600 !important; color: white !important; margin-bottom: 10px !important; padding-top: 10px !important; text-align: center; }
    
    /* Wyniki - Zielone (Zakresy) */
    .result-box { background-color: #28a745; color: white; padding: 15px; border-radius: 10px; text-align: center; margin-top: 10px; margin-bottom: 10px; }
    
    /* Wyniki - Czerwone (Ostrzeżenia) */
    .danger-box { background-color: #dc3545; color: white; padding: 15px; border-radius: 10px; text-align: center; margin-top: 10px; margin-bottom: 10px; }

    /* Wynik CE - Czarny */
    .si-box { background-color: #333333; color: #00ff00; padding: 15px; border-radius: 10px; text-align: center; margin-top: 10px; margin-bottom: 10px; border: 1px solid #444; }
    
    .result-val { font-size: 35px !important; font-weight: 800; display: block; margin-top: 5px;}
    .result-label { font-size: 20px !important; font-weight: 600; text-transform: uppercase; }
    
    .stNumberInput input { height: 50px !important; font-size: 22px !important; color: #1f77b4 !important; }
    /* Suwaki */
    .stSlider [data-baseweb="slider"] { margin-bottom: 10px !important; }
    
    div.stButton > button { background-color: #FFD700 !important; color: black !important; font-size: 20px !important; font-weight: bold !important; border-radius: 12px !important; border: none !important; transition: all 0.1s ease-in-out; }
    div.stButton > button:active { transform: scale(0.95) !important; background-color: #e6c200 !important; }
    
    .stTabs [data-baseweb="tab-list"] { gap: 5px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #333; border-radius: 10px; color: white; padding: 10px; font-size: 18px !important; }
    .stTabs [aria-selected="true"] { background-color: #00BFFF !important; color: black !important; font-weight: bold; }
    hr { margin-top: 5px !important; margin-bottom: 5px !important; border-color: #555; }
    </style>
""", unsafe_allow_html=True)

st.title("🔬 Panel Specjalisty 6.1")

# --- 3. LOGIKA PAMIĘCI ---
if 'topseed_val' not in st.session_state: st.session_state.topseed_val = 8.5
if 'kubek_val' not in st.session_state: st.session_state.kubek_val = 4.0
if 'last_masa' not in st.session_state: st.session_state.last_masa = 1100.0

# --- 4. ZAKŁADKI ---
tab1, tab2, tab3, tab4 = st.tabs(["⚖️ 1. ZAPRAWA", "📊 2. KOREKTA", "🧱 3. ŚCIANKA", "🛢️ 4. NADLEWY"])

# ==============================================================================
# ZAKŁADKA 1: ZAPRAWA
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
    
    st.markdown('<div class="custom-header">Zakładany Uzysk Mg [%]:</div>', unsafe_allow_html=True)
    uzysk_custom = st.slider("", 45, 75, value=60, step=1, label_visibility="collapsed")

    proporcja = masa / 1100
    domyslny_topseed = max(4.0, min(12.0, round((8.8 * proporcja) * 2) / 2))
    domyslny_kubek = max(1.0, min(6.0, round((4.0 * proporcja) * 2) / 2))

    if masa != st.session_state.last_masa:
        st.session_state.topseed_val = domyslny_topseed
        st.session_state.kubek_val = domyslny_kubek
        st.session_state.last_masa = masa

    mg_sklad = zaprawy_db[wybrana]["Mg"]
    si_sklad_zap = zaprawy_db[wybrana]["Si"]
    komponent_mg = (target_mg + 0.76 * (siarka - 0.01) + 0.007)
    ilosc_zaprawy = (masa * (komponent_mg / (mg_sklad * uzysk_custom)) * (temp / 1450)) * 100

    st.markdown("---")
    st.markdown('<div class="custom-header">Materiały pomocnicze:</div>', unsafe_allow_html=True)
    
    topseed_kg = st.slider("Topseed [Kg]:", 4.0, 12.0, value=st.session_state.topseed_val, step=0.5)
    st.session_state.topseed_val = topseed_kg
    
    kubek_kg = st.slider("Modyfikacja do kubka [Kg]:", 1.0, 6.0, value=st.session_state.kubek_val, step=0.5)
    st.session_state.kubek_val = kubek_kg

    if st.button("🔄 RESETUJ SUGEROWANE", use_container_width=True):
        st.session_state.topseed_val = domyslny_topseed
        st.session_state.kubek_val = domyslny_kubek
        st.rerun()

    si_z_zaprawy = (ilosc_zaprawy * si_sklad_zap) / masa * 100
    si_z_topseed = (topseed_kg * 0.485) / masa * 100
    si_z_kubka = (kubek_kg * 0.7496) / masa * 100
    total_si_inc = si_z_zaprawy + si_z_topseed + si_z_kubka

    st.markdown(f"""
        <div class="result-box">
            <div class="result-label">ILOŚĆ ZAPRAWY (Uzysk {uzysk_custom}%)</div>
            <div class="result-val">{ilosc_zaprawy:.1f} kg</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="si-box">
            <div class="result-label">PRZEWIDYWANY PRZYROST Si</div>
            <div class="result-val">+{total_si_inc:.2f}%</div>
        </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# ZAKŁADKA 2: KOREKTA
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
            st.markdown(f'<div class="result-box"><span class="result-label">DODAJ NAWĘGLACZA:</span><br><span class="result-val">{wynik_c:.2f} kg</span></div>', unsafe_allow_html=True)
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
            st.markdown(f'<div class="result-box"><span class="result-label">DODAJ FeSi:</span><br><span class="result-val">{wynik_si:.2f} kg</span></div>', unsafe_allow_html=True)
        else:
            st.info("Skład OK.")

    with st.expander("🟠 MIEDŹ (Cu)", expanded=False):
        col1, col2, col3 = st.columns(3)
        cu_curr = col1.number_input("Obecna Cu [%]:", 0.00, 2.00, 0.06, 0.01)
        cu_dest = col2.number_input("Cel Cu [%]:", 0.00, 2.00, 0.72, 0.01)
        cu_cont = col3.number_input("Cu w dodatku [%]:", 0.0, 100.0, 99.0, 1.0)
        
        if cu_dest > cu_curr:
            res_cu = oblicz_korkte(masa_korekta, cu_curr, cu_dest, cu_cont)
            st.markdown(f'<div class="result-box"><span class="result-label">DODAJ MIEDZI:</span><br><span class="result-val">{res_cu:.2f} kg</span></div>', unsafe_allow_html=True)
        else:
            st.success("Skład OK.")

    with st.expander("⚪ NIKIEL (Ni)", expanded=False):
        col1, col2, col3 = st.columns(3)
        ni_curr = col1.number_input("Obecny Ni [%]:", 0.00, 5.00, 2.13, 0.01)
        ni_dest = col2.number_input("Cel Ni [%]:", 0.00, 5.00, 2.40, 0.01)
        ni_cont = col3.number_input("Ni w dodatku [%]:", 0.0, 100.0, 99.0, 1.0)
        
        if ni_dest > ni_curr:
            res_ni = oblicz_korkte(masa_korekta, ni_curr, ni_dest, ni_cont)
            st.markdown(f'<div class="result-box"><span class="result-label">DODAJ NIKLU:</span><br><span class="result-val">{res_ni:.2f} kg</span></div>', unsafe_allow_html=True)
        else:
            st.success("Skład OK.")

    with st.expander("🟣 MOLIBDEN (Mo)", expanded=False):
        col1, col2, col3 = st.columns(3)
        mo_curr = col1.number_input("Obecny Mo [%]:", 0.00, 5.00, 0.00, 0.01)
        mo_dest = col2.number_input("Cel Mo [%]:", 0.00, 5.00, 0.20, 0.01)
        mo_cont = col3.number_input("Mo w dodatku [%]:", 0.0, 100.0, 69.0, 1.0)
        
        if mo_dest > mo_curr:
            res_mo = oblicz_korkte(masa_korekta, mo_curr, mo_dest, mo_cont)
            st.markdown(f'<div class="result-box"><span class="result-label">DODAJ FeMo:</span><br><span class="result-val">{res_mo:.2f} kg</span></div>', unsafe_allow_html=True)
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
            st.markdown(f'<div class="result-box" style="background-color: #dc3545;"><span class="result-label">DODAJ STALI:</span><br><span class="result-val">{res_stal:.1f} kg</span></div>', unsafe_allow_html=True)
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


# ==============================================================================
# ZAKŁADKA 3: ŚCIANKA (OKNO TECHNOLOGICZNE - SUWAK SI)
# ==============================================================================
with tab3:
    st.markdown("### Dobór parametrów do ścianki")
    st.info("Algorytm z wygładzoną krzywą spadku CE (brak skoków logicznych).")

    st.markdown('<div class="custom-header">1. Grubość ścianki odlewu [mm]:</div>', unsafe_allow_html=True)
    grubosc = st.slider("", 5, 80, 20, step=1, label_visibility="collapsed", key="slider_grubosc")

    # BAZA DANYCH CE (WYGŁADZONA)
    tabela_ce = [
        (0,  7,   4.75),
        (8,  12,  4.60),
        (13, 17,  4.50),
        (18, 22,  4.40),
        (23, 27,  4.35),
        (28, 32,  4.30),
        (33, 37,  4.25),
        (38, 42,  4.20),
        (43, 47,  4.16),
        (48, 52,  4.12),
        (53, 57,  4.08),
        (58, 62,  4.04),
        (63, 67,  4.01),
        (68, 72,  3.98),
        (73, 77,  3.95),
        (78, 80,  3.93) 
    ]

    target_ce = 0
    for min_g, max_g, ce in tabela_ce:
        if min_g <= grubosc <= max_g:
            target_ce = ce
            break

    # SUWAK ZAKRESU SI
    st.markdown("---")
    st.markdown('<div class="custom-header">2. Planowany zakres Krzemu (Si) [%]:</div>', unsafe_allow_html=True)
    
    si_range = st.slider("", 2.00, 2.90, (2.00, 2.90), step=0.01, label_visibility="collapsed", key="slider_si_range")
    
    si_min_user = si_range[0]
    si_max_user = si_range[1]

    # OBLICZANIE WĘGLA
    c_lower_bound = target_ce - (si_max_user / 3.0) 
    c_upper_bound = target_ce - (si_min_user / 3.0) 

    ce_min = target_ce * 0.99
    ce_max = target_ce * 1.01

    st.markdown("---")
    
    # WYNIKI
    col_w1, col_w2 = st.columns(2)
    
    with col_w1:
        st.markdown(f"""
            <div class="result-box" style="background-color: #333; border: 1px solid white;">
                <div class="result-label">WYMAGANY WĘGIEL (C)</div>
                <div class="result-val" style="color: orange; font-size: 30px !important;">{c_lower_bound:.2f} - {c_upper_bound:.2f}</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col_w2:
        st.markdown(f"""
            <div class="result-box" style="background-color: #333; border: 1px solid white;">
                <div class="result-label">WYBRANY KRZEM (Si)</div>
                <div class="result-val" style="color: #00BFFF; font-size: 30px !important;">{si_min_user:.2f} - {si_max_user:.2f}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="si-box">
            <div class="result-label">DOCELOWY RÓWNOWAŻNIK (CE)</div>
            <div class="result-val">{target_ce:.2f}</div>
            <div style="font-size: 16px; color: #888; margin-top: 5px;">(Tolerancja +/- 1%: {ce_min:.2f} - {ce_max:.2f})</div>
        </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# ZAKŁADKA 4: NADLEWY BOCZNE (Kalkulacja ciągła)
# ==============================================================================
with tab4:
    st.markdown("### Dobór Nadlewów Bocznych")
    st.info("Kalkulator wylicza optymalne wymiary nadlewu (zawsze przyjmując proporcję H = 1.5 D), weryfikując je przez pryzmat Warunku Modułu (czas krzepnięcia) oraz Bilansu Masy (zdolność pokrycia skurczu).")

    col_n1, col_n2 = st.columns(2)
    
    with col_n1:
        st.markdown("**Geometria Odlewu**")
        waga_odl = st.number_input("Waga odlewu [kg]:", value=50.0, step=1.0)
        v_odl = st.number_input("Objętość odlewu [cm3]:", value=7000.0, step=100.0)
        s_odl = st.number_input("Powierzchnia odlewu [cm2]:", value=2000.0, step=100.0)
        
        st.markdown("**Geometria Węzła Cieplnego**")
        v_wezla = st.number_input("Objętość węzła [cm3]:", value=500.0, step=10.0)
        s_wezla = st.number_input("Powierzchnia węzła [cm2]:", value=250.0, step=10.0)
        p_przekroju = st.number_input("Pole przekroju węzła [cm2]:", value=50.0, step=1.0)
        obwod_wezla = st.number_input("Obwód węzła [cm]:", value=30.0, step=1.0)

    with col_n2:
        st.markdown("**Parametry Zasilania**")
        wsp_bezp = st.selectbox("Współczynnik bezpieczeństwa:", [1.2, 1.25, 1.3], index=0)
        liczba_nadlewow = st.number_input("Ile nadlewów przewidujesz?:", value=2, min_value=1, step=1)
        
        skurcz_obj = st.slider("Skurcz objętościowy (S_obj) [%]:", 1.0, 4.0, 2.0, 0.5)
        wsp_wyssania = st.number_input("Współczynnik wyssania nadlewu (W) [%]:", value=15.0, min_value=1.0, max_value=60.0, step=1.0, help="Dla nadlewu naturalnego w piasku zazwyczaj 14-16%.")
        gestosc_metalu = 7.2  # Gęstość żeliwa kg/dm3
    
    st.markdown("---")
    
    if st.button("🚀 OBLICZ I DOBIERZ NADLEW", use_container_width=True):
        # 1. OBLICZANIE MODUŁÓW
        modul_odl_vs = (v_odl / s_odl) if s_odl > 0 else 0
        modul_wezla_vs = (v_wezla / s_wezla) if s_wezla > 0 else 0
        modul_wezla_po = (p_przekroju / obwod_wezla) if obwod_wezla > 0 else 0
        
        # System wybiera bezpieczniejszy (większy) moduł węzła
        modul_wezla_ostateczny = max(modul_wezla_vs, modul_wezla_po)
        
        # Wymagany moduł nadlewu
        modul_nadlewu_wymagany = modul_wezla_ostateczny * wsp_bezp
        
        # Matematyka walca (H = 1.5 * D)
        # Moduł V/S dla walca = (pi*D^2/4 * 1.5*D) / (pi*D*1.5*D + 2*pi*D^2/4) = 0.1875 * D
        # Zatem wymagane D [cm] z warunku modułu:
        D_cm_mod = modul_nadlewu_wymagany / 0.1875
        D_mm_mod = D_cm_mod * 10.0
        
        # 2. OBLICZENIA MASOWE
        zapotrzebowanie_calkowite_kg = waga_odl * (skurcz_obj / 100.0)
        zapotrzebowanie_na_1_nadlew = zapotrzebowanie_calkowite_kg / liczba_nadlewow
        
        # Minimalna masa nadlewu wynikająca z fizyki wyssania
        wymagana_masa_nadlewu_kg = zapotrzebowanie_na_1_nadlew / (wsp_wyssania / 100.0)

        # Wymagana objętość 1 nadlewu
        V_wymagane_dm3 = wymagana_masa_nadlewu_kg / gestosc_metalu
        V_wymagane_cm3 = V_wymagane_dm3 * 1000.0
        
        # Objętość V = (1.5 * pi * D^3) / 4. Z tego wyznaczamy D [cm] dla masy:
        D_cm_mas = (4.0 * V_wymagane_cm3 / (1.5 * math.pi)) ** (1.0 / 3.0)
        D_mm_mas = D_cm_mas * 10.0
        
        # 3. DOBÓR FINALNYCH WYMIARÓW
        D_kalkulowane = max(D_mm_mod, D_mm_mas)
        
        # Zaokrąglenie średnicy w górę do pełnych 5 mm (standard rynkowy)
        D_final = int(math.ceil(D_kalkulowane / 5.0) * 5)
        
        # Sztywna reguła H = 1.5 * D
        H_final = int(1.5 * D_final)
        
        # 4. PRZELICZENIE FINALNYCH PARAMETRÓW PO ZAOKRĄGLENIU
        D_final_cm = D_final / 10.0
        H_final_cm = H_final / 10.0
        
        V_final_cm3 = (math.pi * (D_final_cm ** 2) / 4.0) * H_final_cm
        M_final_cm = 0.1875 * D_final_cm
        Waga_final_kg = (V_final_cm3 / 1000.0) * gestosc_metalu
        
        # Sprawdzenie, co windowało gabaryt
        if D_mm_mod >= D_mm_mas:
            powod_doboru = "O doborze zadecydował WARUNEK MODUŁU (czas krzepnięcia)."
        else:
            powod_doboru = "O doborze zadecydował WARUNEK MASY (brakowało metalu na skurcz)."
        
        # WYPISANIE WYNIKÓW
        c_res1, c_res2, c_res3 = st.columns(3)
        with c_res1:
            st.metric("Moduł Węzła (Mw)", f"{modul_wezla_ostateczny:.2f} cm")
        with c_res2:
            st.metric(f"Wymagany Moduł Nadlewu (x{wsp_bezp})", f"{modul_nadlewu_wymagany:.2f} cm")
        with c_res3:
            st.metric("Wymagana masa (1 szt.)", f"{wymagana_masa_nadlewu_kg:.2f} kg")
            
        st.markdown(f"""
            <div class="result-box" style="background-color: #007bff; border: 2px solid white;">
                <div class="result-label">ZALECANY NADLEW</div>
                <div style="font-size: 24px; font-weight: bold;">
                    ⌀ {D_final} mm | Wys: {H_final} mm
                </div>
                <div style="font-size: 18px; margin-top: 10px;">
                    Moduł: {M_final_cm:.2f} cm | Waga: ~{Waga_final_kg:.2f} kg
                </div>
            </div>
            <div style="text-align: center; color: #aaa;">{powod_doboru}</div>
        """, unsafe_allow_html=True)
