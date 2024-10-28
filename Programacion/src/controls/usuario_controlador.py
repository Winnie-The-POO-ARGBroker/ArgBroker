from daos.usuario_dao import UsuarioDAO
from models.usuario import Usuario

class UsuarioControlador:

    def __init__(self):
        self.usuario_dao = UsuarioDAO()

    def solicitar_opcion(self, mensaje, opciones_validas):
        """Solicita una opción al usuario y valida que esté dentro de las opciones permitidas."""
        while True:
            try:
                opcion = int(input(mensaje))
                if opcion in opciones_validas:
                    return opcion
                else:
                    print(f"Por favor, ingrese un valor válido: {opciones_validas}.")
            except ValueError:
                print("Error: Debe ingresar un número.")

    def solicitar_documento(self, tipo_documento):
        """Solicita y valida el documento del usuario según el tipo de documento especificado."""
        tipos = {1: "CUIL", 2: "CUIT", 3: "Pasaporte"}
        while True:
            documento = input(f"Ingrese su {tipos[tipo_documento]}: ")
            if not Usuario.validar_documento(documento, tipo_documento):
                print("Documento inválido.")
            elif self.usuario_dao.verificar_existencia("documento", documento):
                print("Documento ya registrado.")
            else:
                return documento

    def solicitar_contrasena(self):
        """Solicita y valida la contraseña del usuario."""
        while True:
            contrasena = input("Ingrese la contraseña: ")
            if Usuario.validar_contrasena(contrasena):
                return contrasena
            else:
                print("Contraseña inválida.")

    def registrar_nuevo_usuario(self):
        """Registra un nuevo usuario solicitando sus datos y verificando su disponibilidad en el sistema."""
        while True:
            nombre_usuario = input("Ingrese nombre: ")
            if not self.usuario_dao.verificar_existencia("nombre_usuario", nombre_usuario):
                break
            print("Razón social ya registrada.")

        tipo_documento = self.solicitar_opcion("Seleccione el tipo de documento (1- CUIL, 2- CUIT, 3- Pasaporte): ", [1, 2, 3])
        documento = self.solicitar_documento(tipo_documento)

        while True:
            email = input("Ingrese el email: ")
            if Usuario.validar_email(email) and not self.usuario_dao.verificar_existencia("email", email):
                break
            print("Email inválido o ya registrado.")

        contrasena = self.solicitar_contrasena()

        nuevo_usuario = Usuario(
            documento=documento,
            email=email,
            nombre_usuario=nombre_usuario,
            id_tipo_documento=tipo_documento,
            contrasena=contrasena
        )

        return self.usuario_dao.insertar(nuevo_usuario)

    def iniciar_sesion(self):
        """Inicia sesión para un usuario dado su email y contraseña, con un límite de intentos."""
        email = input("Ingrese su email: ")
        usuario_datos = self.usuario_dao.obtener_uno(email)
        
        if usuario_datos:
            intentos = 3  # Intentos permitidos
            while intentos > 0:
                contrasena = input("Ingrese su contraseña: ")

                if usuario_datos[1] == contrasena:
                    print(f"Inicio de sesión exitoso.")
                    
                    usuario_objeto = Usuario(
                        documento=usuario_datos[2],           
                        email=usuario_datos[3],               
                        nombre_usuario=usuario_datos[4],     
                        id_tipo_documento=usuario_datos[5],   
                        contrasena=usuario_datos[1]          
                    )
                    return usuario_objeto  
                else:
                    intentos -= 1
                    if intentos > 0:
                        print(f"Contraseña incorrecta. Intentos restantes: {intentos}.")
                    else:
                        print("Ha superado el número máximo de intentos. Usuario bloqueado.")
                        return None  
        else:
            print("Email no registrado.")
            return None
