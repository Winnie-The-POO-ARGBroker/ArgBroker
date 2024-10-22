class Usuario:
    def __init__(self, id, nombre, apellido, cuil, email, contraseña, fecha_registro, saldo=1000000.00, total_invertido=0.00, rendimiento_total=0.00):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.cuil = cuil
        self.email = email
        self.contraseña = contraseña
        self.fecha_registro = fecha_registro 
        self.saldo = saldo
        self.total_invertido = total_invertido
        self.rendimiento_total = rendimiento_total

    def __str__(self):
        return f"Usuario({self.nombre}, {self.apellido}, {self.cuil}, {self.email}, Fecha Registro: {self.fecha_registro}, Saldo: {self.saldo}, Total Invertido: {self.total_invertido}, Rendimiento Total: {self.rendimiento_total})"
