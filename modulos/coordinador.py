import streamlit as st

def mostrar(data):
    st.title(f"📋 Coordinación Académica")
    st.write(f"Bienvenido, {data['nombre']}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Estudiantes", "156")
    with col2:
        st.metric("Total Docentes", "18")
    with col3:
        st.metric("Total Cursos", "12")
