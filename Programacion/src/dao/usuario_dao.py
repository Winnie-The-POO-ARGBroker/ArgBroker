import mysql.connector
from mysql.connector import Error
from service.gestor_bd import GestorDB
from models.usuario import Usuario

class UsuarioDAO:
    def __init__(self, db_connect: GestorDB):
        self.db_connect = db_connect  # Guardar la instancia de GestorDB

    def registrar_nuevo_usuario(self, usuario):
        connection = self.db_connect.connect()
        if connection is None:
            return

        try:
            cursor = connection.cursor()
            cursor.execute(''' 
            INSERT INTO usuarios (nombre, apellido, cuil, email, contraseña, saldo, total_invertido, rendimiento_total) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) 
            ''', (usuario.nombre, usuario.apellido, usuario.cuil, usuario.email, usuario.contraseña, 1000000, 0.00, 0.00))
            connection.commit()
            print("Registro exitoso.")
        except mysql.connector.Error as e:
            print(f"Error al registrar usuario: {e}")
        finally:
            cursor.close()

    def iniciar_sesion_usuario(self, email, contraseña):
        connection = self.db_connect.connect()
        if connection is None:
            return None

        try:
            cursor = connection.cursor()
            cursor.execute('SELECT id, nombre, apellido, cuil, email, contraseña, saldo, total_invertido, rendimiento_total FROM usuarios WHERE email = %s AND contraseña = %s', (email, contraseña))
            usuario = cursor.fetchone()
            if usuario:
                return Usuario(*usuario)  # Asegúrate de que los campos coincidan con el constructor
            else:
                return None
        except mysql.connector.Error as e:
            print(f"Error al iniciar sesión: {e}")
            return None
        finally:
            cursor.close()

    def calcular_total_invertido_usuario(self, usuario_id):
        connection = self.db_connect.connect()
        if connection is None:
            return 0

        try:
            cursor = connection.cursor()
            cursor.execute('SELECT SUM(monto) FROM transacciones WHERE usuario_id = %s AND tipo = "compra"', (usuario_id,))
            total_invertido = cursor.fetchone()[0] or 0
            return total_invertido
        except mysql.connector.Error as e:
            print(f"Error al calcular total invertido: {e}")
            return 0
        finally:
            cursor.close()

    def calcular_rendimiento_total_usuario(self, usuario_id):
        connection = self.db_connect.connect()
        if connection is None:
            return 0

        try:
            cursor = connection.cursor()
            cursor.execute('''SELECT SUM(a.cantidad * c.precio_venta) - SUM(t.cantidad * t.precio_compra) 
                              FROM acciones a
                              JOIN cotizaciones c ON a.simbolo = c.simbolo
                              JOIN transacciones t ON a.simbolo = t.simbolo AND a.usuario_id = t.usuario_id
                              WHERE a.usuario_id = %s
                           ''', (usuario_id,))
            rendimiento_total = cursor.fetchone()[0] or 0
            return rendimiento_total
        except mysql.connector.Error as e:
            print(f"Error al calcular rendimiento total: {e}")
            return 0
        finally:
            cursor.close()

    def actualizar_total_invertido_usuario(self, usuario_id, monto, tipo_transaccion):
        connection = self.db_connect.connect()
        if connection is None:
            return

        try:
            cursor = connection.cursor()
            if tipo_transaccion == "compra":
                cursor.execute('''UPDATE usuarios
                                  SET total_invertido = total_invertido + %s
                                  WHERE id = %s
                                  ''', (monto, usuario_id))
            elif tipo_transaccion == "venta":
                cursor.execute('''UPDATE usuarios
                                  SET total_invertido = total_invertido - %s
                                  WHERE id = %s
                                  ''', (monto, usuario_id))
            connection.commit()
            print("Total invertido actualizado.")
        except mysql.connector.Error as e:
            print(f"Error al actualizar total invertido: {e}")
        finally:
            cursor.close()

    def actualizar_rendimiento_total_usuario(self, usuario_id, rendimiento):
        connection = self.db_connect.connect()
        if connection is None:
            return

        try:
            cursor = connection.cursor()
            cursor.execute('''UPDATE usuarios
                              SET rendimiento_total = rendimiento_total + %s
                              WHERE id = %s
                              ''', (rendimiento, usuario_id))
            connection.commit()
            print("Rendimiento total actualizado.")
        except mysql.connector.Error as e:
            print(f"Error al actualizar rendimiento total: {e}")
        finally:
            cursor.close()

    def listar_activos_portafolio_usuario(self, usuario_id):
        connection = self.db_connect.connect()
        if connection is None:
            return []

        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute('''SELECT 
                                a.nombre_empresa AS empresa, 
                                a.cantidad AS cantidad_acciones, 
                                c.precio_compra AS precio_compra_actual, 
                                c.precio_venta AS precio_venta_actual, 
                                ((c.precio_venta - t.precio_compra) * a.cantidad) AS rendimiento
                            FROM 
                                acciones a
                            JOIN 
                                cotizaciones c ON a.simbolo = c.simbolo
                            JOIN 
                                transacciones t ON a.simbolo = t.simbolo AND a.usuario_id = t.usuario_id
                            WHERE 
                                a.usuario_id = %s
                            ''', (usuario_id,))
            
            activos = cursor.fetchall()  # Devuelve todos los registros de activos del usuario
            rendimiento_total = sum(activo['rendimiento'] for activo in activos)
            
            # Actualizar el rendimiento total en la tabla de usuarios
            cursor.execute('UPDATE usuarios SET rendimiento_total = %s WHERE id = %s', (rendimiento_total, usuario_id))
            connection.commit()

            return activos
            
        except mysql.connector.Error as e:
            print(f"Error al listar activos del portafolio: {e}")
            return []
            
        finally:
            cursor.close()

