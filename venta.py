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
    
    @st.dialog("Cargar Producto")    
    def cargar_prod(self):
        productos = Producto()
        dic_productos = productos.obtener_dato()
        
        seleccion = {row['nombre_producto']:row['idproductos'] for row in dic_productos}
        
        df_productos = pd.DataFrame(dic_productos)
        
        seleccion_producto = st.selectbox('Seleccionar Producto', seleccion.keys())
        df_productos = df_productos[df_productos['nombre_producto'] == seleccion_producto]
        
        st.write(df_productos)
        producto_seleccionado = seleccion_producto
        st.write(f"Has seleccionado: {producto_seleccionado}")
        st.write(f'---')
        st.write(f"Precio efectivo: {df_productos.iloc[0][2]}")
        st.write(f"Precio lista: {df_productos.iloc[0][3]}")
        st.write(f"Stock disponible: {df_productos.iloc[0][4]}")
        cantidad = st.number_input(f"Cuántos {producto_seleccionado} va a vender?",step=1, format="%d")

        if st.button("cargar"):
            if df_productos.iloc[0][4] < cantidad:
                st.warning(f"No tiene el suficiente stock de {producto_seleccionado}")
            else:
                st.session_state.nueva_fila = {"Producto":producto_seleccionado,"Precio de Lista":df_productos.iloc[0][3], "Precio Efectivo":df_productos.iloc[0][2],"Cantidad":cantidad,"Total Efectivo":(cantidad * df_productos.iloc[0][2]),"Total Lista":(cantidad * df_productos.iloc[0][3])}
                st.rerun()
    
    def displayVenta(self):
        st.title("VENTA")
        if 'nueva_fila' in st.session_state:
            nueva_fila = pd.DataFrame([st.session_state.nueva_fila])
            if st.session_state.nueva_fila!=None:
                st.session_state.df_productos = pd.concat([st.session_state.df_productos, nueva_fila], ignore_index=True)
                st.session_state.nueva_fila = None
        
        evento = {}
        if not(st.session_state.df_productos.empty):
            evento = st.dataframe(st.session_state.df_productos,
                        on_select='rerun',
                        selection_mode='single-row',)            
        
        if st.button("Cargar producto"):
            self.cargar_prod()
        
        if evento!={}:
            if evento['selection']['rows']:
                df_filtrado = st.session_state.df_productos[st.session_state.df_productos.index.isin(evento.selection['rows'])]
                st.write(df_filtrado)
                st.write(evento.selection['rows'])
                
                if 'df_productos' in st.session_state:
                    st.session_state.df_productos.drop(evento.selection['rows'],axis = 0, inplace = True)
                    st.session_state.df_productos = st.session_state.df_productos.reset_index(drop=True)
                    st.rerun()