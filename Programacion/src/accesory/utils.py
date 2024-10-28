from prettytable import PrettyTable

def mostrar(titulo, ancho=112):
    
    tabla_titulo = PrettyTable()
    tabla_titulo.field_names = [titulo]  

    tabla_titulo.align[titulo] = "c"  
    
    tabla_titulo.min_width[titulo] = ancho

    tabla_titulo.add_row(["ARG BROKER DEMO"])

    print(tabla_titulo)