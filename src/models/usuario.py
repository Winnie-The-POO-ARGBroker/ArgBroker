from datetime import datetime


class Usuario:
    def __init__(self, id, nombre, apellido, cuil, email, contraseña, saldo=1000000.00, total_invertido=0.00, rendimiento_total=0.00):
        self._id = id
        self._nombre = nombre
        self._apellido = apellido
        self._cuil = cuil
        self._email = email
        self._contraseña = contraseña  # Asegúrate de que este atributo está definido
        self._fecha_registro = datetime.now()  # Esto lo puedes mantener si deseas manejar la fecha aquí
        self._saldo = saldo
        self._total_invertido = total_invertido
        self._rendimiento_total = rendimiento_total


    # Métodos que exponen sólo lo necesario
    @property
    def id(self):
        return self._id

    @property
    def nombre(self):
        return self._nombre

    @property
    def apellido(self):
        return self._apellido

    @property
    def cuil(self):
        return self._cuil

    @property
    def email(self):
        return self._email

    @property
    def contraseña(self):
        return self._contraseña

    @property
    def feecha_registro(self):
        return self._fecha_registro

    @property
    def saldo(self):
        return self._saldo

    @saldo.setter
    def saldo(self, nuevo_saldo):
        if nuevo_saldo >= 0:
            self._saldo = nuevo_saldo
        else:
            raise ValueError("El saldo no puede ser negativo.")

    @property
    def total_invertido(self):
        return self._total_invertido

    @total_invertido.setter
    def total_invertido(self, monto):
        if monto >= 0:
            self._total_invertido += monto
        else:
            raise ValueError("El monto invertido no puede ser negativo.")

    @property
    def rendimiento_total(self):
        return self._rendimiento_total

    @rendimiento_total.setter
    def rendimiento_total(self, rendimiento):
        self._rendimiento_total += rendimiento

    # Métodos con alta cohesión y bajo acoplamiento (Modularidad y Bajo Acoplamiento)
    def actualizar_inversion(self, monto, tipo_transaccion):
        if tipo_transaccion == "compra":
            self.total_invertido = monto
        elif tipo_transaccion == "venta":
            self.total_invertido = -monto

    def actualizar_rendimiento(self, rendimiento):
        self.rendimiento_total = rendimiento

    def mostrar_datos(self):
        # Este método abstrae la lógica interna (Abstracción)
        return f"Usuario: {self.nombre} {self.apellido}, CUIL: {self.cuil}, Email: {self.email}\n" \
               f"Saldo: {self.saldo}, Total Invertido: {self.total_invertido}, Rendimiento Total: {self.rendimiento_total}"
