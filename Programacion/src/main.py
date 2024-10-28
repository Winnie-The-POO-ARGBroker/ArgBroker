from controls.usuario_controlador import UsuarioControlador
from menus.cuenta_menu import cuenta_menu
from accesory.utils import mostrar

def main():
    usuario_controlador = UsuarioControlador()

    while True:
        mostrar("MENU PRINCIPAL")
        print()
        print("1. Registrar")
        print("2. Iniciar sesión")
        print("3. Salir")
        print()
        opcion = input("Seleccione una opción: ")
        print()

        if opcion == '1':
            usuario_controlador.registrar_nuevo_usuario()
        elif opcion == '2':
            usuario_logeo = usuario_controlador.iniciar_sesion()
            if usuario_logeo:
                cuenta_menu(usuario_logeo)

        elif opcion == '3':
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()