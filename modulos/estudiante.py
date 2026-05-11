import streamlit as st
import pandas as pd
import plotly.express as px

def mostrar(data):
    st.title(f"🎓 Panel del Estudiante")
    st.write(f"Bienvenido, {data['nombre']}")
    st.success(f"📖 Grado: {data.get('grado', '11°A')}")
    
    # ========== NOTAS CON GRÁFICOS ==========
    st.subheader("📖 Mis Calificaciones")
    
    # Datos de ejemplo (después vendrán de Supabase)
    notas_ejemplo = [
        {"materia": "Matemáticas", "nota": 4.5, "periodo": 1},
        {"materia": "Ciencias", "nota": 3.8, "periodo": 1},
        {"materia": "Español", "nota": 4.2, "periodo": 1},
        {"materia": "Inglés", "nota": 4.0, "periodo": 1},
        {"materia": "Sociales", "nota": 3.5, "periodo": 1},
    ]
    
    # Crear DataFrame con las notas
    df_notas = pd.DataFrame(notas_ejemplo)
    
    # Calcular promedio general
    promedio_general = df_notas["nota"].mean()
    
    # Mostrar notas en tabla
    for _, row in df_notas.iterrows():
        st.write(f"**{row['materia']}:** {row['nota']}")
    
    st.divider()
    st.write(f"**📊 Promedio General:** {promedio_general:.1f}")
    
    # ========== GRÁFICO DE BARRAS ==========
    fig = px.bar(
        df_notas,
        x="materia",
        y="nota",
        title="📊 Mis Calificaciones por Materia",
        color="nota",
        color_continuous_scale=["red", "yellow", "green"],
        range_color=[0, 5],
        text="nota"
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # ========== TAREAS PENDIENTES ==========
    st.subheader("📋 Tareas Pendientes")
    st.write("• Matemáticas: Taller de fracciones - Entrega: 15/05/2026")
    st.write("• Ciencias: Cuestionario - Entrega: 18/05/2026")
    
    # ========== COMUNICACIONES ==========
    st.subheader("💬 Comunicaciones")
    st.write("💬 Papá: 'Recuerda estudiar para el examen de matemáticas'")
    st.write("💬 Profe Ciencias: 'Revisar el laboratorio para la próxima clase'")
