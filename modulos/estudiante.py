import streamlit as st

def mostrar(data):
    st.title(f"🎓 Panel del Estudiante")
    st.write(f"Bienvenido, {data['nombre']}")
    st.success(f"📖 Grado: {data.get('grado', 'No asignado')}")
    
    st.subheader("📖 Mis Calificaciones")
    st.write("**Matemáticas:** 4.5")
    st.write("**Ciencias:** 3.8")
    st.write("**Español:** 4.2")
    st.write("**Promedio:** 4.2")
    
    st.subheader("📋 Tareas Pendientes")
    st.write("• Matemáticas: Taller de fracciones - Entrega: 15/05/2026")
    
    st.subheader("💬 Comunicaciones")
    st.write("💬 Papá: 'Recuerda estudiar para el examen'")
