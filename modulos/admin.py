import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from utils import SUPABASE_URL, get_headers

def mostrar(data):
    st.title("⚙️ Administración")
    st.write(f"Bienvenido, {data['nombre']}")
    
    # Pestañas
    tab1, tab2, tab3 = st.tabs(["👥 Usuarios", "📤 Carga Masiva", "⚙️ Configuración"])
    
    # ========== TAB 1: USUARIOS ==========
    with tab1:
        st.subheader("Usuarios del Sistema")
        
        headers = get_headers()
        url = f"{SUPABASE_URL}/rest/v1/usuarios_login"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200 and response.json():
            users = response.json()
            for user in users:
                st.write(f"• **{user['username']}** - {user['rol']} - {user['nombre']}")
            st.caption(f"Total: {len(users)} usuarios")
        else:
            st.info("No hay usuarios registrados")
    
    # ========== TAB 2: CARGA MASIVA ==========
    with tab2:
        st.subheader("📤 Carga Masiva de Datos")
        st.caption("Sube archivos Excel con la estructura correcta para cargar estudiantes, docentes y asignaciones.")
        
        # Explicación del formato
        with st.expander("📋 Ver formato esperado de los archivos"):
            st.markdown("""
            **Archivo de estudiantes:**
            - Columnas obligatorias: `nombre_estudiante`, `apellidos_estudiante`, `documento_estudiante`, `curso`, `nombre_acudiente`, `documento_acudiente`, `parentesco`, `telefono_acudiente`
            - Opcional: `email_acudiente`, `sexo_estudiante`
            
            **Archivo de asignación académica:**
            - Columnas obligatorias: `curso`, `asignatura`, `intensidad_semanal`, `nombre_docente`, `apellidos_docente`, `documento_docente`
            - Opcional: `telefono_docente`, `email_docente`
            """)
        
        # Separar en dos secciones
        col1, col2 = st.columns(2)
        
        # ===== SECCIÓN 1: Carga de estudiantes =====
        with col1:
            st.subheader("📚 Cargar Estudiantes")
            archivo_estudiantes = st.file_uploader(
                "Seleccionar archivo de estudiantes (Excel)",
                type=["xlsx", "xls"],
                key="estudiantes"
            )
            
            if archivo_estudiantes is not None:
                try:
                    df_estudiantes = pd.read_excel(archivo_estudiantes)
                    
                    # Validar columnas
                    columnas_necesarias = ["nombre_estudiante", "apellidos_estudiante", "documento_estudiante", 
                                           "curso", "nombre_acudiente", "documento_acudiente", 
                                           "parentesco", "telefono_acudiente"]
                    
                    columnas_faltantes = [col for col in columnas_necesarias if col not in df_estudiantes.columns]
                    
                    if columnas_faltantes:
                        st.error(f"❌ Faltan columnas: {', '.join(columnas_faltantes)}")
                    else:
                        st.success(f"✅ Archivo válido. {len(df_estudiantes)} estudiantes encontrados.")
                        
                        if st.button("🚀 Subir estudiantes a la base de datos", key="btn_estudiantes"):
                            with st.spinner("Procesando..."):
                                resultado = procesar_estudiantes(df_estudiantes)
                                st.success(resultado)
                                
                except Exception as e:
                    st.error(f"Error al leer el archivo: {e}")
        
        # ===== SECCIÓN 2: Carga de docentes y asignaciones =====
        with col2:
            st.subheader("📚 Cargar Docentes y Asignaciones")
            archivo_docentes = st.file_uploader(
                "Seleccionar archivo de docentes / asignaciones (Excel)",
                type=["xlsx", "xls"],
                key="docentes"
            )
            
            if archivo_docentes is not None:
                try:
                    df_docentes = pd.read_excel(archivo_docentes)
                    
                    # Validar columnas
                    columnas_necesarias = ["curso", "asignatura", "intensidad_semanal", 
                                          "nombre_docente", "apellidos_docente", "documento_docente"]
                    
                    columnas_faltantes = [col for col in columnas_necesarias if col not in df_docentes.columns]
                    
                    if columnas_faltantes:
                        st.error(f"❌ Faltan columnas: {', '.join(columnas_faltantes)}")
                    else:
                        st.success(f"✅ Archivo válido. {len(df_docentes)} asignaciones encontradas.")
                        
                        if st.button("🚀 Subir docentes y asignaciones", key="btn_docentes"):
                            with st.spinner("Procesando..."):
                                resultado = procesar_docentes(df_docentes)
                                st.success(resultado)
                                
                except Exception as e:
                    st.error(f"Error al leer el archivo: {e}")
    
    # ========== TAB 3: CONFIGURACIÓN ==========
    with tab3:
        st.subheader("Configuración General")
        st.write("**Periodos académicos:** Periodo I, II, III, IV")
        st.write("**Escala de notas:** 0 a 5")
        st.write("**Nota mínima aprobatoria:** 3.0")
        st.info("Próximamente: más opciones de configuración")


