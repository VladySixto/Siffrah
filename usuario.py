import mysql.connector
import streamlit as st
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

class Usuario:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host = os.getenv('DB_HOST'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            database = os.getenv('DB_NAME')
        )
        self.cursor = self.connection.cursor(dictionary=True)
            
    def crear_usuario(self,name,password):
        self.cursor.execute('SELECT nombre_usuario FROM usuario')
        list_usuarios = self.cursor.fetchall()
        if (len(list_usuarios)) != 0:
            for i in range(len(list_usuarios)):
                existente=False
                if list_usuarios[i]["nombre_usuario"] == name:
                    st.warning(f"El usuario {name} ya está registrado en la base de datos")
                    existente = True
                    break
            if existente == False:
                self.cursor.execute('SELECT * FROM usuario ORDER BY idusuario DESC LIMIT 1')
                list_usuarios = self.cursor.fetchall()
                id = list_usuarios[0]['idusuario']
                id +=1
                self.cursor.execute('INSERT INTO usuario(idusuario , nombre_usuario, contraseña) VALUES(%s,%s,%s)',(id,name,password))
                self.connection.commit()
                st.success("el usuario se creo correctamente")   
        else:
            id=1
            self.cursor.execute('INSERT INTO usuario(idusuario , nombre_usuario, contraseña) VALUES(%s,%s,%s)',(id,name,password))
            self.connection.commit()
            st.success("el usuario se creo correctamente")
    
    def obtener_usuarios(self):
        self.cursor.execute("SELECT * FROM usuario")
        obtener = self.cursor.fletchall()
        return obtener
    
    def iniciar_sesion(self,name,password):
        self.cursor.execute("SELECT * FROM usuario WHERE nombre_usuario = %s AND contraseña = %s",(name,password))
        user = self.cursor.fetchall()
        if user:
           st.success("se inicio sesion correctamente")
        else:
           st.warning("el usuario y/o contraseña no se encuentran registrados")    
        
# Interfaz de Streamlit
def displayRegistro():
    st.title("Registro de usuario")
    username = st.text_input("Nombre de usuario")
    password = st.text_input("Contraseña", type="password")
    password_2 = st.text_input(" Repita su Contraseña", type="password")

    if st.button("Registrarme"):
        if username and password and password_2 and password == password_2:
            usuario = Usuario()
            usuario.crear_usuario(username, password)
        else:
            if password_2 != password:
                st.warning("las contraseñas no coinciden")
            else:
                st.warning("complete todos los campos")

def displayInicioSesion():
    st.title("Inicio de sesión")
    username = st.text_input("Nombre de usuario")
    password = st.text_input("Contraseña", type="password")
    
    if st.button("Ingresar"):
        usuario = Usuario()
        usuario.iniciar_sesion(username,password)

