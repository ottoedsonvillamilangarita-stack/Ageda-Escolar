import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from utils import get_headers, SUPABASE_URL

def mostrar(data):
    st.title(f"🍎 Panel del Docente")
    st.write(f"Bienvenido, {data['nombre']}")
    
    headers = get_headers()
    
    # Obtener los cursos del docente desde Supabase
    url_cursos = f"{SUPABASE_URL}/rest/v1/asignacion_academica?id_docente=eq.{data.get('id_persona', 0)}"
    response_cursos = requests.get(url_cursos, headers=headers)
    
    if response_cursos.status_code != 200 or not response_cursos.json():
        st.warning("No tienes cursos asignados")
        return
    
    # Preparar lista de cursos
    cursos = []
    for curso in response_cursos.json():
        grado_id = curso.get("id_grado")
        materia_id = curso.get("id_materia")
        
        # Obtener nombre del grado
        url_grado = f"{SUPABASE_URL}/rest/v1/grados?id_grado=eq.{grado_id}"
        resp_grado = requests.get(url_grado, headers=headers)
        grado_nombre = resp_grado.json()[0]["nombre"] if resp_grado.json() else f"Grado {grado_id}"
        
        # Obtener nombre de la materia
        url_materia = f"{SUPABASE_URL}/rest/v1/materias?id_materia=eq.{materia_id}"
        resp_materia = requests.get(url_materia, headers=headers)
        materia_nombre = resp_materia.json()[0]["nombre"] if resp_materia.json() else f"Materia {materia_id}"
        
        cursos.append({
            "id_grado": grado_id,
            "grado_nombre": grado_nombre,
            "id_materia": materia_id,
            "materia_nombre": materia_nombre
        })
    
    # Selector de curso
    curso_seleccionado = st.selectbox(
        "Seleccionar curso",
        cursos,
        format_func=lambda x: f"{x['materia_nombre']} - {x['grado_nombre']}"
    )
    
    if curso_seleccionado:
        grado_id = curso_seleccionado["id_grado"]
        materia_id = curso_seleccionado["id_materia"]
        materia_nombre = curso_seleccionado["materia_nombre"]
        
        st.success(f"📚 Trabajando con: **{materia_nombre}**")
        
        # Obtener estudiantes del grado
        url_estudiantes = f"{SUPABASE_URL}/rest/v1/estudiantes_grados?id_grado=eq.{grado_id}"
        response_estudiantes = requests.get(url_estudiantes, headers=headers)
        
        if response_estudiantes.status_code != 200 or not response_estudiantes.json():
            st.info("No hay estudiantes en este curso")
            return
        
        # Lista de estudiantes
        estudiantes = []
        for est_rel in response_estudiantes.json():
            id_estudiante = est_rel["id_estudiante"]
            url_est = f"{SUPABASE_URL}/rest/v1/personas?id_persona=eq.{id_estudiante}"
            resp_est = requests.get(url_est, headers=headers)
            if resp_est.status_code == 200 and resp_est.json():
                estudiantes.append({
                    "id": id_estudiante,
                    "nombre": resp_est.json()[0]["nombre"]
                })
        
        # ========== ESTADÍSTICAS Y GRÁFICOS ==========
        st.subheader("📊 Estadísticas del Curso")
        
        # Obtener notas de los estudiantes para esta materia
        datos_notas = []
        for estudiante in estudiantes:
            url_notas = f"{SUPABASE_URL}/rest/v1/notas?id_estudiante=eq.{estudiante['id']}&id_materia=eq.{materia_id}&periodo=eq.1"
            resp_notas = requests.get(url_notas, headers=headers)
            
            if resp_notas.status_code == 200 and resp_notas.json():
                nota = resp_notas.json()[0].get("nota", 0)
                datos_notas.append({
                    "estudiante": estudiante['nombre'],
                    "nota": nota
                })
        
        if datos_notas:
            df_notas = pd.DataFrame(datos_notas)
            
            # Calcular estadísticas
            promedio_curso = df_notas["nota"].mean()
            nota_minima = df_notas["nota"].min()
            nota_maxima = df_notas["nota"].max()
            aprobados = len(df_notas[df_notas["nota"] >= 3.0])
            porcentaje_aprobados = (aprobados / len(df_notas)) * 100
            
            # Mostrar métricas
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📊 Promedio Curso", f"{promedio_curso:.1f}")
            with col2:
                st.metric("⬆️ Nota Máxima", f"{nota_maxima:.1f}")
            with col3:
                st.metric("⬇️ Nota Mínima", f"{nota_minima:.1f}")
            with col4:
                st.metric("✅ Aprobados", f"{aprobados}/{len(df_notas)} ({porcentaje_aprobados:.0f}%)")
            
            # Gráfico de barras con todas las notas
            fig = px.bar(
                df_notas,
                x="estudiante",
                y="nota",
                title=f"📊 Notas de {materia_nombre} - Periodo 1",
                color="nota",
                color_continuous_scale=["red", "yellow", "green"],
                range_color=[0, 5],
                text="nota"
            )
            fig.update_traces(textposition="outside")
            fig.update_layout(height=400, xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
            
            # Gráfico de distribución (histograma)
            fig_hist = px.histogram(
                df_notas,
                x="nota",
                nbins=10,
                title="📈 Distribución de Notas",
                color_discrete_sequence=["#3498db"]
            )
            fig_hist.update_layout(height=300)
            st.plotly_chart(fig_hist, use_container_width=True)
            
            # Botón para exportar
            if st.button("📎 Exportar estadísticas a Excel"):
                from utils import exportar_excel
                excel = exportar_excel(datos_notas, f"estadisticas_{materia_nombre}")
                st.download_button(
                    label="📥 Descargar Excel",
                    data=excel,
                    file_name=f"estadisticas_{materia_nombre}.xlsx"
                )
        else:
            st.info("No hay notas registradas para este curso")
        
        st.divider()
        
        # ========== CALIFICACIONES ==========
        tab_calif, tab_asist = st.tabs(["📝 Calificaciones", "📅 Asistencia"])
        
        with tab_calif:
            st.subheader(f"Registrar Notas - {materia_nombre}")
            periodo = st.selectbox("Periodo", [1, 2, 3, 4], format_func=lambda x: f"Periodo {x}")
            
            notas_registradas = {}
            for estudiante in estudiantes:
                # Obtener nota actual si existe
                url_nota = f"{SUPABASE_URL}/rest/v1/notas?id_estudiante=eq.{estudiante['id']}&id_materia=eq.{materia_id}&periodo=eq.{periodo}"
                resp_nota = requests.get(url_nota, headers=headers)
                nota_actual = resp_nota.json()[0]["nota"] if resp_nota.json() else 3.0
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{estudiante['nombre']}**")
                with col2:
                    nota = st.number_input(
                        f"Nota",
                        min_value=0.0,
                        max_value=5.0,
                        step=0.1,
                        value=float(nota_actual),
                        key=f"nota_{estudiante['id']}_{materia_id}_{periodo}",
                        label_visibility="collapsed"
                    )
                    notas_registradas[estudiante['id']] = nota
            
            if st.button("💾 Guardar todas las notas"):
                guardadas = 0
                for estudiante in estudiantes:
                    nota = notas_registradas[estudiante['id']]
                    
                    url_verificar = f"{SUPABASE_URL}/rest/v1/notas?id_estudiante=eq.{estudiante['id']}&id_materia=eq.{materia_id}&periodo=eq.{periodo}"
                    resp_verificar = requests.get(url_verificar, headers=headers)
                    
                    if resp_verificar.status_code == 200 and resp_verificar.json():
                        nota_id = resp_verificar.json()[0]["id_nota"]
                        url_update = f"{SUPABASE_URL}/rest/v1/notas?id_nota=eq.{nota_id}"
                        response_update = requests.patch(
                            url_update,
                            headers={**headers, "Content-Type": "application/json"},
                            json={"nota": nota}
                        )
                        if response_update.status_code == 200:
                            guardadas += 1
                    else:
                        nueva_nota = {
                            "id_estudiante": estudiante['id'],
                            "id_materia": materia_id,
                            "id_grado": grado_id,
                            "periodo": periodo,
                            "nota": nota
                        }
                        response_insert = requests.post(
                            f"{SUPABASE_URL}/rest/v1/notas",
                            headers={**headers, "Content-Type": "application/json"},
                            json=nueva_nota
                        )
                        if response_insert.status_code == 201:
                            guardadas += 1
                
                st.success(f"✅ {guardadas} notas guardadas correctamente")
                st.rerun()
        
        with tab_asist:
            st.subheader("Registrar Asistencia")
            st.info("Próximamente: registro de asistencia por fecha")
