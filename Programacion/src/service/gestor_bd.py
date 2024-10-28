import traceback
import mysql.connector
from mysql.connector import Error

class GestorDB:
     def __init__(self):
         self.conexion = None
         self.transaccion_activa = False
         self.establecer_conexion()

     def __enter__(self):
         self.cursor = self.conexion.cursor()
         return self

     def __exit__(self, exc_type, exc_value, traceback):
         if exc_type is not None:
             self.revertir()  # Rollback
         else:
             self.confirmar()  # Commit
         self.cerrar_conexion()  

     def establecer_conexion(self):
         try:
            
             self.conexion = mysql.connector.connect(
                 host="localhost",
                 user="root",
                 password="4413",
                 database="ArgBrokerDEMO",
                 port=3306,  
             )
         except Error as e:
             print(f"Error al conectar con la base de datos: {e}")
             self.conexion = None

     def ejecutar_query(self, query, valores=None, mantener_transaccion=False):
         conexion_abierta = True
         if self.conexion is None or not self.conexion.is_connected():
             self.establecer_conexion()
             conexion_abierta = False
            

         cursor = self.conexion.cursor()
         try:
             if valores:
                 cursor.execute(query, valores)
             else:
                 cursor.execute(query)
            
             if query.strip().lower().startswith("select"):
                 return cursor.fetchall()

             return cursor.lastrowid

         except Error as e:
             print(f"Error al ejecutar la consulta: {e}")
             traceback.print_exc()
             self.revertir()
             return False
    
         finally:
             cursor.close()
             if not mantener_transaccion:
                 if self.transaccion_activa:
                     try:
                         self.confirmar()
                     except Exception as e:
                         self.revertir()
             if not mantener_transaccion and not self.transaccion_activa and not conexion_abierta:
                 self.cerrar_conexion()

     def iniciar_transaccion(self):
         """Inicia una transacción manualmente."""
         if self.conexion and self.conexion.is_connected():
             try:
                 self.conexion.start_transaction()
                 self.transaccion_activa = True
             except Error as e:
                 print(f"Error al iniciar la transacción: {e}")

     def verificar_existencia(self, tabla, campo, valor):
         """Verifica si existe un registro en la tabla según el campo y valor proporcionados."""
         query = f"SELECT COUNT(*) FROM {tabla} WHERE {campo} = %s"
         resultado = self.ejecutar_query(query, (valor,))
         return resultado[0][0] > 0 if resultado else False

     def confirmar(self):
         """Confirma los cambios en la base de datos."""
         try:
             if self.conexion and self.conexion.is_connected():
                 self.conexion.commit()
                 self.transaccion_activa = False
         except Error as e:
             print(f"Error al confirmar la transacción: {e}")
             self.revertir()

     def revertir(self):
         if self.conexion:
             self.conexion.rollback()
         if self.conexion and self.conexion.is_connected():
             try:
                 self.conexion.commit()
                 self.transaccion_activa = False
             except Error as e:
                 print(f"Error al confirmar la transacción: {e}")
                 self.revertir()

     def cerrar_conexion(self):
         if not self.transaccion_activa and self.conexion and self.conexion.is_connected():
             self.conexion.close()
         elif self.transaccion_activa:
             print("No se cerró la conexión porque hay una transacción en curso.")

     def obtener_cursor(self):
         """Devuelve un cursor para realizar operaciones en la base de datos."""
         if self.conexion and self.conexion.is_connected():
             return self.conexion.cursor(buffered=True)
         else:
             return None
