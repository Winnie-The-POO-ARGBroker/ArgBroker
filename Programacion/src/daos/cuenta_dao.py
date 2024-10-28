from mysql.connector import Error
from service.gestor_bd import GestorDB
from models.metodos_abc import MetodosAbstractos
from models.transaccion import Transaccion

class CuentaDAO(MetodosAbstractos):
    
    def obtener_datos_cuenta(self, id_usuario):
        """Obtiene los datos de una cuenta específica por su ID."""
        with GestorDB() as conexion:
            try:
                query = """
                SELECT numero_cuenta, saldo 
                FROM cuentas 
                WHERE id_usuario = %s
                """
                resultado = conexion.ejecutar_query(query, (id_usuario,))
                return resultado[0] if resultado else None

            except Error as e:
                print(f"Error al acceder a la base de datos: {e}")
                raise

    def obtener_transacciones_por_cuenta(self, id_cuenta):
        """Obtiene las transacciones asociadas a una cuenta específica por su ID de cuenta."""
        with GestorDB() as conexion:
            query = """
                SELECT t.id_transaccion, t.cantidad_acciones, t.monto_total, t.comision, t.fecha_hora, 
                       t.numero_cuenta, t.id_tipo_transaccion, t.id_accion
                FROM transacciones t
                INNER JOIN cuentas c ON t.numero_cuenta = c.numero_cuenta
                WHERE c.id_usuario = %s
            """
            resultado = conexion.ejecutar_query(query, (id_cuenta,))
            return [
                Transaccion(id_transaccion, cantidad_acciones, monto_total, comision, fecha_hora, numero_cuenta, id_tipo_transaccion, id_accion)
                for id_transaccion, cantidad_acciones, monto_total, comision, fecha_hora, numero_cuenta, id_tipo_transaccion, id_accion in resultado
            ] if resultado else []