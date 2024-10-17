import streamlit as st
import pandas as pd
import usuario
from clientes import DataManagerCliente 
from producto import DataManagerProducto
from venta import DataManagerVenta

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
    if st.sidebar.button("Productos"):
        st.session_state.page = 'Productos'
    if st.sidebar.button("Venta"):
        st.session_state.page = 'Venta'


    if st.session_state.page =="index":
        st.title("Siffrah")
        st.header('Sistema de control de stock')

    if st.session_state.page == 'registro_usuario':
        usuario.displayRegistro()
    
    if st.session_state.page == 'inicio_sesion':
        usuario.displayInicioSesion()
        
    if st.session_state.page == "Clientes":
        objeto = DataManagerCliente()
        objeto.displayClientes()
        
    if st.session_state.page == "Productos":
        objeto = DataManagerProducto()
        objeto.displayProductos()
    
    if st.session_state.page == 'Venta':
        objeto = DataManagerVenta()
        objeto.displayVenta()
    
     
        
if __name__ == "__main__":
    main()