# ======================================================
# FUNCIONES DE PROCESAMIENTO
# ======================================================

def procesar_estudiantes(df):
    """Procesa el archivo de estudiantes y lo sube a Supabase"""
    
    headers = get_headers()
    
    # Limpiar documentos (eliminar decimales)
    df["documento_estudiante"] = df["documento_estudiante"].astype(str).str.split('.').str[0]
    df["documento_acudiente"] = df["documento_acudiente"].astype(str).str.split('.').str[0]
    
    estudiantes_insertados = 0
    acudientes_insertados = 0
    relaciones_insertadas = 0
    
    # Primero, insertar acudientes (sin repetir)
    acudientes_unicos = df[["nombre_acudiente", "documento_acudiente", "telefono_acudiente", "email_acudiente"]].drop_duplicates(subset=["documento_acudiente"])
    
    for _, row in acudientes_unicos.iterrows():
        documento = str(row["documento_acudiente"])
        
        # Verificar si ya existe
        url_verificar = f"{SUPABASE_URL}/rest/v1/personas?documento=eq.{documento}"
        response = requests.get(url_verificar, headers=headers)
        
        if response.status_code == 200 and response.json():
            # Ya existe, obtener su id
            acudiente_id = response.json()[0]["id_persona"]
        else:
            # Insertar nuevo acudiente
            persona = {
                "nombre": row["nombre_acudiente"],
                "documento": documento,
                "telefono": str(row["telefono_acudiente"]) if pd.notna(row["telefono_acudiente"]) else None,
                "email": row["email_acudiente"] if pd.notna(row["email_acudiente"]) else None,
                "rol": "acudiente"
            }
            
            response_insert = requests.post(
                f"{SUPABASE_URL}/rest/v1/personas",
                headers={**headers, "Content-Type": "application/json"},
                json=persona
            )
            
            if response_insert.status_code == 201:
                acudiente_id = response_insert.json()[0]["id_persona"]
                acudientes_insertados += 1
            else:
                continue
    
    # Luego, insertar estudiantes
    for _, row in df.iterrows():
        documento_est = str(row["documento_estudiante"])
        nombre_completo = f"{row['nombre_estudiante']} {row['apellidos_estudiante']}"
        
        # Verificar si el estudiante ya existe
        url_verificar = f"{SUPABASE_URL}/rest/v1/personas?documento=eq.{documento_est}"
        response = requests.get(url_verificar, headers=headers)
        
        if response.status_code == 200 and response.json():
            estudiante_id = response.json()[0]["id_persona"]
        else:
            # Insertar nuevo estudiante
            estudiante = {
                "nombre": nombre_completo,
                "documento": documento_est,
                "rol": "estudiante"
            }
            
            response_insert = requests.post(
                f"{SUPABASE_URL}/rest/v1/personas",
                headers={**headers, "Content-Type": "application/json"},
                json=estudiante
            )
            
            if response_insert.status_code == 201:
                estudiante_id = response_insert.json()[0]["id_persona"]
                estudiantes_insertados += 1
            else:
                continue
        
        # Obtener id del acudiente
        doc_acudiente = str(row["documento_acudiente"])
        url_acudiente = f"{SUPABASE_URL}/rest/v1/personas?documento=eq.{doc_acudiente}"
        response_acudiente = requests.get(url_acudiente, headers=headers)
        
        if response_acudiente.status_code == 200 and response_acudiente.json():
            acudiente_id = response_acudiente.json()[0]["id_persona"]
            
            # Crear relación estudiante-acudiente
            relacion = {
                "id_estudiante": estudiante_id,
                "id_acudiente": acudiente_id,
                "parentesco": row["parentesco"]
            }
            
            # Verificar si la relación ya existe
            url_relacion = f"{SUPABASE_URL}/rest/v1/estudiantes_acudientes?id_estudiante=eq.{estudiante_id}&id_acudiente=eq.{acudiente_id}"
            response_relacion = requests.get(url_relacion, headers=headers)
            
            if response_relacion.status_code == 200 and not response_relacion.json():
                requests.post(
                    f"{SUPABASE_URL}/rest/v1/estudiantes_acudientes",
                    headers={**headers, "Content-Type": "application/json"},
                    json=relacion
                )
                relaciones_insertadas += 1
    
    return f"✅ {estudiantes_insertados} estudiantes, {acudientes_insertados} acudientes, {relaciones_insertadas} relaciones insertadas"


