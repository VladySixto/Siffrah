import streamlit as st 
import mysql.connector
from mysql.connector import Error
import pandas as pd 

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
        st.error(f"Error al conectarse a la base de datos: {e}")
        return None

# Interfaz de clientes
def main():
    connection = create_connection()
    if connection is None: 
        return 
    #Funcion para agregar cliente
    mycursor = connection.cursor()
    op_cliente = st.sidebar.selectbox('Selecciona una opcion',("Agregar Cliente", "Buscar Cliente", "Actulizar Cliente", "Eliminar Cliente"))
    if op_cliente == 'Agregar Cliente':
        st.subheader('Agregar Cliente')
        name_add = st.text_input('Introduzca el nombre del cliente: ')
        surname = st.text_input('Introduzca el apellido del cliente: ')
        if st.button('Agregar'):
            cursor = "insert into clientes (nombre_cliente, apellido_cliente) values (%s,%s)"
            val = (name_add,surname)
            mycursor.execute(cursor,val)
            connection.commit()
            st.success('Cliente agregado satisfactoriamente!')                
#Funcion para buscar y filtrar cliente

    elif op_cliente == 'Buscar Cliente':
        st.subheader ('Buscar Cliente')
        df = pd.read_csv('clientes.csv')
        st.dataframe(df)
#Funcion para actualizar/editar cliente

    elif op_cliente == 'Actulizar Cliente':
        st.subheader ('Actualizar Cliente')
        id_reload = st.number_input('Numero de ID del cliente a actualizar: ',step=1)
        name_reload = st.text_input('Introduzca nuevo nombre: ')
        surname_reload = st.text_input('Introduzca nuevo apellido: ')
        if st.button('Actualizar'):
            sql="update clientes set nombre_cliente=%s, apellido_cliente=%s where idclientes=%s"
            val = (name_reload, surname_reload, id_reload)
            mycursor.execute(sql,val)
            connection.commit()
            st.warning('Se actualizo el cliente satisfactoriamente!')
#Funcion para eliminar cliente

    elif op_cliente == 'Eliminar Cliente':
        st.subheader ('Eliminar Cliente')
        delete = st.number_input('Introduzca el ID del cliente a borrar: ',min_value=1)
        if st.button('Borrar'):
            sql="delete from clientes  where idclientes=%s"
            val = (delete,)
            mycursor.execute(sql,val)
            connection.commit()
            st.error('Se borro el cliente satisfactoriamente!')
if __name__ == "__main__":
    main()
