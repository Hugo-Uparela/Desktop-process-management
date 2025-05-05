import customtkinter as ctk
from tkinter import ttk
from .utilidades import CatalogosDB

def crear_ventana_catalogos(parent=None):
    ventana = ctk.CTkToplevel(parent) if parent else ctk.CTkToplevel()
    ventana.title("📚 Catálogos Guardados")
    ventana.configure(fg_color="#242424", corner_radius=12)
    w, h = 1000, 600
    sw, sh = ventana.winfo_screenwidth(), ventana.winfo_screenheight()
    ventana.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
    ventana.grab_set()

    cont = ctk.CTkFrame(ventana, fg_color="#1f1f1f", corner_radius=12)
    cont.pack(fill="both", expand=True, padx=20, pady=20)

    notebook = ttk.Notebook(cont)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Cat.Treeview",
                    background="#2b2b2b",
                    foreground="white",
                    rowheight=32,
                    fieldbackground="#2b2b2b",
                    font=("Segoe UI", 13))
    style.configure("Cat.Treeview.Heading",
                    font=("Segoe UI", 14, "bold"))
    style.map("Cat.Treeview",
              background=[("selected", "#3b8ed0")])

    db = CatalogosDB()
    for criterio in ("cpu", "memoria"):
        frame = ctk.CTkFrame(notebook, fg_color="#242424", corner_radius=8)
        notebook.add(frame, text=criterio.upper())

        tree = ttk.Treeview(
            frame,
            columns=("ID_Cat", "Nombre_Cat", "PID", "Proceso", "Usuario", "Prioridad"),
            show="headings",
            style="Cat.Treeview"
        )
        headings = [
            ("ID_Cat", "ID Catálogo", 120),
            ("Nombre_Cat", "Nombre Catálogo", 200),
            ("PID", "PID", 80),
            ("Proceso", "Proceso", 200),
            ("Usuario", "Usuario", 200),
            ("Prioridad", "Prioridad", 100),
        ]
        for col, txt, width in headings:
            tree.heading(col, text=txt)
            tree.column(col, width=width, anchor="center")

        vsb = ctk.CTkScrollbar(frame, orientation="vertical",
                               command=tree.yview, fg_color="#1f1f1f")
        tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y", pady=10)
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Para cada catálogo (catalog_id, nombre_catalogo) cargamos los procesos
        for catalog_id, nombre_cat in db.listar_catalogos_con_id(criterio):
            procesos = db.obtener_procesos_completos(criterio, catalog_id)
            tag = f"cat_{catalog_id}"
            for pid, proc_name, usuario, prioridad in procesos:
                tree.insert(
                    "",
                    "end",
                    values=(catalog_id, nombre_cat, pid, proc_name, usuario, prioridad),
                    tags=(tag,)
                )
            # Opcional: fondo distinto por catálogo
            tree.tag_configure(tag, background="#2b2b2b" if criterio=="cpu" else "#313131")

    return ventana
