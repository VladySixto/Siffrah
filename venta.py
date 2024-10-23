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
            host = os.getenv('DB_HOST_S'),
            user = os.getenv('DB_USER_S'),
            password = os.getenv('DB_PASSWORD_S'),
            database = os.getenv('DB_NAME_S')
        )
        self.cursor = self.connection.cursor(dictionary=True)


if "df_productos" not in st.session_state:
    st.session_state.df_productos = pd.DataFrame(columns=["Producto","Precio Efectivo","Precio de lista","Cantidad","Total Efectivo","Total Lista"])      
if "totales" not in st.session_state:
    st.session_state["totales"] = pd.DataFrame([[0, 0]], columns=["TOTAL EFECTIVO", "TOTAL LISTA"])

class DataManagerVenta:
    def __init__(self) -> None:
        self.db_venta = Venta()
    
    def displayVenta(self):
        if "nueva_fila" not in st.session_state:
            st.session_state.nueva_fila = None
        st.title("VENTA")
        if st.session_state.nueva_fila !=None :  
            # aca se carga el nuevo producto a la lista de venta
            nueva_fila = pd.DataFrame([st.session_state.nueva_fila])
            st.session_state.df_productos = pd.concat([st.session_state.df_productos, nueva_fila], ignore_index=True)
            
            st.session_state.nueva_fila = None
            # aca sumamos los precios crear el dataframe con los totales
            totales = nueva_fila.to_numpy()
            totalEf = totales[0,4]
            totalList = totales[0,5]
            st.session_state["totales"].loc[0, "TOTAL EFECTIVO"] += totalEf
            st.session_state["totales"].loc[0, "TOTAL LISTA"] += totalList
        st.write(st.session_state.df_productos) #se muestra en pantalla la lista de venta
        
        st.write(st.session_state["totales"]) # esto muestra los totales de los productos en la lista de venta
        
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
        st.write(sum(st.session_state.df_productos['Total Efectivo']))
        st.write(sum(st.session_state.df_productos['Total Lista']))
        
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
            if cantidad == 0:
                st.warning("la cantidad a vender debe ser mayor a 0")
            elif producto_seleccionado['stock_producto'] < cantidad :
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
                totalEf=(df.iloc[0, 4])
                totalList=(df.iloc[0, 5])
                st.session_state["totales"].loc[0, "TOTAL EFECTIVO"] -= totalEf
                st.session_state["totales"].loc[0, "TOTAL LISTA"] -= totalList
                df = df.drop(indice)
                st.session_state.df_productos = df
                st.rerun()     
            if indice !=0 : 
                totalEf=(df.iloc[0, 4])
                totalList=(df.iloc[0, 5])
                st.session_state["totales"].loc[0, "TOTAL EFECTIVO"] -= totalEf
                st.session_state["totales"].loc[0, "TOTAL LISTA"] -= totalList
                df = df.drop(indice)
                st.session_state.df_productos = df
                st.rerun()
            

            
            st.rerun()
            
                
    def vender(self,df):
        df = df.to_numpy()
        nombre_prod = df[:, [0,3]]
        producto = Producto()
        for nombre , cantidad in nombre_prod:
            id=(producto.obtenerID(nombre))
            id= id[0]["idproductos"]
            producto.bajarStock(id,cantidad)
        

       
       