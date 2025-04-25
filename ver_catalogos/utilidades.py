import os
import json

def cargar_procesos_desde_archivo(ruta):
    """
    Carga y retorna la lista de procesos desde un archivo JSON dado su ruta.
    Si no existe el archivo o hay error de lectura, retorna una lista vacía.
    """
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def listar_catalogos_por_categoria():
    """
    Recorre las carpetas 'catalogos/cpu' y 'catalogos/memoria',
    y devuelve un dict con la estructura:
    {
        "cpu": ("catalogos/cpu", [lista de archivos .json]),
        "memoria": ("catalogos/memoria", [lista de archivos .json])
    }
    """
    base = "catalogos"
    categorias = {}
    for crit in ("cpu", "memoria"):
        path = os.path.join(base, crit)
        archivos = []
        if os.path.isdir(path):
            archivos = [f for f in os.listdir(path) if f.endswith(".json")]
        categorias[crit] = (path, sorted(archivos))
    return categorias
