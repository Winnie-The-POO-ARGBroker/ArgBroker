import mysql.connector
from mysql.connector import Error

class TransaccionDAO:
    def __init__(self, db_connect):
        self.db_connect = db_connect

    def registrar_transaccion(self, usuario_id, simbolo, cantidad, precio_compra):
        connection = self.db_connect.connect()
        if connection is None:
            return

        try:
            cursor = connection.cursor()
            cursor.execute('''INSERT INTO transacciones (usuario_id, simbolo, cantidad, precio_compra, tipo) 
                              VALUES (%s, %s, %s, %s, 'compra')''', (usuario_id, simbolo, cantidad, precio_compra))
            connection.commit()
        except mysql.connector.Error as e:
            print(f"Error al registrar la transacción: {e}")
        finally:
            cursor.close()
