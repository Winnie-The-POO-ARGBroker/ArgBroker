from accesory.utils import mostrar

def transacciones_menu(transaccion_controlador, usuario, id_usuario):
    while True:
        mostrar("TRANSACCIONES")

        print()
        print("1. Comprar acciones")
        print("2. Vender acciones")
        print("3. Volver al menú principal")
        print()

        opcion = input("Seleccione una opción: ")
        print()

        if opcion == "1":
            transaccion_controlador.comprar_acciones(id_usuario)
        elif opcion == "2":
            transaccion_controlador.vender_acciones(id_usuario)
        elif opcion == "3":
            print("Volviendo al menú principal...")
            break
        else:
            print("Opción no válida.")