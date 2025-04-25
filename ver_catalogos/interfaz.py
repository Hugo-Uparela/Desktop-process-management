import os
import customtkinter as ctk
from tkinter import ttk
from .utilidades import cargar_procesos_desde_archivo


def crear_ventana_catalogos(categorias_con_archivos, parent=None):
    """
    Muestra un Toplevel con los catálogos guardados. No inicia un nuevo mainloop.
    """
    # Ventana hija de parent si se proporciona
    ventana = ctk.CTkToplevel(parent) if parent else ctk.CTkToplevel()
    ventana.title("📚 Catálogos Guardados")
    ventana.configure(fg_color="#242424", corner_radius=12)
    w, h = 1000, 600
    sw, sh = ventana.winfo_screenwidth(), ventana.winfo_screenheight()
    ventana.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
    ventana.grab_set()

    # Marco interior
    cont = ctk.CTkFrame(ventana, fg_color="#1f1f1f", corner_radius=12)
    cont.pack(fill="both", expand=True, padx=20, pady=20)

    # Notebook
    notebook = ttk.Notebook(cont)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    # Estilo para Treeview
    style = ttk.Style()
    style.theme_use("clam")
    # Fuente más grande y filas más altas
    style.configure("Cat.Treeview",
                    background="#2b2b2b",
                    foreground="black",
                    rowheight=32,
                    fieldbackground="#2b2b2b",
                    font=("Segoe UI", 13))
    style.configure("Cat.Treeview.Heading",
                    font=("Segoe UI", 14, "bold"))
    style.map("Cat.Treeview",
              background=[("selected", "#3b8ed0")])

    colores = [
        "#B0C4DE",  # LightSteelBlue
        "#C0C0C0",  # Silver
        "#D3D3D3",  # LightGray
        "#D8BFD8",  # Thistle
        "#BC8F8F"   # RosyBrown
    ]

    for idx_cat, (categoria, (ruta_cat, archivos)) in enumerate(categorias_con_archivos.items()):
        frame = ctk.CTkFrame(notebook, fg_color="#242424", corner_radius=8)
        notebook.add(frame, text=categoria.upper())

        tree = ttk.Treeview(
            frame,
            columns=("ID", "Nombre", "PID", "Proceso", "Usuario", "Prioridad"),
            show="headings",
            style="Cat.Treeview"
        )
        for col, txt in [("ID", "ID Catálogo"), ("Nombre", "Nombre Catálogo"),
                         ("PID", "PID"), ("Proceso", "Proceso"),
                         ("Usuario", "Usuario"), ("Prioridad", "Prioridad")]:
            tree.heading(col, text=txt)
            width = 250 if col in ("Nombre", "Proceso") else 100
            tree.column(col, width=width, anchor="center")

        vsb = ctk.CTkScrollbar(frame, orientation="vertical",
                               command=tree.yview, fg_color="#1f1f1f")
        tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y", pady=10)
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Insertar filas
        for i, archivo in enumerate(archivos):
            procesos = cargar_procesos_desde_archivo(
                os.path.join(ruta_cat, archivo))
            sin_ext = archivo[:-5]
            partes = sin_ext.split("-", 2)
            cat_id = f"{partes[0]}-{partes[1]}" if len(
                partes) >= 3 else sin_ext
            nombre_cat = partes[2] if len(partes) >= 3 else "(Desconocido)"

            tag = f"row_{i}"
            bg = colores[i % len(colores)]
            tree.tag_configure(tag, background=bg)

            for p in procesos:
                tree.insert("", "end",
                            values=(cat_id, nombre_cat,
                                    p["pid"], p["nombre"],
                                    p["usuario"], p["prioridad"]),
                            tags=(tag,))

    # No iniciar mainloop; es parte de la app principal
    return ventana
