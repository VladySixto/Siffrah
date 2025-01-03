import streamlit as st
import pandas as pd
import usuario
from cliente import DataManagerCliente 
from producto import DataManagerProducto
from venta import DataManagerVenta
from PIL import Image

###Logo
logo = Image.open("logo.png")
###Define sidebar, Se muestra solo si el user esta loggeado, se llama desde el archivo prueba.py en este caso
def cargar_sidebar():
    st.sidebar.title("Menú Principal")
    opciones = st.sidebar.radio("Selecciona una opción", ["Inicio", "Clientes", "Productos", "Ventas", "Cerrar Sesión"])
    st.image(logo)    
    if opciones == "Inicio ":
        st.title("Bienvenido a Siffrah")
        st.write(f"Bienvenido {st.session_state.get('usuario_actual', 'Desconocido')}! ")

    elif opciones == "Clientes":
        st.title("Gestión de Clientes")
        cliente_manager = DataManagerCliente()
        cliente_manager.displayClientes()

    elif opciones == "Productos":
        st.title("Gestión de Productos")
        producto_manager = DataManagerProducto()
        producto_manager.displayProductos()

    elif opciones == "Ventas":
        st.title("Gestión de Ventas")
        venta_manager = DataManagerVenta()
        venta_manager.displayVenta()

    elif opciones == "Cerrar Sesión":
        st.session_state.encontrado = False
        st.session_state.usuario_actual = None
        st.success("Has cerrado sesión")

if __name__ == "__main__":
    cargar_sidebar()
