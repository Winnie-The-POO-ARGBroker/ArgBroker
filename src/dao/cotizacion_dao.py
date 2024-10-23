import mysql.connector
from mysql.connector import Error
from service.gestor_bd import GestorDB

class CotizacionDAO:
    def __init__(self, db_connect: GestorDB):
        self.db_connect = db_connect

    def obtener_precio_cotizacion(self, simbolo):
        connection = self.db_connect.connect()
        if connection is None:
            return None
        
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT precio_compra FROM cotizaciones WHERE simbolo = %s', (simbolo,))
            resultado = cursor.fetchone()
            
            if resultado:
                return resultado[0]  # Devuelve el precio de compra
            else:
                return None  # No se encontró cotización
            
        except mysql.connector.Error as e:
            print(f"Error al obtener cotización: {e}")
            return None
        
        finally:
            cursor.close()