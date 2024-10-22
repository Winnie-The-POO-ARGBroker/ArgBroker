from service.gestor_bd import GestorDB
from dao.usuario_dao import UsuarioDAO
from models.usuario import Usuario

def main():
    # Inicializa la conexión a la base de datos
    gestor_db = GestorDB()
    conexion = gestor_db.connect()  # Método para establecer la conexión

    # Inicializa los DAOs con la conexión
    usuario_dao = UsuarioDAO()

    while True:
        print("\nMENÚ PRINCIPAL")
        print("1. Registrar")
        print("2. Iniciar sesión")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            registrar_usuario(usuario_dao)
        elif opcion == '2':
            iniciar_sesion(usuario_dao)
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
            pass
        elif opcion == '2':
            pass
        elif opcion == '3':
            pass
        elif opcion == '4':
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")


def registrar_usuario(usuario_dao):
    # Solicita los datos del usuario
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
        print(f"Ingreso exitoso. Bienvenido, {usuario.nombre}!")
        menu_usuario(usuario_dao, usuario)  # Llama al menú del usuario
    else:
        print("Email o contraseña incorrectos.")


if __name__ == "__main__":
    main()