import streamlit as st
from modulos import login, estudiante, docente, acudiente, director, coordinador, secretaria, supervisor, admin

st.set_page_config(page_title="Plataforma Escolar", page_icon="📚", layout="wide")

# Inicializar sesión
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Mostrar login o panel según corresponda
if not st.session_state.logged_in:
    login.mostrar()
else:
    # Barra lateral común
    with st.sidebar:
        st.write(f"👤 {st.session_state.user_data['nombre']}")
        st.write(f"📌 Rol: {st.session_state.user_data['rol']}")
        st.divider()
        if st.button("🚪 Cerrar Sesión"):
            st.session_state.logged_in = False
            st.rerun()
    
    # Mostrar el panel según el rol
    rol = st.session_state.user_data["rol"]
    data = st.session_state.user_data
    
    if rol == "estudiante":
        estudiante.mostrar(data)
    elif rol == "docente":
        docente.mostrar(data)
    elif rol == "acudiente":
        acudiente.mostrar(data)
    elif rol == "director":
        director.mostrar(data)
    elif rol == "coordinador":
        coordinador.mostrar(data)
    elif rol == "secretaria":
        secretaria.mostrar(data)
    elif rol == "supervisor":
        supervisor.mostrar(data)
    elif rol == "admin":
        admin.mostrar(data)
    
    st.divider()
    st.caption("📚 Plataforma Escolar Demo - 2026")
