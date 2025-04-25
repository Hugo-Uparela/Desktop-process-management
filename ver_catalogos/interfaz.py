import os
import tkinter as tk
from tkinter import ttk
from .utilidades import cargar_procesos_desde_archivo

def crear_ventana_catalogos(categorias_con_archivos):
    ventana = tk.Toplevel()
    ventana.title("Catálogos Guardados")
    ventana.geometry("1000x600")

    notebook = ttk.Notebook(ventana)
    notebook.pack(fill="both", expand=True)

    colores = [
        "#aed6f1", "#f9e79f", "#f5b7b1", "#a9dfbf",
        "#f7dc6f", "#d7bde2", "#f1948a", "#a2d9ce",
        "#f0b27a", "#abebc6"
    ]

    for categoria, (categoria_path, archivos) in categorias_con_archivos.items():
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=categoria.upper())

        tree = ttk.Treeview(
            frame,
            columns=("ID", "Nombre", "PID", "Proceso", "Usuario", "Prioridad"),
            show="headings"
        )

        encabezados = {
            "ID": "ID Catálogo",
            "Nombre": "Nombre del Catálogo",
            "PID": "PID",
            "Proceso": "Nombre del Proceso",
            "Usuario": "Usuario",
            "Prioridad": "Prioridad"
        }

        for col, txt in encabezados.items():
            tree.heading(col, text=txt)
            ancho = 250 if col in ["Nombre", "Proceso"] else 100
            tree.column(col, width=ancho, anchor="center")

        tree.pack(fill="both", expand=True, padx=10, pady=10)

        tag_counter = 0

        for archivo in sorted(archivos):
            archivo_path = os.path.join(categoria_path, archivo)
            procesos = cargar_procesos_desde_archivo(archivo_path)

            archivo_sin_ext = archivo.replace(".json", "")
            partes = archivo_sin_ext.split("-", 2)

            catalogo_id = f"{partes[0]}-{partes[1]}" if len(partes) >= 3 else archivo_sin_ext
            nombre_catalogo = partes[2] if len(partes) >= 3 else "(Desconocido)"

            tag_name = f"tag_{tag_counter}"
            color_fondo = colores[tag_counter % len(colores)]
            tree.tag_configure(tag_name, background=color_fondo)
            tag_counter += 1

            for p in procesos:
                tree.insert("", tk.END, values=(
                    catalogo_id, nombre_catalogo,
                    p["pid"], p["nombre"], p["usuario"], p["prioridad"]
                ), tags=(tag_name,))
