import streamlit as st

# 1. LOGIKA PAMIĘCI (Session State)
# Musi być na początku, aby resetowanie działało bezbłędnie
if 'topseed_val' not in st.session_state:
    st.session_state.topseed_val = 8.5
if 'kubek_val' not in st.session_state:
    st.session_state.kubek_val = 4.0
if 'last_masa' not in st.session_state:
    st.session_state.last_masa = 1100.0

# 2. STYLE CSS - LAYOUT I KOLORY
st.markdown("""
    <style>
    /* 1. Usunięcie marginesów na samej górze strony */
    .block-container { padding-top: 3rem !important; padding-bottom: 7rem !important; }
    
    /* 2. ZMNIEJSZENIE PRZERW MIĘDZY WIERSZAMI */
    div[data-testid="stVerticalBlock"] > div {
        margin-top: -7px !important;
        padding-top: 0px !important;
    }

    /* 3. ZMNIEJSZENIE ODSTĘPÓW POD TYTUŁAMI h1 i h3 */
    h1 { margin-bottom: 0px !important; padding-bottom: 15px !important; }
    h3 { margin-bottom: 0px !important; padding-bottom: 10px !important; }
       
    /* 4. Styl ogólny tekstu */
    html, body, [class*="st-"] { font-size: 20px !important; font-weight: 600; }

    /* 5. WIELKI POMARAŃCZOWY TYTUŁ (h1) */
    h1 { 
        font-size: 50px !important; 
        color: orange !important; 
        text-align: center; 
        padding-top: 5px !important;
        margin-top: 0px !important;
        display: block !important;
    }

    /* 6. NAPIS "MATERIAŁY POMOCNICZE" (h3) */
    h3 { 
        font-size: 30px !important; 
        color: white !important;
        padding-top: 10px;
    }

    /* 7. Styl pól do wpisywania liczb */
    .stNumberInput input { height: 75px !important; font-size: 32px !important; color: #1f77b4 !important; }
    
    /* 8. Zielone tło dla głównego wyniku */
    .result-box { 
        background-color: #28a745; color: white; padding: 15px; 
        border-radius: 15px; text-align: center; margin-bottom: 15px;
    }
    .result-val { font-size: 50px !important; font-weight: 800; }
    
    /* 9. Ciemne tło dla sekcji Si */
    .si-box { 
        background-color: #333333; color: #00ff00; padding: 15px; 
        border-radius: 12px; text-align: center; margin-bottom: 10px;
    }

    /* 10. Zmniejszenie odległości pomiędzy sekcjami (hr) */
    hr { margin-top: 0px !important; margin-bottom: 0px !important; }

    /* 11. ROZCIĄGNIĘTY ŻÓŁTY PRZYCISK RESETU Z EFEKTAMI */
    div.stButton > button {
        width: 100% !important;
        height: 60px !important;
        background-color: #FFD700 !important;
        color: black !important;
        font-size: 22px !important;
        font-weight: bold !important;
        border-radius: 15px !important;
        border: none !important;
        margin-top: 10px !important;
        transition: all 0.2s ease;
    }
    div.stButton > button:hover { background-color: #FFC400 !important; transform: scale(1.01); }
    div.stButton > button:active { transform: scale(0.98); background-color: #E6B800 !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. TYTUŁ APLIKACJI
st.title("⚖️ Kalkulator zaprawy 1.0")

# 4. BAZA DANYCH ZAPRAW
zaprawy_db = {
    "Zap. FeSiMg - VL 63": {"Mg": 6.5, "Si": 0.45},
    "Zap. FeSiMg - VL 63 (0) - zerówka": {"Mg": 6.5, "Si": 0.47},
    "Zap. FeSiMg - 611A": {"Mg": 6.45, "Si": 0.4505},
    "Zap. NiMg16": {"Mg": 16.63, "Si": 0.0063},
    "Zap. FeSiMg - LAMET 5504": {"Mg": 5.57, "Si": 0.47}
}

# 5. WEJŚCIE DANYCH - PARAMETRY WYTOPU
masa = st.number_input("Ilość metalu w kadzi [Kg]:", value=1100, step=5)
temp = st.number_input("Temperatura spustu [oC]:", value=1480, step=10)
target_mg = st.number_input("Magnez końcowy [%]:", value=0.045, step=0.005, format="%.3f")
siarka = st.number_input("Siarka techniczna [%]:", value=0.010, step=0.001, format="%.3f")
wybrana = st.selectbox("Wybierz zaprawę:", list(zaprawy_db.keys()))
nowa_kadz = st.checkbox("🔥 NOWA KADŹ (+10%)")

# 6. LOGIKA OBLICZEŃ DOMYŚLNYCH
proporcja = masa / 1100
domyslny_topseed = round((8.8 * proporcja) * 2) / 2
domyslny_kubek = round((4.0 * proporcja) * 2) / 2

# Automatyczny reset materiałów pomocniczych przy zmianie masy
if masa != st.session_state.last_masa:
    st.session_state.topseed_val = domyslny_topseed
    st.session_state.kubek_val = domyslny_kubek
    st.session_state.last_masa = masa

# 7. OBLICZENIA METALURGICZNE (ILOŚĆ ZAPRAWY)
uzysk = 60.0 
mg_sklad = zaprawy_db[wybrana]["Mg"]
si_sklad_zap = zaprawy_db[wybrana]["Si"]

komponent_mg = (target_mg + 0.76 * (siarka - 0.01) + 0.007)
ilosc_zaprawy = (masa * (komponent_mg / (mg_sklad * uzysk)) * (temp / 1450)) * 100
if nowa_kadz:
    ilosc_zaprawy *= 1.1

# --- POPRAWIONA LOGIKA W SEKCJI 8 I 9 ---

# Funkcje pomocnicze do zapisu zmian (callbacki)
def update_topseed():
    st.session_state.topseed_val = st.session_state.temp_topseed

def update_kubek():
    st.session_state.kubek_val = st.session_state.temp_kubek

# 8. SEKCJA MATERIAŁÓW POMOCNICZYCH (EDYTOR)
st.divider()
st.subheader("Obliczone materiały pomocnicze (można edytować):")

col1, col2 = st.columns(2)
with col1:
    topseed_kg = st.number_input(
        "Topseed [Kg]:", 
        value=st.session_state.topseed_val, 
        step=0.5, 
        key='temp_topseed', 
        on_change=update_topseed
    )
with col2:
    kubek_kg = st.number_input(
        "Modyfikacja do kubka [Kg]:", 
        value=st.session_state.kubek_val, 
        step=0.5, 
        key='temp_kubek', 
        on_change=update_kubek
    )

# 9. PRZYCISK RESETU
if st.button("🔄 PRZYWRÓĆ SUGEROWANE DAWKI", use_container_width=True):
    st.session_state.topseed_val = domyslny_topseed
    st.session_state.kubek_val = domyslny_kubek
    st.rerun()

# 10. OBLICZENIA PRZYROSTU KRZEMU (Si)
si_z_zaprawy = (ilosc_zaprawy * si_sklad_zap) / masa * 100
si_z_topseed = (topseed_kg * 0.485) / masa * 100
si_z_kubka = (kubek_kg * 0.7496) / masa * 100
total_si_inc = si_z_zaprawy + si_z_topseed + si_z_kubka

# 11. WYŚWIETLENIE WYNIKÓW KOŃCOWYCH
st.markdown(f"""
    <div class="result-box">
        <div style="font-size: 25px;">ILOŚĆ ZAPRAWY</div>
        <div class="result-val">{ilosc_zaprawy:.1f} kg</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f"""
    <div class="si-box">
        <div style="color: white; font-size: 20px;">PRZEWIDYWANY PRZYROST Si Z CAŁEGO ZABIEGU:</div>
        <div style="font-size: 40px; font-weight: 800;">{total_si_inc:.2f} %</div>
    </div>
    """, unsafe_allow_html=True)

