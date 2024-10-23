from service.gestor_bd import GestorDB
from dao.usuario_dao import UsuarioDAO
from models.usuario import Usuario
from datetime import datetime
from dao.accion_dao import AccionDAO
from dao.cotizacion_dao import CotizacionDAO

def main():
    # Inicializa la conexión a la base de datos
    gestor_db = GestorDB()
    connection = gestor_db.connect()

    # Inicializa los DAOs con la conexión
    usuario_dao = UsuarioDAO(gestor_db)
    accion_dao = AccionDAO(gestor_db)
    cotizacion_dao = CotizacionDAO(gestor_db)

    while True:
        print("\nMENÚ PRINCIPAL")
        print("1. Registrar")
        print("2. Iniciar sesión")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            registrar_usuario(usuario_dao)
        elif opcion == '2':
            usuario = iniciar_sesion(usuario_dao)
            if usuario:
                menu_usuario(usuario_dao, accion_dao, cotizacion_dao, usuario)
            else:
                print("Credenciales incorrectas. Intente nuevamente.")
        elif opcion == '3':
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

    gestor_db.close()

def menu_usuario(usuario_dao, accion_dao, cotizacion_dao, usuario):
    while True:
        print("\nMENÚ USUARIO")
        print("1. Mostrar datos de la cuenta")
        print("2. Listar activos del portafolio")
        print("3. Comprar acciones")
        print("4. Vender acciones")  # Opción para vender acciones
        print("5. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            mostrar_datos_cuenta(usuario)
        elif opcion == '2':
            listar_activos_portafolio(usuario_dao, usuario.id)  # Cambiar _id a id
        elif opcion == '3':
            comprar_acciones(usuario_dao, accion_dao, cotizacion_dao, usuario.id)  # Cambiar _id a id
        elif opcion == '4':
            vender_acciones(usuario_dao, accion_dao, cotizacion_dao, usuario.id)  # Cambiar _id a id
        elif opcion == '5':
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

def registrar_usuario(usuario_dao):
    nombre = input("Ingrese su nombre: ")
    apellido = input("Ingrese su apellido: ")
    cuil = input("Ingrese su CUIL: ")
    email = input("Ingrese su email: ")
    contraseña = input("Ingrese su contraseña: ")

    # Crea una instancia de Usuario
    nuevo_usuario = Usuario(None, nombre, apellido, cuil, email, contraseña)

    # Llama al método para registrar el usuario
    usuario_dao.registrar_nuevo_usuario(nuevo_usuario)

def iniciar_sesion(usuario_dao):
    email = input("Ingrese su email: ")
    contraseña = input("Ingrese su contraseña: ")
    
    usuario = usuario_dao.iniciar_sesion_usuario(email, contraseña)
    
    if usuario:
        return usuario
    else:
        print("Email o contraseña incorrectos.")

# Mostrar saldo, total invertido y rendimiento total
def mostrar_datos_cuenta(usuario):
    print("\n--- DATOS DE LA CUENTA ---")
    print(f"Saldo: {usuario.saldo}")
    print(f"Total Invertido: {usuario.total_invertido}")
    print(f"Rendimiento Total: {usuario.rendimiento_total}")

# Listar acciones (activos) del portafolio
def listar_activos_portafolio(usuario_dao, usuario_id):
    activos = usuario_dao.listar_activos_portafolio_usuario(usuario_id)
    if activos:
        print("\nACTIVOS DEL PORTAFOLIO:")
        for activo in activos:
            print(f"Empresa: {activo['empresa']}, Cantidad: {activo['cantidad_acciones']}, "
                  f"Precio Compra Actual: {activo['precio_compra_actual']}, "
                  f"Precio Venta Actual: {activo['precio_venta_actual']}, "
                  f"Rendimiento: {activo['rendimiento']}")
    else:
        print("No se encontraron activos en el portafolio.")

def comprar_acciones(usuario_dao, accion_dao, cotizacion_dao, usuario_id):
    simbolo = input("Ingrese el símbolo de la acción: ")
    cantidad = int(input("Ingrese la cantidad de acciones a comprar: "))
    
    # Obtener el precio de compra de la cotización
    precio_compra = cotizacion_dao.obtener_precio_cotizacion(simbolo)
    
    if precio_compra is None:
        print("No se encontró la cotización para el símbolo proporcionado.")
        return  # Salir del método si no hay cotización
    
    # Proceder con la compra si se encontró el precio
    accion_dao.comprar_acciones(usuario_id, simbolo, cantidad, precio_compra)

def vender_acciones(usuario_dao, accion_dao, cotizacion_dao, usuario_id):
    simbolo = input("Ingrese el símbolo de la acción: ")
    cantidad = int(input("Ingrese la cantidad de acciones a vender: "))
    
    # Obtener el precio de venta de la cotización
    precio_venta = cotizacion_dao.obtener_precio_cotizacion(simbolo)

    if precio_venta is None:
        print("No se pudo obtener el precio de venta. La acción no se venderá.")
        return

    # Proceder con la venta
    accion_dao.vender_acciones(usuario_id, simbolo, cantidad, precio_venta)

if __name__ == "__main__":
    main()
