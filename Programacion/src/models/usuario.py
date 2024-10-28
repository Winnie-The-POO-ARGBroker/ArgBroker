import re

class Usuario:
    def __init__(self, contrasena, documento, email, nombre_usuario, id_tipo_documento):
        self._contrasena = contrasena
        self._documento = documento
        self._email = email
        self._nombre_usuario = nombre_usuario
        self._id_tipo_documento = id_tipo_documento
        self._contrasena = contrasena  

    @property
    def documento(self):
        return self._documento
    
    @property
    def email(self):
        return self._email

    @property
    def nombre_usuario(self):
        return self._nombre_usuario

    @property
    def id_tipo_documento(self):
        return self._id_tipo_documento

    @property
    def contrasena(self):
        return self._contrasena

    # Método para verificar la contraseña
    def verificar_contrasena(self, contrasena):
        return self._contrasena == contrasena
    
    def incrementar_intentos_fallidos(self):
        self._intentos_fallidos += 1

    def resetear_intentos_fallidos(self):
        self._intentos_fallidos = 0

    def esta_bloqueado(self):
        return self._intentos_fallidos >= 3
    
    def validar_email(email):
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(patron, email) is not None
    
    def validar_documento(documento, tipo_documento):
        longitudes = {1: 11, 2: 11, 3: 9}  # CUIL/CUIT: 11 dígitos, Pasaporte: 9 dígitos
        return documento.isdigit() and len(documento) == longitudes.get(tipo_documento, 0)

    def validar_contrasena(contrasena):
        # Verifica que la contraseña tenga al menos 4 caracteres, 
        # contenga al menos un número y al menos una letra
        if (len(contrasena) < 4 or
            not re.search(r"[A-Za-z]", contrasena) or  # Al menos una letra
            not re.search(r"[0-9]", contrasena)):  # Al menos un número
            return False
        return True

    def mostrar_info(self):
        return {
            "Usuario": self.nombre_usuario,
            "Documento": self._documento,
            "Email": self._email,
            "Tipo de Documento": self._id_tipo_documento,
        }