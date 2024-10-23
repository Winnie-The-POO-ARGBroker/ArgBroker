import os
from dotenv import load_dotenv
import mysql.connector

# Cargar variables de entorno desde el archivo .env
load_dotenv()

class GestorDB:
    def __init__(self):
        self.connection = None

    def connect(self):
        if self.connection is None or not self.connection.is_connected():
            try:
                self.connection = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME")
              )
            except mysql.connector.Error as e:
                print(f"Error conectando a la base de datos: {e}")
                self.connection = None
        return self.connection

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.connection = None