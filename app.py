import streamlit as st

# 1. STYLE CSS - TWOJA DOPRACOWANA STRUKTURA
st.markdown("""
    <style>
    /* Usunięcie marginesów na samej górze strony */
    .block-container { padding-top: 1rem !important; padding-bottom: 5rem !important; }
    
    /* ZMNIEJSZENIE PRZERW MIĘDZY WIERSZAMI */
    div[data-testid="stVerticalBlock"] > div {
        margin-top: -7px !important;
        padding-top: 0px !important;
    }

    /* ZMNIEJSZENIE ODSTĘPÓW POD TYTUŁAMI h1 i h3 */
    h1 { margin-bottom: 0px !important; padding-bottom: 15px !important; }
    h3 { margin-bottom: 0px !important; padding-bottom: 10px !important; }
        
    /* Styl ogólny tekstu */
    html, body, [class*="st-"] { font-size: 20px !important; font-weight: 600; }

    /* WIELKI POMARAŃCZOWY TYTUŁ (h1) */
    h1 { 
        font-size: 50px !important; 
        color: orange !important; 
        text-align: center; 
        padding-top: 5px !important;
        margin-top: 0px !important;
        display: block !important;
    }

    /* NAPIS "MATERIAŁY POMOCNICZE" (h3) */
    h3 { 
        font-size: 30px !important; 
        color: white !important;
        padding-top: 10px;
    }

    /* Styl pól do wpisywania liczb */
    .stNumberInput input { height: 75px !important; font-size: 32px !important; color: #1f77b4 !important; }
    
    /* Zielone tło dla głównego wyniku */
    .result-box { 
        background-color: #28a745; color: white; padding: 15px; 
        border-radius: 15px; text-align: center; margin-bottom: 10px;
    }
    .result-val { font-size: 50px !important; font-weight: 800; }
    
    /* Ciemne tło dla sekcji Si */
    .si-box { 
        background-color: #333333; color: #00ff00; padding: 15px; 
        border-radius: 12px; text-align: center;
    }

    /* Styl dla przycisku Reset */
    .stButton > button {
        width: 100%; height: 50px; background-color: #ff4b4b; color: white;
        font-size: 18px; font-weight: bold; border-radius: 10px; border: none;
        margin-top: 10px;
    }

    /* Zmniejszenie odległości pomiędzy sekcjami */
    hr { margin-top: 0px !important; margin-bottom: 0px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIKA STANU (Session State - zapamiętywanie masy) ---
if 'last_masa' not in st.session_state:
    st.session_state['last_masa'] = 1100.0

st.title("⚖️ Kalkulator zaprawy 1.0")

# 2. BAZA ZAPRAW
zaprawy_db = {
    "Zap. FeSiMg - VL 63": {"Mg": 6.5, "Si": 0.45},
    "Zap. FeSiMg - VL 63 (0) - zerówka": {"Mg": 6.5, "Si": 0.47},
    "Zap. FeSiMg - 611A": {"Mg": 6.45, "Si": 0.4505},
    "Zap. NiMg16": {"Mg": 16.63, "Si": 0.0063},
    "Zap. FeSiMg - LAMET 5504": {"Mg": 5.57, "Si": 0.47}
}

# 3. WEJŚCIE DANYCH
masa = st.number_input("Ilość metalu w kadzi [Kg]:", value=1100, step=5)
temp = st.number_input("Temperatura spustu [oC]:", value=1480, step=10)
target_mg = st.number_input("Magnez końcowy [%]:", value=0.045, step=0.005, format="%.3f")
siarka = st.number_input("Siarka techniczna [%]:", value=0.010, step=0.001, format="%.3f")
wybrana = st.selectbox("Wybierz zaprawę:", list(zaprawy_db.keys()))
nowa_kadz = st.checkbox("🔥 NOWA KADŹ (+10%)")

# Obliczenia sugerowane wg Twojego Excela
proporcja = masa / 1100
domyslny_topseed = round((8.8 * proporcja) * 2) / 2
domyslny_kubek = round((4.0 * proporcja) * 2) / 2

# RESET JEŚLI MASA SIĘ ZMIENIŁA
if masa != st.session_state['last_masa']:
    st.session_state['topseed_val'] = domyslny_topseed
    st.session_state['kubek_val'] = domyslny_kubek
    st.session_state['last_masa'] = masa

# Inicjalizacja pól w pamięci
if 'topseed_val' not in st.session_state: st.session_state['topseed_val'] = domyslny_topseed
if 'kubek_val' not in st.session_state: st.session_state['kubek_val'] = domyslny_kubek

# 4. OBLICZENIA GŁÓWNE (ZAPRAWA)
uzysk = 60.0 
mg_sklad = zaprawy_db[wybrana]["Mg"]
si_sklad_zap = zaprawy_db[wybrana]["Si"]

komponent_mg = (target_mg + 0.76 * (siarka - 0.01) + 0.007)
ilosc_zaprawy = (masa * (komponent_mg / (mg_sklad * uzysk)) * (temp / 1450)) * 100
if nowa_kadz:
    ilosc_zaprawy *= 1.1

# 5. MATERIAŁY POMOCNICZE (Edytowalne z pamięcią)
st.divider()
st.subheader("Materiały pomocnicze (można edytować):")

col_mod1, col_mod2 = st.columns(2)
with col_mod1:
    topseed_kg = st.number_input("Topseed [Kg]:", key='topseed_val', step=0.5)
with col_mod2:
    kubek_kg = st.number_input("Modyfikacja do kubka [Kg]:", key='kubek_val', step=0.5)

# Przycisk ręcznego resetu
if st.button("🔄 PRZYWRÓĆ SUGEROWANE DAWKI"):
    st.session_state['topseed_val'] = domyslny_
