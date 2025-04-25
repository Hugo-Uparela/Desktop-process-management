import os
from .interfaz import crear_ventana_catalogos
from .utilidades import obtener_categorias, obtener_archivos_json

def mostrar_catalogos():
    base_path = "catalogos"
    categorias = obtener_categorias()
    categorias_con_archivos = {}

    for categoria in categorias:
        categoria_path = os.path.join(base_path, categoria)
        archivos = obtener_archivos_json(categoria_path)
        if archivos:
            categorias_con_archivos[categoria] = (categoria_path, archivos)

    if categorias_con_archivos:
        crear_ventana_catalogos(categorias_con_archivos)
