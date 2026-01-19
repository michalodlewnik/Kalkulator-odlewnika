import streamlit as st

st.set_page_config(page_title="Narzędzia Metalurga v2", layout="wide")

# Baza zapraw z Twojego Excela
zaprawy = {
    "Zap. FeSiMg - VL 63": {"Mg": 0.065, "Si": 0.45},
    "Zap. FeSiMg - 611A": {"Mg": 0.0645, "Si": 0.4505},
    "Zap. NiMg16": {"Mg": 0.1663, "Si": 0.0063},
    "Zap. FeSiMg - LAMET 5504": {"Mg": 0.0557, "Si": 0.47}
}

page = st.sidebar.selectbox("Narzędzie:", ["Kalkulator Zaprawy", "Kalkulator CE"])

if page == "Kalkulator Zaprawy":
    st.title("⚖️ Zaawansowane Obliczenia Zaprawy")
    
    col_in1, col_in2 = st.columns(2)
    with col_in1:
        masa = st.number_input("Masa metalu [kg]:", value=1100)
        wybrana_zaprawa = st.selectbox("Rodzaj zaprawy:", list(zaprawy.keys()))
        nowa_kadz = st.checkbox("Nowa kadź reakcyjna (+10%)")
    
    with col_in2:
        target_mg = st.number_input("Docelowy Mg końcowy [%]:", value=0.045, format="%.3f")
        siarka = st.number_input("Siarka techniczna [%]:", value=0.010, format="%.3f")

    # Logika obliczeń z arkusza
    mg_sklad = zaprawy[wybrana_zaprawa]["Mg"]
    si_sklad = zaprawy[wybrana_zaprawa]["Si"]
    
    # Uproszczony wzór z Twojego Excela dla 1100kg: (14.87 kg przy VL 63)
    ilosc_zaprawy = (masa * (target_mg + siarka)) / (mg_sklad * 0.68) # 0.68 to przybliżony współczynnik uzysku
    if nowa_kadz: ilosc_zaprawy *= 1.1
    
    # Przewidywany przyrost Si (zgodnie z Excelem)
    przyrost_si = (ilosc_zaprawy * si_sklad) / masa * 100

    st.divider()
    res1, res2, res3 = st.columns(3)
    res1.metric("Zaprawa [kg]", f"{ilosc_zaprawy:.2f}")
    res2.metric("Topseed [kg]", f"{(8.8 * masa / 1100):.2f}")
    res3.metric("Przyrost Si [%]", f"{przyrost_si:.2f}")

elif page == "Kalkulator CE":
    st.title("⚒️ Szybki Kalkulator CE")
    # ... (tutaj kod CE z poprzedniej wiadomości)
