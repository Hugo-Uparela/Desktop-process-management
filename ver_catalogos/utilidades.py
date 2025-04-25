import os
import json

def obtener_categorias():
    return ["cpu", "memoria"]

def obtener_archivos_json(path):
    if not os.path.exists(path):
        return []
    return [f for f in os.listdir(path) if f.endswith(".json")]

def cargar_procesos_desde_archivo(archivo_path):
    with open(archivo_path, "r", encoding="utf-8") as f:
        return json.load(f)
