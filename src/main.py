from service.gestor_bd import GestorDB
from dao.usuario_dao import UsuarioDAO
from models.usuario import Usuario

def main():
    # Inicializa la conexión a la base de datos
    gestor_db = GestorDB()
    connection = gestor_db.connect()

    # Inicializa los DAOs con la conexión
    usuario_dao = UsuarioDAO(gestor_db)

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
                menu_usuario(usuario_dao, usuario)
            else:
                print("Credenciales incorrectas. Intente nuevamente.")
        elif opcion == '3':
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")


def menu_usuario(usuario_dao, usuario):
    while True:
        print("\nMENÚ USUARIO")
        print("1. Mostrar datos de la cuenta")
        print("2. Listar activos del portafolio")
        print("3. Comprar acciones")
        print("4. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            mostrar_datos_cuenta(usuario)
        elif opcion == '2':
            # listar_activos_portafolio(usuario_dao, usuario)
            pass
        elif opcion == '3':
            pass
        elif opcion == '4':
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
    nuevo_usuario = Usuario(nombre, apellido, cuil, email, contraseña)
    
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

# Solamente mostrar saldo, total invertido y rendimiento total
def mostrar_datos_cuenta(usuario):
    print("\n--- DATOS DE LA CUENTA ---")
    print(f"Saldo: {usuario.saldo}")
    print(f"Total Invertido: {usuario.total_invertido}")
    print(f"Rendimiento Total: {usuario.rendimiento_total}")

# Listar las acciones (activos) del portafolio: nombre de la empresa, cantidad de acciones, los valores de cotizacion y el rendimiento.
def listar_activos_portafolio(usuario_dao, usuario_id):
     activos = usuario_dao.listar_activos_portafolio(usuario_id)
     if activos:
         print("\nACTIVOS DEL PORTAFOLIO:")
         for activo in activos:
             print(f"Empresa: {activo['empresa']}, Cantidad: {activo['cantidad_acciones']}, "
                   f"Precio Compra Actual: {activo['precio_compra_actual']}, "
                 f"Precio Venta Actual: {activo['precio_venta_actual']}, "
                  f"Rendimiento: {activo['rendimiento']}")
     else:
        print("No se encontraron activos en el portafolio.")


if __name__ == "__main__":
    main()