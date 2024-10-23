import mysql.connector
from mysql.connector import Error
from service.gestor_bd import GestorDB

class AccionDAO:
    def __init__(self, db_connect: GestorDB):
        self.db_connect = db_connect

    def comprar_acciones(self, usuario_id, simbolo, cantidad, precio_compra):
        connection = self.db_connect.connect()
        if connection is None:
            return

        try:
            cursor = connection.cursor()

            # Validación: Verificar si el usuario tiene suficiente saldo
            total_compra = cantidad * precio_compra
            usuario = self.obtener_usuario(usuario_id)  # Método para obtener el usuario por su ID
            if usuario.saldo < total_compra:
                print("No hay suficiente saldo para realizar la compra.")
                return

            # Registrar la transacción
            cursor.execute('''INSERT INTO transacciones (usuario_id, simbolo, cantidad, precio_compra, tipo) 
                            VALUES (%s, %s, %s, %s, 'compra')''', (usuario_id, simbolo, cantidad, precio_compra))
            
            # Actualizar acciones en el portafolio
            cursor.execute('''INSERT INTO acciones (usuario_id, simbolo, cantidad, nombre_empresa) 
                            VALUES (%s, %s, %s, (SELECT nombre_empresa FROM cotizaciones WHERE simbolo = %s))
                            ON DUPLICATE KEY UPDATE cantidad = cantidad + %s''', (usuario_id, simbolo, cantidad, simbolo, cantidad))

            # Actualizar saldo y total invertido
            comision = total_compra * 0.01  # Ejemplo: comisión del 1%
            cursor.execute('UPDATE usuarios SET saldo = saldo - %s, total_invertido = total_invertido + %s WHERE id = %s', 
                        (total_compra + comision, total_compra, usuario_id))
            
            connection.commit()
            print("Compra realizada con éxito.")
        except mysql.connector.Error as e:
            print(f"Error al comprar acciones: {e}")
        finally:
            cursor.close()


    def vender_acciones(self, usuario_id, simbolo, cantidad, precio_venta):
        connection = self.db_connect.connect()
        if connection is None:
            return

        try:
            cursor = connection.cursor()

            # Validación: Verificar si el usuario tiene suficientes acciones
            cursor.execute('SELECT cantidad FROM acciones WHERE usuario_id = %s AND simbolo = %s', (usuario_id, simbolo))
            resultado = cursor.fetchone()

            if resultado is None or resultado[0] < cantidad:
                print("No hay suficientes acciones para realizar la venta.")
                return

            # Registrar la transacción
            cursor.execute('''INSERT INTO transacciones (usuario_id, simbolo, cantidad, precio_venta, tipo) 
                            VALUES (%s, %s, %s, %s, 'venta')''', (usuario_id, simbolo, cantidad, precio_venta))

            # Actualizar acciones en el portafolio
            cursor.execute('UPDATE acciones SET cantidad = cantidad - %s WHERE usuario_id = %s AND simbolo = %s', 
                        (cantidad, usuario_id, simbolo))

            # Actualizar saldo y total invertido
            total_venta = cantidad * precio_venta
            comision = total_venta * 0.01  # Ejemplo: comisión del 1%
            cursor.execute('UPDATE usuarios SET saldo = saldo + %s - %s, total_invertido = total_invertido - %s WHERE id = %s', 
                        (total_venta, comision, total_venta, usuario_id))
            
            connection.commit()
            print("Venta realizada con éxito.")
        except mysql.connector.Error as e:
            print(f"Error al vender acciones: {e}")
        finally:
            cursor.close()

