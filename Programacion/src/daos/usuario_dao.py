import random
import string
from service.gestor_bd import GestorDB
from models.usuario import Usuario
from models.metodos_abc import MetodosAbstractos

class UsuarioDAO(MetodosAbstractos):

    def generar_numero_cuenta(self):
        """Genera un número de cuenta aleatorio que no se repita en la base de datos."""
        while True:
            numero_cuenta = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
            query = "SELECT COUNT(*) FROM cuentas WHERE numero_cuenta = %s"
            
            with GestorDB() as conexion_db:
                resultado = conexion_db.ejecutar_query(query, (numero_cuenta,))
                if resultado is False:
                    return None
                
                count = resultado[0][0]
                if count == 0:
                    return numero_cuenta

    def verificar_existencia(self, campo, valor):
        """Verifica si existe un registro según el campo y valor proporcionado."""
        with GestorDB() as conexion:
            query = f"SELECT COUNT(*) FROM usuarios WHERE {campo} = %s"
            resultado = conexion.ejecutar_query(query, (valor,))
            return resultado and resultado[0][0] > 0

    def insertar(self, usuario: Usuario):
        """Registra un nuevo usuario y su cuenta asociada."""
        try:
            with GestorDB() as conexion_db:
                query_usuario = """
                    INSERT INTO usuarios (documento, email, nombre_usuario, contrasena, 
                                          id_tipo_documento)
                    VALUES (%s, %s, %s, %s, %s)
                """
                valores_usuario = (
                    usuario.documento, 
                    usuario.email,
                    usuario.nombre_usuario, 
                    usuario.contrasena, 
                    usuario.id_tipo_documento
                )
                if not conexion_db.ejecutar_query(query_usuario, valores_usuario):
                    raise Exception("Error al ejecutar la inserción del usuario.")
                
                conexion_db.confirmar()
                
                numero_cuenta = self.generar_numero_cuenta()

                if numero_cuenta is None:
                    raise Exception("Error al generar un número de cuenta único.")

                id_usuario = conexion_db.ejecutar_query("SELECT LAST_INSERT_ID()")

                if id_usuario:
                    id_usuario = id_usuario[0][0] 
                else:
                    raise Exception("No se pudo obtener el ID del usuario creado.")

                query_cuenta = """
                INSERT INTO cuentas (numero_cuenta, saldo, id_usuario) 
                VALUES (%s, %s, %s)
                """

                valores_cuenta = (numero_cuenta, 1000000.00, id_usuario)

                if not conexion_db.ejecutar_query(query_cuenta, valores_cuenta):
                    raise Exception("Error al insertar la cuenta.")
        
        except Exception as e:
            print(f"Error al registrar el usuario y su cuenta: {e}")
    
    def obtener_uno(self, email):
        """Obtiene la información de un usuario a partir del email."""
        with GestorDB() as conexion:
            query = "SELECT * FROM usuarios WHERE email = %s"
            resultado = conexion.ejecutar_query(query, (email,))
            return resultado[0] if resultado else None
