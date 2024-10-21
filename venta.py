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


if "df_productos" not in st.session_state:
    st.session_state.df_productos = pd.DataFrame(columns=["Producto","Precio Efectivo","Precio de lista","Cantidad","Total Efectivo","Total Lista"])      
        
class DataManagerVenta:
    def __init__(self) -> None:
        self.db_venta = Venta()
    
    def displayVenta(self):
        if "nueva_fila" not in st.session_state:
            st.session_state.nueva_fila = None
        st.title("VENTA")
        if st.session_state.nueva_fila !=None :
            nueva_fila = pd.DataFrame([st.session_state.nueva_fila])
            st.session_state.df_productos = pd.concat([st.session_state.df_productos, nueva_fila], ignore_index=True)
            st.session_state.nueva_fila = None
        st.write(st.session_state.df_productos)
        col1,col2,col3,col4 =st.columns([1, 1, 1, 1])
        with col1:
            if st.button("Cargar producto"):
                self.cargar_prod()
        with col2:
            if st.button("borrar producto"):
                df_prod=st.session_state.df_productos
                self.borrar_prod(df_prod)
        with col3:
            if st.button("Vender"):
                df_prod=st.session_state.df_productos
                self.vender(df_prod)
                st.session_state.df_productos = pd.DataFrame(columns=["Producto","Precio Efectivo","Precio de lista","Cantidad","Total Efectivo","Total Lista"])
                st.rerun()      
         
    @st.dialog("Cargar Producto")    # con esta funcion se cargan productos al dataframe df_productos
    def cargar_prod(self):
        productos = Producto()
        productos = productos.obtener_dato()
       
        seleccion = st.selectbox(
            "Productos disponibles:", 
            [producto["nombre_producto"] for producto in productos]
        )
        
        producto_seleccionado = next(producto for producto in productos if producto["nombre_producto"] == seleccion)
        st.write(f"Has seleccionado: {producto_seleccionado['nombre_producto']}")
        st.write(f"Precio efectivo: {producto_seleccionado['precio_efectivo_producto']}")
        st.write(f"Precio lista: {producto_seleccionado['precio_lista_producto']}")
        st.write(f"Stock disponible: {producto_seleccionado['stock_producto']}")
        cantidad = st.number_input(f"Cuantos {producto_seleccionado['nombre_producto']} va a vender?",step=1, format="%d")
        
        if st.button("cargar"):
            df = st.session_state.df_productos['Producto']
            df = df.tolist()
            if producto_seleccionado['stock_producto'] < cantidad:
                st.warning(f"no tiene el suficiente stock de {producto_seleccionado['nombre_producto']}")
            elif producto_seleccionado['nombre_producto'] in df :
                st.warning(f" el producto {producto_seleccionado['nombre_producto']} ya se encuentra en la lista de venta")
            else:
                st.session_state.nueva_fila = {"Producto":producto_seleccionado['nombre_producto'],"Precio Efectivo":producto_seleccionado['precio_efectivo_producto'],"Precio de lista":producto_seleccionado['precio_lista_producto'],"Cantidad":cantidad,"Total Efectivo":producto_seleccionado['precio_efectivo_producto']*cantidad,"Total Lista":producto_seleccionado['precio_lista_producto']*cantidad}
                st.rerun()
                
    @st.dialog("que producto quiere borrar?")
    def borrar_prod(self,df):
        st.write(df)
        indice = st.number_input("que indice desea borrar?",step=1, format="%d")
        if st.button("borrar"):
            if indice == 0:
                df = df.drop(indice)
                st.session_state.df_productos = df
                st.rerun()                
            if indice:
                df = df.drop(indice)
                st.session_state.df_productos = df
                st.rerun()
                
    def vender(self,df):
        df = df.to_numpy()
        nombre_prod = df[:, [0,3]]
        producto = Producto()
        for nombre , cantidad in nombre_prod:
            id=(producto.obtenerID(nombre))
            id= id[0]["idproductos"]
            producto.bajarStock(id,cantidad)
        

       
       