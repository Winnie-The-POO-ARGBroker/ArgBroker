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


class TransaccionControlador:
    def __init__(self):
        self.cuenta_dao = CuentaDAO()
        self.accion_dao = AccionDAO()
        self.portafolio_dao = PortafolioDAO()

    def comprar_acciones(self, id_usuario):
        self.accion_dao.listar_acciones_disponibles()
        print()

        try:
            id_accion = int(input("Ingrese el ID de la acción que desea comprar: "))
            with GestorDB() as conexion:
                try:
                    conexion.iniciar_transaccion()
                
                    accion = self.accion_dao.comprobar_accion(id_accion)

                    if accion:
                        print(f"Precio compra: {accion[3]} - Precio venta: {accion[4]}")
                        print()
                        cantidad = int(input("Ingrese la cantidad de acciones que desea comprar: "))
                        
                        # Monto total con la comisión (1,5%)
                        precio_venta = accion[4]
                        monto_total = round((precio_venta * cantidad) * Decimal(1.015), 2)

                        saldo = self.accion_dao.obtener_saldo_usuario(id_usuario)

                        if saldo >= monto_total:
                            self.accion_dao.registrar_transaccion(
                                id_usuario, id_accion, cantidad, monto_total, Decimal(0.015) * monto_total, 1
                            )

                            self.accion_dao.actualizar_saldo(id_usuario, saldo - monto_total)

                            self.portafolio_dao.asignar_acciones(
                                id_usuario, id_accion, cantidad, precio_venta, accion[3]
                            )

                            conexion.confirmar()

                            print()
                            print(f"Compra exitosa: {cantidad} acciones de {accion[2]} por ${monto_total:.2f}.")
                        else:
                            print("Saldo insuficiente para realizar la compra.")
                    else:
                        print("La acción no existe. Por favor, ingrese un ID válido.")

                except Exception as e:
                    conexion.revertir()
                    print(f"Error en la transacción: {e}")

        except ValueError:
            print("Entrada inválida. Asegúrese de ingresar un número válido.")

        finally:
            conexion.cerrar_conexion()


    def vender_acciones(self, id_usuario):
        acciones_inversor = self.portafolio_dao.listar_acciones_del_usuario(id_usuario)

        if not acciones_inversor:
            print()
            print("=" * 116)
            print("=" * 38, "No tienes acciones en tu portafolio.", "=" * 37)
            print("=" * 116)
            print()
            return

        tabla = PrettyTable()
        tabla.field_names = ["ID", "Empresa", "Cantidad", "Precio venta"]
        tabla._min_table_width = 116

        for accion in acciones_inversor:
            tabla.add_row(accion)

        print(tabla)
        print()

        # Selección del ID de la acción a vender
        try:
            id_accion = int(input("\nIngrese el ID de la acción que desea vender: "))
            accion = self.portafolio_dao.comprobar_accion_en_usuario(id_usuario, id_accion)

            if accion:
                cantidad_disponible = accion[0][2]
                cantidad = int(input(f"Ingrese la cantidad a vender (disponible: {cantidad_disponible}): "))

                if cantidad <= cantidad_disponible:
                    precio_venta = accion[0][3] 
                    monto_total = (precio_venta * cantidad) * Decimal(0.985)  # 1,5% de comisión

                    # Registrar la transacción
                    self.accion_dao.registrar_transaccion(
                        id_usuario, id_accion, cantidad, monto_total, Decimal(0.015) * monto_total, 2
                    )

                    saldo_actual = self.accion_dao.obtener_saldo_usuario(id_usuario)
                    self.accion_dao.actualizar_saldo(id_usuario, saldo_actual + monto_total)

                    self.portafolio_dao.actualizar_cantidad_acciones(id_usuario, id_accion, -cantidad)

                    print()
                    print(f" Venta exitosa: {cantidad} acciones de {accion[0][1]} por ${monto_total:.2f}.")
                else:
                    print()
                    print("=" * 116)
                    print("=" * 35, "La cantidad solicitada supera la disponible.", "=" * 35)
                    print("=" * 116)
                    print()
            else:
                print()
                print("=" * 116)
                print("=" * 37, "La acción no existe en tu portafolio.", "=" * 37)
                print("=" * 116)
                print()
        except ValueError:
            print("Entrada inválida. Asegúrese de ingresar un número válido.")