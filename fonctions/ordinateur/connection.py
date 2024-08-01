import mysql.connector
from mysql.connector import Error
import streamlit as st  
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            port=3306, 
            database='VeoliaRapport',
            user='root',
            password=''
        )
        if connection.is_connected():
            return connection
        else:
            st.error("Failed to connect to MySQL server")
            return None
    except Error as e:
        st.error(f"Error connecting to MySQL: {e}")
        return None
