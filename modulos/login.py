import streamlit as st

def mostrar():
    st.title("📚 Plataforma Escolar")
    st.subheader("Iniciar Sesión")
    
    # Usuarios de prueba (después conectaremos a Supabase)
    usuarios_validos = {
        "estudiante.laura": {"password": "demo2026", "rol": "estudiante", "nombre": "Laura Méndez", "grado": "11°A", "email": "laura.mendez@demo.edu.co"},
        "docente.herrera": {"password": "demo2026", "rol": "docente", "nombre": "Claudia Herrera", "email": "claudia.herrera@demo.edu.co"},
        "acudiente.mendez": {"password": "demo2026", "rol": "acudiente", "nombre": "Carlos Méndez", "email": "carlos.mendez@demo.edu.co"},
        "director.11a": {"password": "demo2026", "rol": "director", "nombre": "Claudia Herrera", "grupo": "11°A", "email": "claudia.herrera@demo.edu.co"},
        "coordinador.rincon": {"password": "demo2026", "rol": "coordinador", "nombre": "Ricardo Rincón", "email": "ricardo.rincon@demo.edu.co"},
        "secretaria": {"password": "demo2026", "rol": "secretaria", "nombre": "Secretaria Académica", "email": "secretaria@demo.edu.co"},
        "supervisor": {"password": "demo2026", "rol": "supervisor", "nombre": "Supervisor", "email": "supervisor@demo.edu.co"},
        "admin": {"password": "demo2026", "rol": "admin", "nombre": "Administrador", "email": "admin@demo.edu.co"}
    }
    
    # Mostrar login o recuperar contraseña
    if "recover_mode" not in st.session_state:
        st.session_state.recover_mode = False
    
    if not st.session_state.recover_mode:
        # Pantalla de login normal
        usuario = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Ingresar", use_container_width=True):
                if usuario in usuarios_validos and usuarios_validos[usuario]["password"] == password:
                    st.session_state.logged_in = True
                    st.session_state.usuario = usuario
                    st.session_state.user_data = usuarios_validos[usuario]
                    st.rerun()
                else:
                    st.error("❌ Usuario o contraseña incorrectos")
        
        with col2:
            if st.button("¿Olvidaste tu contraseña?", use_container_width=True):
                st.session_state.recover_mode = True
                st.rerun()
        
        st.divider()
        st.caption("Usuarios de prueba:")
        st.caption("• estudiante.laura / demo2026")
        st.caption("• docente.herrera / demo2026")
        st.caption("• secretaria / demo2026")
    
    else:
        # Pantalla de recuperar contraseña
        st.subheader("🔐 Recuperar Contraseña")
        st.write("Ingresa tu usuario y te enviaremos instrucciones a tu correo.")
        
        usuario_rec = st.text_input("Usuario")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Enviar instrucciones", use_container_width=True):
                if usuario_rec in usuarios_validos:
                    email = usuarios_validos[usuario_rec]["email"]
                    st.success(f"✅ Se han enviado instrucciones a {email}")
                    st.info("En esta versión demo, tu contraseña es: " + usuarios_validos[usuario_rec]["password"])
                    st.info("En la versión real, recibirías un correo con un enlace para cambiarla.")
                else:
                    st.error("❌ Usuario no encontrado")
        
        with col2:
            if st.button("Volver al inicio de sesión", use_container_width=True):
                st.session_state.recover_mode = False
                st.rerun()
