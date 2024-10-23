class Transaccion:
    def __init__(self, usuario_id, simbolo, cantidad, monto, tipo):
        self._usuario_id = usuario_id
        self._simbolo = simbolo
        self._cantidad = cantidad
        self._monto = monto
        self._tipo = tipo  # 'compra' o 'venta'

        self.validar_transaccion()

    @property
    def usuario_id(self):
        return self._usuario_id

    @property
    def simbolo(self):
        return self._simbolo

    @property
    def cantidad(self):
        return self._cantidad

    @property
    def monto(self):
        return self._monto

    @property
    def tipo(self):
        return self._tipo

    def validar_transaccion(self):
        if self._cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")
        if self._tipo not in ["compra", "venta"]:
            raise ValueError("El tipo de transacción debe ser 'compra' o 'venta'.")
