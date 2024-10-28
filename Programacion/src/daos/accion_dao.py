from service.gestor_bd import GestorDB
from prettytable import PrettyTable
from models.metodos_abc import MetodosAbstractos


class AccionDAO(MetodosAbstractos):

    def listar_acciones_disponibles(self):
        """Lista todas las acciones disponibles."""
        with GestorDB() as conexion:
            query = "SELECT id_accion, simbolo, nombre_empresa, precio_compra, precio_venta FROM acciones"
            acciones = conexion.ejecutar_query(query)
            
            if acciones:
                tabla = PrettyTable()
                tabla.field_names = ["ID", "Símbolo", "Empresa", "Precio Compra", "Precio Venta"]
                tabla._min_table_width = 116

                for accion in acciones:
                    tabla.add_row(accion)
                
                print(tabla)
            else:
                print("No hay acciones disponibles.")

    def comprobar_accion(self, id_accion):
        with GestorDB() as conexion:
            query = "SELECT * FROM acciones WHERE id_accion = %s"
            resultado = conexion.ejecutar_query(query, (id_accion,))
            
            # Verifica tenga al menos un elemento
            if resultado and isinstance(resultado, list) and len(resultado) > 0:
                return resultado[0]  
            return None  

    def obtener_saldo_usuario(self, id_usuario):
        with GestorDB() as conexion:
            query = "SELECT saldo FROM cuentas WHERE id_usuario = %s"
            resultado = conexion.ejecutar_query(query, (id_usuario,))
            return resultado[0][0] if resultado else 0.0
    
    def registrar_transaccion(self, id_usuario, id_accion, cantidad, monto_total, comision, tipo_transaccion):
        """Registra una nueva transacción en la base de datos."""
        with GestorDB() as conexion:
            query = """
                INSERT INTO transacciones (cantidad_acciones, monto_total, comision, fecha_hora, numero_cuenta, 
                                        id_tipo_transaccion, id_accion)
                VALUES (%s, %s, %s, NOW(), 
                    (SELECT numero_cuenta FROM cuentas WHERE id_usuario = %s), 
                    %s, %s)
            """
            conexion.ejecutar_query(query, (cantidad, monto_total, comision, id_usuario, tipo_transaccion, id_accion))
            conexion.confirmar()

    def actualizar_saldo(self, id_usuario, nuevo_saldo):
        with GestorDB() as conexion:
            query = "UPDATE cuentas SET saldo = %s WHERE id_usuario = %s"
            conexion.ejecutar_query(query, (nuevo_saldo, id_usuario))
            conexion.confirmar()
