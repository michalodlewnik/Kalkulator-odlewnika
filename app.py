import streamlit as st

st.markdown("""
    <style>

      /* 1. Usunięcie marginesów na samej górze strony */
    .block-container { padding-top: 3rem !important; padding-bottom: 5rem !important; }
    
    /* 2. ZMNIEJSZENIE PRZERW MIĘDZY WIERSZAMI */
    div[data-testid="stVerticalBlock"] > div {
        margin-top: -12px !important;
        padding-top: 0px !important;
    }

    /* 3. ZMNIEJSZENIE ODSTĘPÓW POD TYTUŁAMI h1 i h3 */
    h1 { margin-bottom: 0px !important; padding-bottom: 15px !important; }
    h3 { margin-bottom: 0px !important; padding-bottom: 25px !important; }
       
    /* 4. Styl ogólny tekstu */
    html, body, [class*="st-"] { font-size: 20px !important; font-weight: 600; }

    /* 5. WIELKI POMARAŃCZOWY TYTUŁ (h1) */
    h1 { 
        font-size: 50px !important; 
        color: orange !important; /* Poprawiona literówka z oragne */
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
        border-radius: 15px; text-align: center; margin-bottom: 20px;
    }
    .result-val { font-size: 50px !important; font-weight: 800; }
    
    /* 9. Ciemne tło dla sekcji Si */
    .si-box { 
        background-color: #333333; color: #00ff00; padding: 15px; 
        border-radius: 12px; text-align: center;
    }

    /* 10. Zmiejszenie odległości pomiędzy sekcjami */
    hr {
    margin-top: 0px !important;
    margin-bottom: 0px !important;
    }
    </style>
    """, unsafe_allow_html=True)

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

# 4. OBLICZENIA GŁÓWNE (ZAPRAWA)
uzysk = 60.0 
mg_sklad = zaprawy_db[wybrana]["Mg"]
si_sklad_zap = zaprawy_db[wybrana]["Si"]

komponent_mg = (target_mg + 0.76 * (siarka - 0.01) + 0.007)
ilosc_zaprawy = (masa * (komponent_mg / (mg_sklad * uzysk)) * (temp / 1450)) * 100
if nowa_kadz:
    ilosc_zaprawy *= 1.1

# 5. EDYTOWALNY TOPSEED I KUBEK (z domyślnym wyliczeniem)
st.divider()
st.subheader("Obliczone materiały pomocnicze (można edytować):")

proporcja = masa / 1100
domyslny_topseed = round((8.8 * proporcja) * 2) / 2
domyslny_kubek = round((4.0 * proporcja) * 2) / 2

col_mod1, col_mod2 = st.columns(2)
with col_mod1:
    topseed_kg = st.number_input("Topseed [Kg]:", value=domyslny_topseed, step=0.5)
with col_mod2:
    kubek_kg = st.number_input("Modyfikacja do kubka [Kg]:", value=domyslny_kubek, step=0.5)

# 6. PRZYROST Si (Zależny od wpisanych wartości)
si_z_zaprawy = (ilosc_zaprawy * si_sklad_zap) / masa * 100
si_z_topseed = (topseed_kg * 0.485) / masa * 100
si_z_kubka = (kubek_kg * 0.7496) / masa * 100
total_si_inc = si_z_zaprawy + si_z_topseed + si_z_kubka

# 7. WYNIKI KOŃCOWE
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





























