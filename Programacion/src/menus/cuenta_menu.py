from controls.cuenta_controlador import CuentaControlador
from controls.transaccion_controlador import TransaccionControlador
from daos.usuario_dao import UsuarioDAO
from menus.transacciones_menu import transacciones_menu
from accesory.utils import mostrar


def cuenta_menu(usuario):
    try:
        
        cuenta_controlador = CuentaControlador()
        usuario_dao = UsuarioDAO()
        transaccion_controlador = TransaccionControlador()

        usuario_info = usuario_dao.obtener_uno(usuario.email)
        if not usuario_info:
            raise Exception("No se pudo obtener la información del usuario")

        id_usuario = usuario_info[0]
        while True:
            mostrar(f" BIENVENIDO {usuario.nombre_usuario}")
            print()
            print("1. Mostrar datos del usuario")
            print("2. Listar activos del portafolio")
            print("3. Realizar transacciones")
            print("4. Cerrar sesión")
            print()
            opcion = input("Seleccione una opcion: ")
            print()

            if opcion == "1":
                cuenta_controlador.mostrar_datos_cuenta(id_usuario)
            elif opcion == "2":
                cuenta_controlador.mostrar_portafolio(id_usuario)
            elif opcion == "3":
                transacciones_menu(transaccion_controlador, usuario, id_usuario)
            elif opcion == "4":
                break
            else:
                print("Opción no válida")
    except Exception as e:
        print(f"Error durante la ejecución: {e}")

