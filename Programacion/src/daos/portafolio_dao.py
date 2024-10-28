from service.gestor_bd import GestorDB
from prettytable import PrettyTable
from models.metodos_abc import MetodosAbstractos

class PortafolioDAO(MetodosAbstractos):

    def asignar_acciones(self, id_usuario, id_accion, cantidad, precio_compra, precio_venta):
        with GestorDB() as conexion:
            query = """
                INSERT INTO portafolio (id_usuario, id_accion, cantidad_acciones, 
                                                    precio_compra, precio_venta)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE cantidad_acciones = cantidad_acciones + %s
            """
            conexion.ejecutar_query(
                query, (id_usuario, id_accion, cantidad, precio_compra, precio_venta, cantidad)
            )
            conexion.confirmar()

    def listar_acciones_del_usuario(self, id_usuario):
        with GestorDB() as conexion:
            query = """
                SELECT a.id_accion, a.nombre_empresa, p.cantidad_acciones, a.precio_compra
                FROM portafolio p
                JOIN acciones a ON p.id_accion = a.id_accion
                WHERE p.id_usuario = %s
            """
            resultados = conexion.ejecutar_query(query, (id_usuario,))
            return resultados if resultados else []

    def comprobar_accion_en_usuario(self, id_usuario, id_accion):
        with GestorDB() as conexion:
            query = """
                SELECT a.id_accion, a.nombre_empresa, p.cantidad_acciones, a.precio_compra
                FROM portafolio p
                JOIN acciones a ON p.id_accion = a.id_accion
                WHERE p.id_usuario = %s AND p.id_accion = %s
            """
            return conexion.ejecutar_query(query, (id_usuario, id_accion))

    def actualizar_cantidad_acciones(self, id_usuario, id_accion, cantidad):
        with GestorDB() as conexion:
            query = """
                UPDATE portafolio
                SET cantidad_acciones = cantidad_acciones + %s
                WHERE id_usuario = %s AND id_accion = %s
            """
            conexion.ejecutar_query(query, (cantidad, id_usuario, id_accion))
            conexion.confirmar()