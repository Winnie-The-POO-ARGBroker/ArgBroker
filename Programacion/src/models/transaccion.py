class Transaccion:
    def __init__(self, id_transaccion, cantidad_acciones, monto_total, comision, fecha_hora, numero_cuenta, id_tipo_transaccion, id_accion, simbolo=None):
        self._id_transaccion = id_transaccion
        self._cantidad_acciones = cantidad_acciones
        self._monto_total = monto_total
        self._comision = comision
        self._fecha_hora = fecha_hora
        self._numero_cuenta = numero_cuenta
        self._id_tipo_transaccion = id_tipo_transaccion
        self._id_accion = id_accion
        self._simbolo = simbolo

    @property
    def id_transaccion(self):
        return self._id_transaccion

    @id_transaccion.setter
    def id_transaccion(self, value):
        self._id_transaccion = value

    @property
    def id_accion(self):
        return self._id_accion

    @id_accion.setter
    def id_accion(self, value):
        self._id_accion = value

    @property
    def simbolo(self):
        return self._simbolo

    @simbolo.setter
    def simbolo(self, value):
        self._simbolo = value

    @property
    def numero_cuenta(self):
        return self._numero_cuenta

    @numero_cuenta.setter
    def numero_cuenta(self, value):
        self._numero_cuenta = value

    @property
    def monto_total(self):
        return self._monto_total

    @monto_total.setter
    def monto_total(self, value):
        self._monto_total = value

    @property
    def comision(self):
        return self._comision

    @comision.setter
    def comision(self, value):
        self._comision = value

    @property
    def cantidad_acciones(self):
        return self._cantidad_acciones

    @cantidad_acciones.setter
    def cantidad_acciones(self, value):
        self._cantidad_acciones = value

    @property
    def fecha_hora(self):
        return self._fecha_hora

    @fecha_hora.setter
    def fecha_hora(self, value):
        self._fecha_hora = value

    @property
    def tipo(self):
        return self._id_tipo_transaccion  # Agregar propiedad para el tipo

    @property
    def id_tipo_transaccion(self):
        return self._id_tipo_transaccion

    @id_tipo_transaccion.setter
    def id_tipo_transaccion(self, value):
        self._id_tipo_transaccion = value  # Corregido

    # Método para mostrar información de la transacción en formato de cadena
    def __str__(self):
        return (f"ID Transacción: {self._id_transaccion}, Acción: {self._simbolo} ({self._id_accion}), "
                f"Cuenta: {self._numero_cuenta}, Monto Total: {self._monto_total}, "
                f"Comisión: {self._comision}, Cantidad: {self._cantidad_acciones}, "
                f"Fecha y Hora: {self._fecha_hora}, Tipo: {self.tipo}")

    def __repr__(self):
        return (f"Transaccion(id_transaccion={self._id_transaccion}, cantidad_acciones={self._cantidad_acciones}, "
                f"monto_total={self._monto_total}, comision={self._comision}, fecha_hora={self._fecha_hora}, "
                f"numero_cuenta={self._numero_cuenta}, id_tipo_transaccion={self._id_tipo_transaccion}, "
                f"id_accion={self._id_accion}, simbolo={self._simbolo})")
