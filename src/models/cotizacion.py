class Cotizacion:
    def __init__(self, simbolo, precio_actual, precio_compra, precio_venta):
        self._simbolo = simbolo
        self._precio_actual = precio_actual
        self._precio_compra = precio_compra
        self._precio_venta = precio_venta

    @property
    def simbolo(self):
        return self._simbolo

    @property
    def precio_actual(self):
        return self._precio_actual

    @property
    def precio_compra(self):
        return self._precio_compra

    @property
    def precio_venta(self):
        return self._precio_venta

    def actualizar_precio(self, nuevo_precio_actual):
        self._precio_actual = nuevo_precio_actual
