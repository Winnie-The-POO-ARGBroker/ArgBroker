import mysql.connector
from mysql.connector import Error
from service.gestor_bd import GestorDB
from models.usuario import Usuario

class UsuarioDAO:
    def __init__(self):
        self.gestor_db = GestorDB()
        self.connection = self.gestor_db.connect()

    def registrar_nuevo_usuario(self, usuario):
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
            INSERT INTO usuarios (nombre, apellido, cuil, email, contraseña, saldo, total_invertido, rendimiento_total)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', (usuario.nombre, usuario.apellido, usuario.cuil, usuario.email, usuario.contraseña, 1000000, 0.00, 0.00))
            self.connection.commit()
            print("Registro exitoso.")
        except mysql.connector.Error as e:
            print(f"Error al registrar usuario: {e}")
        finally:
            cursor.close()


    def iniciar_sesion_usuario(self, email, contraseña):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE email = %s AND contraseña = %s', (email, contraseña))
        usuario = cursor.fetchone()
        cursor.close()
        if usuario:
            return Usuario(*usuario)  # Ahora coincide con el número de columnas
        else:
            return None


    def calcular_total_invertido_usuario(self, usuario_id):
        cursor = self.connection.cursor()
        cursor.execute('SELECT SUM(monto) FROM transacciones WHERE usuario_id = %s AND tipo = "compra"', (usuario_id,))
        total_invertido = cursor.fetchone()[0] or 0
        cursor.close()
        return total_invertido


    def calcular_rendimiento_total_usuario(self, usuario_id):
        cursor = self.connection.cursor()
        cursor.execute('''
        SELECT SUM(a.cantidad * c.precio_actual) - SUM(t.monto) 
        FROM acciones a
        JOIN cotizaciones c ON a.simbolo = c.simbolo
        JOIN transacciones t ON a.transaccion_id = t.id
        WHERE t.usuario_id = %s
        ''', (usuario_id,))
        rendimiento_total = cursor.fetchone()[0] or 0
        cursor.close()
        return rendimiento_total

    # ACTUALIZAR DESPUÉS DE COMPAR/VENDER ACCIONES
    def actualizar_total_invertido_usuario(self, usuario_id, monto, tipo_transaccion):
        try:
            cursor = self.connection.cursor()
            if tipo_transaccion == "compra":
                cursor.execute('''
                UPDATE usuarios
                SET total_invertido = total_invertido + %s
                WHERE id = %s
                ''', (monto, usuario_id))
            elif tipo_transaccion == "venta":
                cursor.execute('''
                UPDATE usuarios
                SET total_invertido = total_invertido - %s
                WHERE id = %s
                ''', (monto, usuario_id))
            self.connection.commit()
            print("Total invertido actualizado.")
        except mysql.connector.Error as e:
            print(f"Error al actualizar total invertido: {e}")
        finally:
            cursor.close()


    def actualizar_rendimiento_total_usuario(self, usuario_id, rendimiento):
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
            UPDATE usuarios
            SET rendimiento_total = rendimiento_total + %s
            WHERE id = %s
            ''', (rendimiento, usuario_id))
            self.connection.commit()
            print("Rendimiento total actualizado.")
        except mysql.connector.Error as e:
            print(f"Error al actualizar rendimiento total: {e}")
        finally:
            cursor.close()
