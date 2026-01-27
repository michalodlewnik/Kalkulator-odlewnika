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
    /* Obniżenie tytułu */
    .block-container { 
        padding-top: 3.5rem !important; 
        padding-bottom: 3rem !important; 
    }
    
    /* Nagłówki */
    h1 { color: #00BFFF !important; text-align: center; margin-bottom: 5px !important; font-size: 36px !important; }
    h2 { color: #FFA500 !important; font-size: 24px !important; margin-bottom: 5px !important; }
    
    /* Nagłówki sekcji */
    .custom-header {
        font-size: 22px !important;
        font-weight: 600 !important;
        color: white !important;
        margin-bottom: 10px !important;
        padding-top: 10px !important;
        text-align: center;
    }
    
    /* Karty wyników */
    .result-box { 
        background-color: #28a745; color: white; padding: 15px; 
        border-radius: 10px; text-align: center; margin-top: 10px; margin-bottom: 10px;
    }
    
    /* Karta wyniku Si/CE (Czarna) */
    .si-box { 
        background-color: #333333; color: #00ff00; padding: 15px; 
        border-radius: 10px; text-align: center; margin-top: 10px; margin-bottom: 10px;
        border: 1px solid #444;
    }
    
    /* Styl wartości w wynikach */
    .result-val { font-size: 35px !important; font-weight: 800; display: block; margin-top: 5px;}
    .result-label { font-size: 20px !important; font-weight: 600; text-transform: uppercase; }
    
    /* Inputy i Suwaki */
    .stNumberInput input { height: 50px !important; font-size: 22px !important; color: #1f77b4 !important; }
    .stSlider [data-baseweb="slider"] { margin-bottom: 5px !important; }
    
    /* Przycisk Reset */
    div.stButton > button {
        background-color: #FFD700 !important; color: black !important;
        font-size: 20px !important; font-weight: bold !important; border-radius: 12px !important; border: none !important;
        transition: all 0.1s ease-in-out;
    }
    div.stButton > button:active { transform: scale(0.95) !important; background-color: #e6c200 !important; }
    
    /* Zakładki */
    .stTabs [data-baseweb="tab-list"] { gap: 5px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #333; border-radius: 10px; color: white; padding: 10px; }
    .stTabs [aria-selected="true"] { background-color: #00BFFF !important; color: black !important; }
    
    hr { margin-top: 5px !important; margin-bottom: 5px !important; border-color: #555; }
    </style>
""", unsafe_allow_html=True)

st.title("🔬 Panel Specjalisty 4.0")

# --- 3. LOGIKA PAMIĘCI ---
if 'topseed_val' not in st.session_state: st.session_state.topseed_val = 8.5
if 'kubek_val' not in st.session_state: st.session_state.kubek_val = 4.0
if 'last_masa' not in st.session_state: st.session_state.last_masa = 1100.0

# --- 4. ZAKŁADKI (TERAZ 3) ---
tab1, tab2, tab3 = st.tabs(["⚖️ 1. ZAPRAWA", "📊 2. KOREKTA", "🧱 3. ŚCIANKA"])

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
    
    st.markdown('<div class="custom-header">Zakładany Uzysk Mg [%]:</div>', unsafe_allow_html=True)
    uzysk_custom = st.slider("", 45, 75, value=60, step=1, label_visibility="collapsed")

    proporcja = masa / 1100
    domyslny_topseed = max(4.0, min(12.0, round((8.8 * proporcja
