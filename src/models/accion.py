class Accion:
    def __init__(self, usuario_id, simbolo, nombre_empresa, cantidad, precio_compra):
        self._usuario_id = usuario_id
        self._simbolo = simbolo
        self._nombre_empresa = nombre_empresa
        self._cantidad = cantidad
        self._precio_compra = precio_compra

    @property
    def usuario_id(self):
        return self._usuario_id

    @property
    def simbolo(self):
        return self._simbolo

    @property
    def nombre_empresa(self):
        return self._nombre_empresa

    @property
    def cantidad(self):
        return self._cantidad

    @property
    def precio_compra(self):
        return self._precio_compra

    def calcular_valor_total(self):
        return self._cantidad * self._precio_compra
