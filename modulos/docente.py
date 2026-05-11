import streamlit as st

def mostrar(data):
    st.title(f"🍎 Panel del Docente")
    st.write(f"Bienvenido, {data['nombre']}")
    st.success(f"📚 Materia: {data.get('materia', 'No asignada')}")
    
    st.subheader("📚 Mis Cursos")
    st.write("• 11°A - Matemáticas")
    st.write("• 10°A - Matemáticas")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝 Calificaciones"):
            st.info("Próximamente: registrar calificaciones")
    with col2:
        if st.button("📅 Asistencia"):
            st.info("Próximamente: registrar asistencia")
