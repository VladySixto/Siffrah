import streamlit as st
import mysql.connector
from mysql.connector import Error

# Función para conectarse a la base de datos
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',  
            database='Siffrah',  
            user='root',  
            password='root'  
        )
        if connection.is_connected():
            return connection
    except Error as e:
        st.error(f"¡Error al conectarse a la base de datos: {e}!")
        return None

# Función para verificar las credenciales
def verificar_credenciales(username, password):
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM usuario WHERE nombre_usuario = %s AND pass_usuario = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result is not None
    return False

    # Interfaz de Streamlit
    def main():
        st.title("Inicio de sesión")

        username = st.text_input("Nombre de usuario")
        password = st.text_input("Contraseña", type="password")

        if st.button("Iniciar sesión"):
            if username and password:
                if verificar_credenciales(username, password):
                    st.success(f"Bienvenido, {username}!")
                else:
                    st.error("Usuario o contraseña incorrectos")
            else:
                st.warning("Por favor, complete ambos campos")

    if __name__ == "__main__":
        main()
