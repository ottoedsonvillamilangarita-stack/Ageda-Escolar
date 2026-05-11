import streamlit as st

def mostrar(data):
    st.title(f"👨‍👩‍👧 Panel del Acudiente")
    st.write(f"Bienvenido, {data['nombre']}")
    
    hijo = st.selectbox("Seleccionar hijo", ["Laura Méndez (11°A)", "Andrés Méndez (10°A)"])
    st.subheader(f"📖 Notas de {hijo}")
    st.write("**Matemáticas:** 4.5")
    st.write("**Ciencias:** 3.8")
    st.write("**Español:** 4.2")
