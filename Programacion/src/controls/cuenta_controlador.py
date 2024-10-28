from datetime import datetime
from daos.cuenta_dao import CuentaDAO
from models.cuenta import Cuenta
from daos.accion_dao import AccionDAO
from daos.portafolio_dao import PortafolioDAO
from decimal import Decimal
from service.gestor_bd import GestorDB
import random
from prettytable import PrettyTable
from accesory.utils import mostrar


class CuentaControlador:
    def __init__(self):
        self.cuenta_dao = CuentaDAO()
        self.accion_dao = AccionDAO()
        self.portafolio_dao = PortafolioDAO()


    def mostrar_datos_cuenta(self, id_usuario):
        rendimiento_acumulado = 0
        total_invertido = 0

        datos = self.cuenta_dao.obtener_datos_cuenta(id_usuario)
        if datos:
            cuenta = Cuenta(id_usuario, *datos)
            transacciones = self.cuenta_dao.obtener_transacciones_por_cuenta(id_usuario)

            if transacciones:
                # Total invertido
                total_invertido = (
                    sum(t.monto_total for t in transacciones if t.id_tipo_transaccion == 1) -
                    sum(t.monto_total for t in transacciones if t.id_tipo_transaccion == 2)
                )
                
                accion_dao = AccionDAO()
                portafolio_dao = PortafolioDAO()

                # Rendimiento acumulado
                for t in transacciones:
                    id_accion = t.id_accion
                    datos_accion = accion_dao.comprobar_accion(id_accion)
                    accion_usuario = portafolio_dao.comprobar_accion_en_usuario(id_usuario, id_accion)

                    if datos_accion and accion_usuario:
                        cantidad = accion_usuario[0][2]
                        precio_compra = datos_accion[3]  # Precio de compra original
                        precio_venta = datos_accion[4]   # Precio de venta actual

                        # Generar precios aleatorios
                        nuevo_precio_compra = round(precio_compra * Decimal(random.uniform(0.9, 1.1)), 2)
                        nuevo_precio_venta = round(precio_venta * Decimal(random.uniform(0.9, 1.1)), 2)

                        rendimiento = round((nuevo_precio_venta - nuevo_precio_compra) * cantidad, 2)
                        rendimiento_acumulado += rendimiento

            mostrar("DATOS DE LA CUENTA")

            # Crear tabla
            tabla = PrettyTable()
            tabla.field_names = ["Descripción", "Informacion"]
            tabla._min_table_width = 116
            tabla.add_row(["Nro de Cuenta", cuenta.numero_cuenta])
            tabla.add_row(["Saldo Disponible", f"${cuenta.saldo:.2f}"])
            tabla.add_row(["Total Invertido", f"${total_invertido:.2f}"])
            tabla.add_row(["Rendimiento Acumulado", f"${rendimiento_acumulado:.2f}"])

            print(tabla)

        else:
            print("Cuenta no encontrada")


    def mostrar_portafolio(self, id_usuario):
        """Genera precios aleatorios y muestra los activos del usuario."""
        activos = self.portafolio_dao.listar_acciones_del_usuario(id_usuario)

        if not activos:
            print("No tienes activos en tu portafolio.")
            return

        tabla = PrettyTable()
        tabla.field_names = ["ID", "Empresa", "Cantidad", "Precio compra actual", "Precio venta actual", "Rendimiento"]
        tabla._min_table_width = 116

        for activo in activos:
            id_accion = activo[0]
            nombre_empresa = activo[1]
            cantidad = int(activo[2])
            precio_compra = Decimal(activo[3])

            # Generar precios aleatorios
            nuevo_precio_compra = round(precio_compra * Decimal(random.uniform(0.9, 1.1)), 2)
            nuevo_precio_venta = round(precio_compra * Decimal(random.uniform(0.9, 1.1)), 2)

            rendimiento = round((nuevo_precio_venta - precio_compra) * cantidad, 2)

            signo = "+" if rendimiento >= 0 else ""
            tabla.add_row([id_accion, nombre_empresa, cantidad, f"${nuevo_precio_compra}", f"${nuevo_precio_venta}", f"{signo}${rendimiento}"])
           
        mostrar("ACTIVOS EN TU PORTAFOLIO")

        print()
        print(tabla)
