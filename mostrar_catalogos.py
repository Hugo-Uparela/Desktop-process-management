import json
import os
import tkinter as tk
from tkinter import ttk

def mostrar_catalogos():
    base_path = "catalogos"
    categorias = ["cpu", "memoria"]

    for categoria in categorias:
        categoria_path = os.path.join(base_path, categoria)
        if not os.path.exists(categoria_path):
            continue

        archivos = [f for f in os.listdir(categoria_path) if f.endswith(".json")]
        if not archivos:
            continue

        # Crear ventana por categoría
        ventana = tk.Toplevel()
        ventana.title(f"Catálogos de {categoria.upper()}")
        ventana.geometry("1000x600")

        # Crear la tabla principal
        tree = ttk.Treeview(
            ventana,
            columns=("ID", "Nombre", "PID", "Proceso", "Usuario", "Prioridad"),
            show="headings"
        )

        tree.heading("ID", text="ID Catálogo")
        tree.heading("Nombre", text="Nombre del Catálogo")
        tree.heading("PID", text="PID")
        tree.heading("Proceso", text="Nombre del Proceso")
        tree.heading("Usuario", text="Usuario")
        tree.heading("Prioridad", text="Prioridad")

        tree.column("ID", width=100, anchor="center")
        tree.column("Nombre", width=250)
        tree.column("PID", width=80, anchor="center")
        tree.column("Proceso", width=250)
        tree.column("Usuario", width=200)
        tree.column("Prioridad", width=80, anchor="center")

        tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Colores más vivos para distinguir los catálogos
        colores = [
            "#aed6f1", "#f9e79f", "#f5b7b1", "#a9dfbf",
            "#f7dc6f", "#d7bde2", "#f1948a", "#a2d9ce",
            "#f0b27a", "#abebc6"
        ]

        tag_counter = 0

        # Cargar cada archivo/catalogo
        for archivo in sorted(archivos):
            archivo_path = os.path.join(categoria_path, archivo)
            with open(archivo_path, "r", encoding="utf-8") as f:
                procesos = json.load(f)

            archivo_sin_ext = archivo.replace(".json", "")
            partes = archivo_sin_ext.split("-", 2)

            if len(partes) < 3:
                catalogo_id = archivo_sin_ext
                nombre_catalogo = "(Desconocido)"
            else:
                catalogo_id = f"{partes[0]}-{partes[1]}"
                nombre_catalogo = partes[2]

            # Asignar color para este catálogo
            tag_name = f"tag_{tag_counter}"
            color_fondo = colores[tag_counter % len(colores)]
            tree.tag_configure(tag_name, background=color_fondo)
            tag_counter += 1

            # Insertar los procesos del catálogo
            for p in procesos:
                tree.insert("", tk.END, values=(
                    catalogo_id, nombre_catalogo,
                    p["pid"], p["nombre"], p["usuario"], p["prioridad"]
                ), tags=(tag_name,))


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal
    mostrar_catalogos()
    root.mainloop()