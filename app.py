import streamlit as st

st.set_page_config(page_title="Narzędzia Metalurga", layout="centered")

# Menu boczne do wyboru narzędzia
page = st.sidebar.selectbox("Wybierz narzędzie:", ["Kalkulator Zaprawy", "Kalkulator CE"])

if page == "Kalkulator Zaprawy":
    st.title("⚖️ Obliczenia Zaprawy do Kadzi")
    st.info("Logika oparta na arkuszu v_2.1 (Zaprawa VL 63)")

    # Dane wejściowe
    masa = st.number_input("Ilość metalu w kadzi [kg]:", value=1100, step=50)
    temp = st.slider("Temperatura spustu [°C]:", 1400, 1550, 1470)
    nowa_kadz = st.checkbox("Czy to nowa kadź reakcyjna? (+10% zaprawy)")

    # Obliczenia na podstawie Twojego Excela
    # Bazowa ilość dla 1100 kg to ok. 14.87 kg przy Mg=0.045% i S=0.01%
    proporcja = masa / 1100
    ilosc_zaprawy = 14.869 * proporcja
    
    if nowa_kadz:
        ilosc_zaprawy *= 1.1

    topseed = 8.8 * proporcja
    kubek = 4.0 * proporcja

    # Wyświetlanie wyników
    st.divider()
    st.header(f"Potrzebna ilość zaprawy: {ilosc_zaprawy:.2f} kg")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Topseed [kg]", f"{topseed:.2f}")
    with col2:
        st.metric("Mod. do kubka [kg]", f"{kubek:.2f}")

    st.caption(f"Wyliczenia dla Mg końcowego 0.045% i S technicznej 0.01%")

elif page == "Kalkulator CE":
    st.title("⚒️ Kalkulator CE")
    c = st.number_input("Węgiel (C) %", value=3.50, step=0.01)
    si = st.number_input("Krzem (Si) %", value=2.10, step=0.01)
    p = st.number_input("Fosfor (P) %", value=0.05, step=0.01)
    
    ce = c + (si + p) / 3
    st.metric("Ekwiwalent Węgla (CE)", f"{ce:.2f}")
