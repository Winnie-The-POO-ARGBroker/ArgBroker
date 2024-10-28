class Accion:
    def __init__(self, id_accion, simbolo, nombre_empresa, precio_compra, precio_venta):
        self._id_accion = id_accion
        self._simbolo = simbolo
        self._nombre_empresa = nombre_empresa
        self._precio_compra = precio_compra
        self._precio_venta = precio_venta

    @property
    def id_accion(self):
        return self._id_accion

    @id_accion.setter
    def id_accion(self, id_accion):
        self._id_accion = id_accion

    @property
    def simbolo(self):
        return self._simbolo

    @simbolo.setter
    def simbolo(self, simbolo):
        self._simbolo = simbolo

    @property
    def nombre_empresa(self):
        return self._nombre_empresa

    @nombre_empresa.setter
    def nombre_empresa(self, nombre_empresa):
        self._nombre_empresa = nombre_empresa

    @property
    def precio_compra(self):
        return self._precio_compra

    @precio_compra.setter
    def precio_compra(self, precio_compra):
        self._precio_compra = precio_compra

    @property
    def precio_venta(self):
        return self._precio_venta

    @precio_venta.setter
    def precio_venta(self, precio_venta):
        self._precio_venta = precio_venta

    def actualizar_simbolo(self, nuevo_simbolo):
        self.simbolo = nuevo_simbolo

    def actualizar_nombre_empresa(self, nuevo_nombre):
        self.nombre_empresa = nuevo_nombre

    def actualizar_precios(self, nuevo_precio_compra, nuevo_precio_venta):
        self.precio_compra = nuevo_precio_compra
        self.precio_venta = nuevo_precio_venta

    def __str__(self):
        return (f"ID: {self._id_accion}, Símbolo: {self._simbolo}, "
                f"Empresa: {self._nombre_empresa}, Precio Compra: {self._precio_compra}, "
                f"Precio Venta: {self._precio_venta}")