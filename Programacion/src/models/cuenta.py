class Cuenta:
    def __init__(self, id_cuenta, numero_cuenta, saldo):
        self._id_cuenta = id_cuenta
        self._numero_cuenta = numero_cuenta
        self._saldo = saldo

    @property
    def id_cuenta(self):
        return self._id_cuenta

    @id_cuenta.setter
    def id_cuenta(self, value):
        self._id_cuenta = value

    @property
    def numero_cuenta(self):
        return self._numero_cuenta

    @numero_cuenta.setter
    def numero_cuenta(self, value):
        self._numero_cuenta = value

    @property
    def saldo(self):
        return self._saldo

    @saldo.setter
    def saldo(self, value):
        self._saldo = value

    def actualizar_saldo(self, nuevo_saldo):
        self.saldo = nuevo_saldo

    def __str__(self):
        return f"ID Cuenta: {self._id_cuenta}, Número de Cuenta: {self._numero_cuenta}, Saldo: {self._saldo}"
