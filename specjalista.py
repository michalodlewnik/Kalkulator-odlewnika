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

st.title("🔬 Panel Specjalisty 6.6")

# --- 3. LOGIKA PAMIĘCI ---
if 'topseed_val' not in st.session_state: st.session_state.topseed_val = 8.5
if 'kubek_val' not in st.session_state: st.session_state.kubek_val = 4.0
if 'last_masa' not in st.session_state: st.session_state.last_masa = 1100.0

# --- 4. ZAKŁADKI ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(["⚖️ 1. ZAPRAWA", "📊 2. KOREKTA", "🧱 3. ŚCIANKA", "🛢️ 4. NADLEWY", "⚙️ 5. FILTRY"])

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

    # OBLICZANIE KRZEMU
    si_z_zaprawy = (ilosc_zaprawy * si_sklad_zap) / masa * 100
    si_z_kubka = (kubek_kg * 0.7496) / masa * 100
    
    # Wykluczenie Topseedu dla zaprawy NiMg16
    if wybrana == "Zap. NiMg16":
        si_z_topseed = 0.0
        st.info("💡 Przy zaprawie NiMg16 system automatycznie pomija dodatek Topseed w kalkulacji całkowitego krzemu (Si).")
    else:
        si_z_topseed = (topseed_kg * 0.485) / masa * 100
        
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
# ZAKŁADKA 3: ŚCIANKA (OKNO TECHNOLOGICZNE - SUWAK SI) - ZINTEGROWANA (GJS/GJL)
# ==============================================================================
with tab3:
    rodzaj_zeliwa_scianka = st.radio(
        "Wybierz rodzaj żeliwa do analizy ścianki:", 
        ["🟢 Żeliwo Sferoidalne (GJS)", "⚪ Żeliwo Szare (GJL)"], 
        horizontal=True
    )
    st.markdown("---")

    if rodzaj_zeliwa_scianka == "🟢 Żeliwo Sferoidalne (GJS)":
        st.markdown("### Dobór parametrów do ścianki (SFERO)")
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
        
        # WYNIKI GJS
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

    else:
        # ---------------- LOGIKA GJL (SZARE) ----------------
        st.markdown("### Kalkulator Technologiczny GJL + Perlit")
        
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            dict_gjl = {
                "EN-GJL-150": 4.450,
                "EN-GJL-200": 4.250,
                "EN-GJL-250": 4.100,
                "EN-GJL-300": 3.900
            }
            wybrany_gjl = st.selectbox("Gatunek:", list(dict_gjl.keys()), index=2)
            
        with col_g2:
            grubosc_gjl = st.slider("Ścianka [mm]:", 5, 80, 20, step=1)
            
        st.markdown("#### Skład bazowy (Si)")
        si_range_gjl = st.slider("Zakres Krzemu (Si) [%]:", 1.00, 3.00, (1.80, 2.10), step=0.01)
        si_min_gjl, si_max_gjl = si_range_gjl[0], si_range_gjl[1]
        
        st.markdown("#### Stabilizatory Perlitu i Balans Mn/S")
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            s_val = st.number_input("Siarka (S) [%]:", value=0.050, step=0.005, min_value=0.010, format="%.3f")
        with col_m2:
            mn_val = st.number_input("Mangan (Mn) [%]:", value=0.50, step=0.01)
        with col_m3:
            cu_val = st.slider("Miedź (Cu) [%]:", 0.00, 1.00, 0.00, step=0.05)
            
        # OBLICZENIA GJL
        base_ce = dict_gjl[wybrany_gjl]
        multiplier = math.floor((grubosc_gjl - 5) / 5)
        target_ce_gjl = base_ce - (multiplier * 0.025)
        
        c_low_gjl = target_ce_gjl - (si_max_gjl / 3.0)
        c_up_gjl = target_ce_gjl - (si_min_gjl / 3.0)
        
        ratio_mn_s = mn_val / s_val
        min_mn_required = (1.7 * s_val) + 0.3
        
        # Generowanie Porady
        num_class = int(wybrany_gjl.split('-')[-1])
        advice_text = f"Dla grubości {grubosc_gjl} mm i klasy {num_class}:<br>"
        
        if mn_val < min_mn_required:
            advice_text += f"<span style='color: #ff4b4b; font-weight:bold;'>PODNIEŚ MANGAN!</span> Min. sugerowany dla S={s_val:.3f}% to <b>{min_mn_required:.2f}%</b>.<br>"
        else:
            advice_text += "<span style='color: #00ffaa;'>Balans Mn/S poprawny.</span><br>"
            
        if num_class >= 250 and cu_val < 0.2:
            advice_text += "Dla tej klasy zalecany dodatek Cu (0.2 - 0.5%) dla stabilizacji perlitu."

        # Kolory wskaźników
        mn_color = "#00ffaa" if ratio_mn_s >= 1.7 else "#ff4b4b"
        
        st.markdown("---")
        
        # WYNIKI GJL
        col_out1, col_out2, col_out3 = st.columns(3)
        with col_out1:
            st.markdown(f"""
                <div class="result-box" style="background-color: #1e2128; border-top: 3px solid #ffaa00; border-radius: 8px;">
                    <div style="font-size: 0.75em; color: #aaa; text-transform: uppercase;">Wymagany Węgiel (C)</div>
                    <div style="font-size: 1.8em; font-weight: bold; color: #ffaa00;">{c_low_gjl:.3f} - {c_up_gjl:.3f}</div>
                </div>
            """, unsafe_allow_html=True)
        with col_out2:
            st.markdown(f"""
                <div class="result-box" style="background-color: #1e2128; border-top: 3px solid #00bfff; border-radius: 8px;">
                    <div style="font-size: 0.75em; color: #aaa; text-transform: uppercase;">Docelowy CE</div>
                    <div style="font-size: 1.8em; font-weight: bold; color: white;">{target_ce_gjl:.3f}</div>
                </div>
            """, unsafe_allow_html=True)
        with col_out3:
            st.markdown(f"""
                <div class="result-box" style="background-color: #1e2128; border-top: 3px solid {mn_color}; border-radius: 8px;">
                    <div style="font-size: 0.75em; color: #aaa; text-transform: uppercase;">Stosunek Mn / S</div>
                    <div style="font-size: 1.8em; font-weight: bold; color: {mn_color};">{ratio_mn_s:.2f}</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
            <div class="result-box" style="background: rgba(0, 255, 170, 0.05); border: 1px solid #444; border-radius: 8px; text-align: left; padding: 15px;">
                <div style="font-size: 0.9em; color: #ccc;">{advice_text}</div>
            </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# ZAKŁADKA 4: NADLEWY BOCZNE (Kalkulacja ciągła + Jednostki mm + Szyjka)
# ==============================================================================
with tab4:
    st.markdown("### Dobór Nadlewów Bocznych")
    st.info("Kalkulator sprawdza 3 moduły (odlewu, węzła obj/pow, węzła przekrój/obwód), wybiera największy i wylicza optymal nadlew (H = 1.5 D).")

    col_n1, col_n2, col_n3 = st.columns(3)
    
    with col_n1:
        st.markdown("**Geometria Odlewu**")
        waga_odl = st.number_input("Waga odlewu [kg]:", value=100.0, step=1.0)
        v_odl = st.number_input("Objętość odlewu [mm³]:", value=0.0, step=10000.0)
        s_odl = st.number_input("Powierzchnia odlewu [mm²]:", value=0.0, step=1000.0)
        
        st.markdown("**Geometria Węzła Cieplnego**")
        v_wezla = st.number_input("Objętość węzła [mm³]:", value=0.0, step=1000.0)
        s_wezla = st.number_input("Powierzchnia węzła [mm²]:", value=0.0, step=100.0)
        p_przekroju = st.number_input("Pole przekroju węzła [mm²]:", value=0.0, step=100.0)
        obwod_wezla = st.number_input("Obwód węzła [mm]:", value=0.0, step=10.0)

    with col_n2:
        st.markdown("**Parametry Zasilania**")
        wsp_bezp = st.selectbox("Współczynnik bezpieczeństwa:", [1.2, 1.25, 1.3], index=0)
        liczba_nadlewow = st.number_input("Ile nadlewów przewidujesz?:", value=2, min_value=1, step=1)
        
        skurcz_obj = st.slider("Skurcz objętościowy (S_obj) [%]:", 1.0, 4.0, 2.0, 0.5)
        wsp_wyssania = st.number_input("Współczynnik wyssania nadlewu (W) [%]:", value=15.0, min_value=1.0, max_value=60.0, step=1.0, help="Dla nadlewu naturalnego w piasku zazwyczaj 14-16%.")
        gestosc_metalu = 7.2  # Gęstość żeliwa kg/dm3
        
    with col_n3:
        st.markdown("**Parametry Szyjki (Wlewu)**")
        dict_szyjek = {
            "Gorący (0.55 * Mw)": 0.55,
            "Standardowy (0.65 * Mw)": 0.65,
            "Bezpieczny (0.80 * Mw)": 0.80
        }
        wybor_typu_szyjki = st.selectbox("Wybierz współczynnik szyjki:", list(dict_szyjek.keys()), index=1)
        wsp_szyjki_val = dict_szyjek[wybor_typu_szyjki]
        wysokosc_szyjki = st.number_input("Wysokość szyjki (h) [mm]:", value=30.0, step=1.0)
    
    st.markdown("---")
    
    if st.button("🚀 OBLICZ I DOBIERZ NADLEW", use_container_width=True):
        # 1. OBLICZANIE WSZYSTKICH 3 MODUŁÓW (wyniki w mm)
        modul_odl_vs = (v_odl / s_odl) if s_odl > 0 else 0
        modul_wezla_vs = (v_wezla / s_wezla) if s_wezla > 0 else 0
        modul_wezla_po = (p_przekroju / obwod_wezla) if obwod_wezla > 0 else 0
        
        # Słownik do zidentyfikowania, co wygrało
        moduly_dict = {
            "Odlewu (V/S)": modul_odl_vs,
            "Węzła (V/S)": modul_wezla_vs,
            "Węzła (Przekrój/Obwód)": modul_wezla_po
        }
        
        # System wybiera bezpieczniejszy (największy) moduł
        zwyciezki_typ_modulu = max(moduly_dict, key=moduly_dict.get)
        modul_ostateczny_mm = moduly_dict[zwyciezki_typ_modulu]
        
        if modul_ostateczny_mm == 0:
            st.error("Wprowadź poprawne wymiary węzła lub odlewu! Moduł węzła nie może wynosić 0.")
        else:
            # Wymagany moduł nadlewu w mm
            modul_nadlewu_wymagany_mm = modul_ostateczny_mm * wsp_bezp
            
            # Matematyka walca (H = 1.5 * D) dla warunku Modułu
            D_mm_mod = modul_nadlewu_wymagany_mm / 0.1875
            
            # 2. OBLICZENIA MASOWE
            zapotrzebowanie_calkowite_kg = waga_odl * (skurcz_obj / 100.0)
            zapotrzebowanie_na_1_nadlew = zapotrzebowanie_calkowite_kg / liczba_nadlewow
            
            # Minimalna masa nadlewu wynikająca z fizyki wyssania
            wymagana_masa_nadlewu_kg = zapotrzebowanie_na_1_nadlew / (wsp_wyssania / 100.0)

            # Wymagana objętość 1 nadlewu w mm³
            V_wymagane_dm3 = wymagana_masa_nadlewu_kg / gestosc_metalu
            V_wymagane_mm3 = V_wymagane_dm3 * 1000000.0
            
            # Objętość V = (1.5 * pi * D^3) / 4. Z tego wyznaczamy D [mm] dla warunku Masy:
            D_mm_mas = (4.0 * V_wymagane_mm3 / (1.5 * math.pi)) ** (1.0 / 3.0)
            
            # 3. DOBÓR FINALNYCH WYMIARÓW
            D_kalkulowane = max(D_mm_mod, D_mm_mas)
            
            # Zaokrąglenie średnicy w górę do pełnych 5 mm
            D_final = int(math.ceil(D_kalkulowane / 5.0) * 5)
            H_final = int(1.5 * D_final)
            
            # 4. PRZELICZENIE FINALNYCH PARAMETRÓW PO ZAOKRĄGLENIU
            V_final_mm3 = (math.pi * (D_final ** 2) / 4.0) * H_final
            M_final_mm = 0.1875 * D_final
            Waga_final_kg = (V_final_mm3 / 1000000.0) * gestosc_metalu
            
            # Sprawdzenie, co windowało gabaryt
            if D_mm_mod >= D_mm_mas:
                powod_doboru = "O doborze zadecydował WARUNEK MODUŁU (czas krzepnięcia)."
            else:
                powod_doboru = "O doborze zadecydował WARUNEK MASY (brakowało metalu na skurcz)."

            # 5. OBLICZENIA SZYJKI
            modul_szyjki_wymagany_mm = modul_ostateczny_mm * wsp_szyjki_val
            limit_wysokosci = 2 * modul_szyjki_wymagany_mm
            
            szyjka_blad = False
            szerokosc_szyjki_final = 0
            
            if wysokosc_szyjki <= limit_wysokosci:
                szyjka_blad = True
            else:
                szerokosc_szyjki = (2 * modul_szyjki_wymagany_mm * wysokosc_szyjki) / (wysokosc_szyjki - 2 * modul_szyjki_wymagany_mm)
                szerokosc_szyjki_final = int(math.ceil(szerokosc_szyjki))
                
            # Wyliczenie odległości (L) oraz odległości od osi
            L_min = int(math.ceil(2 * modul_ostateczny_mm))
            L_max = int(math.ceil(3 * modul_ostateczny_mm))
            promien_nadlewu = D_final / 2.0
            os_min = int(math.ceil(L_min + promien_nadlewu))
            os_max = int(math.ceil(L_max + promien_nadlewu))
            
            # WYPISANIE WYNIKÓW
            st.markdown(f"<div style='text-align: center; color: #aaa; margin-bottom: 10px;'>Bazowy moduł wyliczono z: <b>{zwyciezki_typ_modulu}</b></div>", unsafe_allow_html=True)

            c_res1, c_res2, c_res3 = st.columns(3)
            with c_res1:
                st.metric("Największy Moduł (Mw)", f"{modul_ostateczny_mm:.1f} mm")
            with c_res2:
                st.metric(f"Moduł Nadlewu (x{wsp_bezp})", f"{modul_nadlewu_wymagany_mm:.1f} mm")
            with c_res3:
                # Rozbudowany i sformatowany tekst pod wymaganą masą
                st.markdown(f"""
                    <div style="padding-top: 5px;">
                        <span style="font-size: 14px; font-weight: 600; color: #aaa; text-transform: uppercase;">Wymagana masa (1 szt.)</span><br>
                        <span style="font-size: 28px; font-weight: bold; color: white;">{wymagana_masa_nadlewu_kg:.2f} kg</span><br>
                        <span style="font-size: 13px; color: #00BFFF; line-height: 1.3; display: block; margin-top: 5px;">
                            <b>Waga odlewu:</b> {waga_odl} kg x {skurcz_obj}% = {zapotrzebowanie_calkowite_kg:.2f} kg skurczu.<br>
                            Wyssanie ({wsp_wyssania}%) nadlewu musi ten skurcz wypełnić.
                        </span>
                    </div>
                """, unsafe_allow_html=True)
                
            st.markdown("<br>", unsafe_allow_html=True)
            col_out1, col_out2, col_out3 = st.columns(3)
            
            with col_out1:
                st.markdown(f"""
                    <div class="result-box" style="background-color: #007bff; border: 2px solid white; height: 190px; display: flex; flex-direction: column; justify-content: center;">
                        <div class="result-label">ZALECANY NADLEW</div>
                        <div style="font-size: 26px; font-weight: bold;">
                            ⌀ {D_final} mm | Wys: {H_final} mm
                        </div>
                        <div style="font-size: 16px; margin-top: 10px;">
                            Moduł: {M_final_mm:.1f} mm | Waga: ~{Waga_final_kg:.2f} kg
                        </div>
                    </div>
                    <div style="text-align: center; color: #aaa; font-size: 14px;">{powod_doboru}</div>
                """, unsafe_allow_html=True)

            with col_out2:
                if szyjka_blad:
                    st.markdown(f"""
                        <div class="danger-box" style="height: 190px; display: flex; flex-direction: column; justify-content: center;">
                            <div class="result-label" style="font-size: 16px;">BŁĄD SZYJKI! ZA NISKA (h={wysokosc_szyjki} mm)</div>
                            <div style="font-size: 14px; margin-top: 5px;">
                                Limit dla wyliczonego modułu ({modul_szyjki_wymagany_mm:.1f} mm) to minimum {limit_wysokosci:.1f} mm. 
                                Zwiększ założoną wysokość szyjki.
                            </div>
                        </div>
                        <div style="text-align: center; color: #aaa; font-size: 14px; visibility: hidden;">placeholder</div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div class="result-box" style="background-color: #fd7e14; border: 2px solid white; height: 190px; display: flex; flex-direction: column; justify-content: center;">
                            <div class="result-label">ZALECANA SZYJKA</div>
                            <div style="font-size: 26px; font-weight: bold;">
                                Wys: {wysokosc_szyjki} mm | Szer: {szerokosc_szyjki_final} mm
                            </div>
                            <div style="font-size: 16px; margin-top: 10px;">
                                Wymagany Moduł: {modul_szyjki_wymagany_mm:.1f} mm
                            </div>
                        </div>
                        <div style="text-align: center; color: #aaa; font-size: 14px; visibility: hidden;">placeholder</div>
                    """, unsafe_allow_html=True)
                    
            with col_out3:
                st.markdown(f"""
                    <div class="result-box" style="background-color: #6f42c1; border: 2px solid white; height: 190px; display: flex; flex-direction: column; justify-content: center;">
                        <div class="result-label" style="font-size: 16px;">ODLEGŁOŚĆ ODLEWU</div>
                        <div style="font-size: 18px; font-weight: bold; margin-top: 5px;">
                            Długość Szyjki (L):<br> {L_min} - {L_max} mm
                        </div>
                        <hr style="border-top: 1px dashed white; margin: 8px 0;">
                        <div style="font-size: 16px; font-weight: bold;">
                            Od osi nadlewu:<br> {os_min} - {os_max} mm
                        </div>
                    </div>
                """, unsafe_allow_html=True)

# ==============================================================================
# ZAKŁADKA 5: FILTRY (Zintegrowany System OPSA + Modyfikacja na strugę)
# ==============================================================================
with tab5:
    st.markdown("### Zintegrowany System Obliczeniowy (OPSA)")
    
    col_f1, col_f2 = st.columns(2)
    
    with col_f1:
        st.markdown("#### 1. Parametry Formy (Wymagania)")
        iron_type = st.selectbox("Rodzaj żeliwa:", ["Sferoidalne (GJS)", "Szare (GJL)"])
        mass_f = st.slider("Masa brutto (detal + układ) [kg]:", 5.0, 400.0, 100.0, 1.0)
        
        thick_opts = ["Cienkie (< 8 mm)", "Średnie (8 - 15 mm)", "Pogrubione (15 - 30 mm)", "Masywne (> 30 mm)"]
        thick_idx = thick_opts.index(st.selectbox("Przeważająca grubość ścianki:", thick_opts, index=1))
        
        # Wstępne wyliczenie czasu zalewania, aby użytkownik mógł go nadpisać
        is_sfero = (iron_type == "Sferoidalne (GJS)")
        k_arr = [1.1, 1.3, 1.5, 1.8] if is_sfero else [1.3, 1.5, 1.8, 2.2]
        calc_time = k_arr[thick_idx] * math.sqrt(mass_f)
        
        st.markdown("---")
        st.markdown("#### 2. Ustawienia zalewania")
        req_time_user = st.number_input("Czas zalewania [s] (Możesz nadpisać wyliczony ze wzoru):", value=float(f"{calc_time:.1f}"), step=0.5)

    with col_f2:
        st.markdown("#### 3. Układ Filtrujący (Możliwości)")
        filter_opts = ["50x50", "50x75", "60x60", "75x75", "100x100", "150x150"]
        filter_size = st.selectbox("Wymiar filtra [mm]:", filter_opts, index=4)
        count = st.slider("Liczba filtrów [szt.]:", 1, 6, 1, 1)
        
        ppi_opts = [10, 20, 30]
        ppi = st.select_slider("Gęstość (PPI):", options=ppi_opts, value=10)
        
        st.markdown("---")
        st.markdown("#### 4. Modyfikacja na strugę (GJS)")
        mod_range = st.slider("Zakres modyfikacji na strugę [%]:", 0.05, 0.30, (0.10, 0.20), step=0.01)

    if st.button("🚀 OBLICZ FILTRY I MODYFIKACJĘ", use_container_width=True):
        
        # --- OBLICZENIA POPYTU (FORMA) na podstawie ostatecznego czasu z Inputa ---
        req_time = req_time_user
        req_flow = mass_f / req_time if req_time > 0 else 0
        
        # --- OBLICZENIA PODAŻY (FILTR) ---
        dims = filter_size.split('x')
        area_cm2 = (int(dims[0]) * int(dims[1])) / 100.0
        total_area = area_cm2 * count
        
        if is_sfero:
            cap_factor = 1.15 if ppi == 10 else (0.8 if ppi == 20 else 0.5)
        else:
            cap_factor = 2.5 if ppi == 10 else (1.5 if ppi == 20 else 1.0)
            
        flow_factor = 0.12 if ppi == 10 else (0.08 if ppi == 20 else 0.04)
        
        filter_cap = total_area * cap_factor
        filter_flow = total_area * flow_factor
        
        # --- OBLICZENIA MODYFIKACJI NA STRUGĘ ---
        # Wynik podajemy w gramach na sekundę (g/s).
        # Wzór: (Masa [kg] * (Procent / 100)) / Czas [s] = Wynik [kg/s] * 1000 = [g/s]
        mod_min_gs = ((mass_f * (mod_range[0] / 100.0)) / req_time) * 1000.0 if req_time > 0 else 0
        mod_max_gs = ((mass_f * (mod_range[1] / 100.0)) / req_time) * 1000.0 if req_time > 0 else 0

        # --- ZDERZENIE LOGIKI I WERDYKT ---
        flow_ok = filter_flow >= req_flow
        mass_ok = filter_cap >= mass_f
        
        if not flow_ok and not mass_ok:
            v_class = "danger-box"
            v_text = "KATASTROFA: DŁAWIENIE STRUGI + ZATKANIE FILTRA"
        elif not flow_ok:
            v_class = "danger-box"
            v_text = "BŁĄD: FILTR DŁAWI STRUGĘ (RYZYKO NIEDOLAŃ)"
        elif not mass_ok:
            v_class = "danger-box"
            v_text = "BŁĄD: PRZEKROCZONA POJEMNOŚĆ (RYZYKO ZATKANIA)"
        else:
            v_class = "result-box"
            v_text = "UKŁAD BEZPIECZNY - MOŻNA ZALEWAĆ"
            
        # WYŚWIETLENIE WERDYKTU
        st.markdown(f'<div class="{v_class}" style="font-size:22px; font-weight:bold;">{v_text}</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # KARTY METRYK (w tym modyfikacja)
        col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
        
        with col_m1:
            st.markdown(f"""
                <div style="background: #252525; padding: 15px; border-radius: 6px; text-align: center; border-left: 4px solid #2196F3;">
                    <div style="font-size: 0.8em; color: #888; text-transform: uppercase;">Czas Zalewania</div>
                    <div style="font-size: 1.8em; font-weight: bold; margin-top: 5px; color: #64b5f6;">{req_time:.1f} s</div>
                </div>
            """, unsafe_allow_html=True)
            
        with col_m2:
            st.markdown(f"""
                <div style="background: #252525; padding: 15px; border-radius: 6px; text-align: center; border-left: 4px solid #2196F3;">
                    <div style="font-size: 0.8em; color: #888; text-transform: uppercase;">Wymagany Przepływ</div>
                    <div style="font-size: 1.8em; font-weight: bold; margin-top: 5px; color: #64b5f6;">{req_flow:.1f} kg/s</div>
                </div>
            """, unsafe_allow_html=True)
            
        with col_m3:
            st.markdown(f"""
                <div style="background: #252525; padding: 15px; border-radius: 6px; text-align: center; border-left: 4px solid #ff9800;">
                    <div style="font-size: 0.8em; color: #888; text-transform: uppercase;">Max. Pojemność</div>
                    <div style="font-size: 1.8em; font-weight: bold; margin-top: 5px; color: #ffb74d;">{filter_cap:.0f} kg</div>
                </div>
            """, unsafe_allow_html=True)
            
        with col_m4:
            st.markdown(f"""
                <div style="background: #252525; padding: 15px; border-radius: 6px; text-align: center; border-left: 4px solid #ff9800;">
                    <div style="font-size: 0.8em; color: #888; text-transform: uppercase;">Max. Przepływ</div>
                    <div style="font-size: 1.8em; font-weight: bold; margin-top: 5px; color: #ffb74d;">{filter_flow:.1f} kg/s</div>
                </div>
            """, unsafe_allow_html=True)

        with col_m5:
            st.markdown(f"""
                <div style="background: #252525; padding: 15px; border-radius: 6px; text-align: center; border-left: 4px solid #e91e63;">
                    <div style="font-size: 0.7em; color: #888; text-transform: uppercase;">Modyfikacja na strugę</div>
                    <div style="font-size: 1.4em; font-weight: bold; margin-top: 5px; color: #f48fb1;">{mod_min_gs:.1f} - {mod_max_gs:.1f} g/s</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        # ZDERZENIE LOGIKI
        st.markdown("#### Zderzenie Logiki (Popyt vs Podaż)")
        
        flow_icon = "✅" if flow_ok else "❌"
        flow_op = "≤" if flow_ok else ">"
        
        mass_icon = "✅" if mass_ok else "❌"
        mass_op = "≤" if mass_ok else ">"

        st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; background: #1a1a1a; padding: 15px; border-radius: 8px; margin-bottom: 10px; border: 1px solid #333;">
                <div style="font-weight: bold; color: #ccc; width: 30%;">1. Weryfikacja Przepływu (Czasu)</div>
                <div style="display: flex; align-items: center; width: 70%; justify-content: space-around; font-family: monospace; font-size: 1.2em;">
                    <span style="color:#64b5f6;">{req_flow:.1f} kg/s</span>
                    <span style="font-weight: bold; color: #fff; padding: 0 15px;">{flow_op}</span>
                    <span style="color:#ffb74d;">{filter_flow:.1f} kg/s</span>
                    <span style="font-size: 1.5em;">{flow_icon}</span>
                </div>
            </div>

            <div style="display: flex; justify-content: space-between; align-items: center; background: #1a1a1a; padding: 15px; border-radius: 8px; margin-bottom: 10px; border: 1px solid #333;">
                <div style="font-weight: bold; color: #ccc; width: 30%;">2. Weryfikacja Pojemności (Żużla)</div>
                <div style="display: flex; align-items: center; width: 70%; justify-content: space-around; font-family: monospace; font-size: 1.2em;">
                    <span style="color:#64b5f6;">{mass_f:.0f} kg</span>
                    <span style="font-weight: bold; color: #fff; padding: 0 15px;">{mass_op}</span>
                    <span style="color:#ffb74d;">{filter_cap:.0f} kg</span>
                    <span style="font-size: 1.5em;">{mass_icon}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
