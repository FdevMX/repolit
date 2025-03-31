import streamlit as st
from frontend.views.login_view import login_view
from frontend.views.register_view import register_view

def main():
    # Inicializar el estado si no existe
    if 'vista' not in st.session_state:
        st.session_state.vista = "login"
    
    # Sidebar con radio que refleja el estado actual
    st.sidebar.title("Navegación")
    opcion = st.sidebar.radio("Ir a:", ("Iniciar sesión", "Registrarse"), 
                             index=0 if st.session_state.vista == "login" else 1)
    
    # Actualizar el estado cuando cambia el radio
    if (opcion == "Iniciar sesión" and st.session_state.vista != "login") or \
       (opcion == "Registrarse" and st.session_state.vista != "register"):
        st.session_state.vista = "login" if opcion == "Iniciar sesión" else "register"
        st.rerun()
    
    # Mostrar vista según el estado
    if st.session_state.vista == "login":
        login_view()
    else:
        register_view()

if __name__ == "__main__":
    # Cargar estilos
    with open("frontend/assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    main()