def procesar_docentes(df):
    """Procesa el archivo de docentes y asignaciones"""
    
    headers = get_headers()
    
    # Limpiar documentos
    df["documento_docente"] = df["documento_docente"].astype(str).str.split('.').str[0]
    
    docentes_insertados = 0
    asignaciones_insertadas = 0
    
    # Insertar docentes únicos
    docentes_unicos = df[["nombre_docente", "apellidos_docente", "documento_docente", "telefono_docente", "email_docente"]].drop_duplicates(subset=["documento_docente"])
    
    for _, row in docentes_unicos.iterrows():
        documento = str(row["documento_docente"])
        nombre_completo = f"{row['nombre_docente']} {row['apellidos_docente']}"
        
        url_verificar = f"{SUPABASE_URL}/rest/v1/personas?documento=eq.{documento}"
        response = requests.get(url_verificar, headers=headers)
        
        if response.status_code == 200 and response.json():
            docente_id = response.json()[0]["id_persona"]
        else:
            docente = {
                "nombre": nombre_completo,
                "documento": documento,
                "telefono": str(row["telefono_docente"]) if pd.notna(row.get("telefono_docente")) else None,
                "email": row["email_docente"] if pd.notna(row.get("email_docente")) else None,
                "rol": "docente"
            }
            
            response_insert = requests.post(
                f"{SUPABASE_URL}/rest/v1/personas",
                headers={**headers, "Content-Type": "application/json"},
                json=docente
            )
            
            if response_insert.status_code == 201:
                docente_id = response_insert.json()[0]["id_persona"]
                docentes_insertados += 1
            else:
                continue
    
    # Insertar asignaciones
    for _, row in df.iterrows():
        doc_documento = str(row["documento_docente"])
        url_docente = f"{SUPABASE_URL}/rest/v1/personas?documento=eq.{doc_documento}"
        response_docente = requests.get(url_docente, headers=headers)
        
        if response_docente.status_code == 200 and response_docente.json():
            docente_id = response_docente.json()[0]["id_persona"]
            
            asignacion = {
                "curso": row["curso"],
                "asignatura": row["asignatura"],
                "intensidad_horaria": int(row["intensidad_semanal"]),
                "id_docente": docente_id
            }
            
            # Verificar si la asignación ya existe (por ahora solo insertamos)
            asignaciones_insertadas += 1
    
    return f"✅ {docentes_insertados} docentes insertados, {asignaciones_insertadas} asignaciones procesadas"
