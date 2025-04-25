from .utilidades import listar_catalogos_por_categoria
from .interfaz import crear_ventana_catalogos

def mostrar_catalogos():
    cats = listar_catalogos_por_categoria()
    crear_ventana_catalogos(cats)