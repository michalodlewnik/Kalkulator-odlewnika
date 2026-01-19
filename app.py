import streamlit as st

st.set_page_config(page_title="Kalkulator Odlewnika", layout="centered")

st.title("⚒️ Kalkulator Metalurga")
st.subheader("Firma: Odlewnie Polskie S.A.")

# Pola do wprowadzania danych
st.markdown("### Skład chemiczny [%]")
col1, col2, col3 = st.columns(3)

with col1:
    c = st.number_input("Węgiel (C)", value=3.50, step=0.01, format="%.2f")
with col2:
    si = st.number_input("Krzem (Si)", value=2.10, step=0.01, format="%.2f")
with col3:
    p = st.number_input("Fosfor (P)", value=0.05, step=0.01, format="%.2f")

# Obliczenia
ce = c + (si + p) / 3

# Wyświetlanie wyniku
st.divider()
st.metric(label="Ekwiwalent Węgla (CE)", value=f"{ce:.2f}")

# Interpretacja inżynierska
if ce < 4.25:
    st.info("Stop podeutektyczny")
elif ce > 4.35:
    st.warning("Stop nadeutektyczny")
else:
    st.success("Stop eutektyczny")