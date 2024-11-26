import mysql.connector
import streamlit as st
from dotenv import load_dotenv
import os
import pandas as pd
import time
from producto import DataManagerProducto, Producto
from cliente import Cliente

# Cargar variables de entorno
load_dotenv()

class Venta:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        self.cursor = self.connection.cursor(dictionary=True)

# Inicializar estados de sesión
if "df_productos" not in st.session_state:
    st.session_state.df_productos = pd.DataFrame(columns=["Producto", "Precio Efectivo", "Precio de lista", "Cantidad", "Total Efectivo", "Total Lista"])

if "totales" not in st.session_state:
    st.session_state["totales"] = pd.DataFrame([[0, 0]], columns=["TOTAL EFECTIVO", "TOTAL LISTA"])

class DataManagerVenta:
    def __init__(self) -> None:
        self.db_venta = Venta()
    
    def displayVenta(self):
        if "nueva_fila" not in st.session_state:
            st.session_state.nueva_fila = None
        
        st.title("VENTA")
        
        # Agregar producto a la lista
        if st.session_state.nueva_fila is not None:
            nueva_fila = pd.DataFrame([st.session_state.nueva_fila])
            st.session_state.df_productos = pd.concat([st.session_state.df_productos, nueva_fila], ignore_index=True)
            st.session_state.nueva_fila = None
        
        # Mostrar lista de productos y totales
        st.write(st.session_state.df_productos)
        st.session_state["totales"].loc[0, "TOTAL LISTA"] = int(st.session_state.df_productos["Total Lista"].sum())
        st.session_state["totales"].loc[0, "TOTAL EFECTIVO"] = int(st.session_state.df_productos["Total Efectivo"].sum())
        st.write(st.session_state["totales"])
        
        # Botones para interactuar con la venta
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
        with col1:
            if st.button("Cargar producto"):
                self.cargar_prod()
        with col2:
            if st.button("Borrar producto"):
                self.borrar_prod(st.session_state.df_productos)
        with col3:
            if st.button("Venta efectivo"):
                self.vender(st.session_state.df_productos, type="efectivo")
                self.reset_venta()
        with col4:
            if st.button("Venta de lista"):
                self.vender(st.session_state.df_productos, type="lista")
                self.reset_venta()
        with col5:
            if st.button("Venta a cuenta"):
                self.vender(st.session_state.df_productos, type="cuenta")
                self.reset_venta()
    
    def reset_venta(self):
        st.session_state.df_productos = pd.DataFrame(columns=["Producto", "Precio Efectivo", "Precio de lista", "Cantidad", "Total Efectivo", "Total Lista"])
        st.rerun()

    @st.dialog("Cargar Producto")
    def cargar_prod(self):
        productos = Producto().obtener_dato()
        seleccion = st.selectbox("Productos disponibles:", [producto["nombre_producto"] for producto in productos])
        producto_seleccionado = next(producto for producto in productos if producto["nombre_producto"] == seleccion)
        
        st.write(f"Has seleccionado: {producto_seleccionado['nombre_producto']}")
        st.write(f"Precio efectivo: {producto_seleccionado['precio_efectivo_producto']}")
        st.write(f"Precio lista: {producto_seleccionado['precio_lista_producto']}")
        st.write(f"Stock disponible: {producto_seleccionado['stock_producto']}")
        
        cantidad = st.number_input(f"Cuántos {producto_seleccionado['nombre_producto']} desea vender?", step=1, format="%d")
        if st.button("Cargar"):
            df = st.session_state.df_productos['Producto'].tolist()
            if cantidad <= 0:
                st.warning("La cantidad a vender debe ser mayor a 0")
            elif producto_seleccionado['stock_producto'] < cantidad:
                st.warning(f"No tiene suficiente stock de {producto_seleccionado['nombre_producto']}")
            elif producto_seleccionado['nombre_producto'] in df:
                st.warning(f"El producto {producto_seleccionado['nombre_producto']} ya está en la lista de venta")
            else:
                st.session_state.nueva_fila = {
                    "Producto": producto_seleccionado['nombre_producto'],
                    "Precio Efectivo": producto_seleccionado['precio_efectivo_producto'],
                    "Precio de lista": producto_seleccionado['precio_lista_producto'],
                    "Cantidad": cantidad,
                    "Total Efectivo": producto_seleccionado['precio_efectivo_producto'] * cantidad,
                    "Total Lista": producto_seleccionado['precio_lista_producto'] * cantidad
                }
                st.rerun()

    @st.dialog("Qué producto quiere borrar?")
    def borrar_prod(self, df):
        st.write(df)
        indice = st.number_input("Índice del producto a borrar:", step=1, format="%d")
        if st.button("Borrar"):
            if 0 <= indice < len(df):
                st.session_state["totales"].loc[0, "TOTAL EFECTIVO"] -= df.iloc[indice]["Total Efectivo"]
                st.session_state["totales"].loc[0, "TOTAL LISTA"] -= df.iloc[indice]["Total Lista"]
                st.session_state.df_productos = df.drop(indice).reset_index(drop=True)
                st.rerun()
            else:
                st.warning("Índice no válido")

    def vender(self, df, type=None):
        df = df.to_numpy()
        nombre_prod = df[:, [0, 3]]
        producto = Producto()
        
        for nombre, cantidad in nombre_prod:
            id = producto.obtenerID(nombre)
            id = id[0]["idproductos"]
            producto.bajarStock(id, cantidad)
        
        st.success(f"Venta realizada con tipo: {type}")
