import streamlit as st

st.set_page_config(page_title="Mi Escuela", page_icon="📚")

st.title("📚 Mi Plataforma Escolar")
st.write("Si ves este mensaje, Streamlit está funcionando correctamente.")

usuario = st.text_input("Usuario de prueba")
if st.button("Ingresar"):
    st.success(f"Bienvenido {usuario}!")
