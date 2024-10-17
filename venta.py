import mysql.connector
import streamlit as st
from dotenv import load_dotenv
import os
import pandas as pd
import time
from producto import DataManagerProducto , Producto

load_dotenv()

class Venta:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host = os.getenv('DB_HOST'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            database = os.getenv('DB_NAME')
        )
        self.cursor = self.connection.cursor(dictionary=True)

if "nueva_fila" not in st.session_state:
    st.session_state.nueva_fila = None

if "df_productos" not in st.session_state:
    st.session_state.df_productos = pd.DataFrame(columns=["Producto","Precio Efectivo","Precio de lista","Cantidad","Total Efectivo","Total Lista"])      
        
class DataManagerVenta:
    def __init__(self) -> None:
        self.db_venta = Venta()
    
    def displayVenta(self):
        st.title("VENTA")
        if st.session_state.nueva_fila:
            nueva_fila = pd.DataFrame([st.session_state.nueva_fila])
            st.session_state.df_productos = pd.concat([st.session_state.df_productos, nueva_fila], ignore_index=True)
            st.session_state.nueva_fila = None
        st.write(st.session_state.df_productos)
        
        if st.button("Cargar producto"):
            self.cargar_prod()
            
    @st.dialog("Cargar Producto")    
    def cargar_prod(self):
        productos = Producto()
        productos = productos.obtener_dato()
        producto_input = st.text_input("escribe el nombre del producto")
        productos_filtrados = [producto for producto in productos if producto_input.lower() in producto["nombre_producto"].lower()]

        if productos_filtrados:
            seleccion = st.selectbox(
                "Productos disponibles:", 
                [producto["nombre_producto"] for producto in productos_filtrados]
            )
            
            producto_seleccionado = next(producto for producto in productos_filtrados if producto["nombre_producto"] == seleccion)
            st.write(f"Has seleccionado: {producto_seleccionado['nombre_producto']}")
            st.write(f"Precio efectivo: {producto_seleccionado['precio_efectivo_producto']}")
            st.write(f"Precio lista: {producto_seleccionado['precio_lista_producto']}")
            st.write(f"Stock disponible: {producto_seleccionado['stock_producto']}")
            cantidad = st.number_input(f"Cuantos {producto_seleccionado['nombre_producto']} va a vender?",step=1, format="%d")
        else:
            st.write("No se encontraron coincidencias")
        
        if st.button("cargar"):
            if producto_seleccionado['stock_producto'] < cantidad:
                st.warning(f"no tiene el suficiente stock de {producto_seleccionado['nombre_producto']}")
            else:
                st.session_state.nueva_fila = {"Producto":producto_seleccionado['nombre_producto'],"Precio Efectivo":producto_seleccionado['precio_efectivo_producto'],"Precio de lista":producto_seleccionado['precio_lista_producto'],"Cantidad":cantidad,"Total Efectivo":1,"Total Lista":2}
                st.rerun()
       
       