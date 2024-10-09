import streamlit as st
import pandas as pd
from clientes import Cliente, DataManagerCliente

def main():
    if "page" not in st.session_state:
        st.session_state.page = "index"

    st.sidebar.title("Menu de opciones")
    if st.sidebar.button("inicio"):
        st.session_state.page = 'index'
    if st.sidebar.button("Iniciar sesión"):
        st.session_state.page = 'inicio_sesion'
    if st.sidebar.button("Registrar usuario"):
        st.session_state.page = 'registro_usuario'
    if st.sidebar.button("Clientes"):
        st.session_state.page = 'Clientes'



    if st.session_state.page =="index":
        st.title("Siffrah")
        st.header('Sistema de control de stock')

    # if st.session_state.page == 'registro_usuario':
    #     usuario.displayRegistro()
    
    # if st.session_state.page == 'inicio_sesion':
    #     usuario.displayInicioSesion()
    if st.session_state.page == "Clientes":
        objeto_cliente = DataManagerCliente()
        objeto_cliente.displayClientes()        
if __name__ == "__main__":
    main()
