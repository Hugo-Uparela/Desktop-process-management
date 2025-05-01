import customtkinter as ctk
from tkinter import ttk
from .utilidades import CatalogosDB

CONTENT_FONT = ("Segoe UI", 10, "bold")  


def mostrar_catalogos():
    db = CatalogosDB()
    window = ctk.CTkToplevel()
    window.title("Catálogos guardados")
    window.geometry("900x600")
    window.grab_set()

    sel_frame = ctk.CTkFrame(window)
    sel_frame.pack(fill="x", padx=20, pady=10)

    ctk.CTkLabel(sel_frame, text="Criterio:").grid(row=0, column=0, sticky="w", padx=(0,10))

    def on_crit_change(choice):
        key = choice.lower()
        if key == "ambos":
            cpu = db.listar_catalogos_con_id("cpu")
            mem = db.listar_catalogos_con_id("memoria")
            combined = [nombre for _, nombre in cpu] + [nombre for _, nombre in mem]
            seen = []
            nombres = [x for x in combined if not (x in seen or seen.append(x))]
        else:
            con_id = db.listar_catalogos_con_id(key)
            nombres = [nombre for _, nombre in con_id]
        opciones = ["Todos"] + nombres
        opt_name.configure(values=opciones)
        opt_name.set(opciones[0] if opciones else "")

    opt_crit = ctk.CTkOptionMenu(
        sel_frame,
        values=["cpu", "memoria", "ambos"],
        command=on_crit_change
    )
    opt_crit.set("cpu")
    opt_crit.grid(row=0, column=1, sticky="w", padx=(0,20))

    ctk.CTkLabel(sel_frame, text="Catálogo:").grid(row=0, column=2, sticky="w", padx=(0,10))
    con_id_ini = db.listar_catalogos_con_id("cpu")
    nombres_ini = [nombre for _, nombre in con_id_ini]
    opciones_ini = ["Todos"] + nombres_ini
    opt_name = ctk.CTkOptionMenu(sel_frame, values=opciones_ini)
    opt_name.set(opciones_ini[0] if opciones_ini else "")
    opt_name.grid(row=0, column=3, sticky="w")

    # Paleta de colores para distinguir catálogos
    palette = ["#B0C4DE", "#C0C0C0", "#D3D3D3", "#D8BFD8", "#BC8F8F"]

    def on_show():
        crit = opt_crit.get().lower()
        nombre = opt_name.get()
        cursor = db.conn.cursor()
        if crit == "ambos":
            if nombre == "Todos":
                cursor.execute(
                    """
                    SELECT catalog_id, nombre_catalogo, pid, nombre, usuario, prioridad FROM cpu
                    UNION ALL
                    SELECT catalog_id, nombre_catalogo, pid, nombre, usuario, prioridad FROM memoria
                    """
                )
            else:
                cursor.execute(
                    """
                    SELECT catalog_id, nombre_catalogo, pid, nombre, usuario, prioridad FROM cpu WHERE nombre_catalogo = ?
                    UNION ALL
                    SELECT catalog_id, nombre_catalogo, pid, nombre, usuario, prioridad FROM memoria WHERE nombre_catalogo = ?
                    """, (nombre, nombre)
                )
        else:
            if nombre == "Todos":
                cursor.execute(
                    f"SELECT catalog_id, nombre_catalogo, pid, nombre, usuario, prioridad FROM {crit}"
                )
            else:
                cursor.execute(
                    f"SELECT catalog_id, nombre_catalogo, pid, nombre, usuario, prioridad"
                    f" FROM {crit} WHERE nombre_catalogo = ?",
                    (nombre,)
                )
        procesos = cursor.fetchall()

        # Limpiar y configurar tags de colores por catálogo
        for item in tree.get_children():
            tree.delete(item)
        catalog_ids = []
        for row in procesos:
            cid = row[0]
            if cid not in catalog_ids:
                catalog_ids.append(cid)
        color_map = {cid: palette[i % len(palette)] for i, cid in enumerate(catalog_ids)}
        for cid, color in color_map.items():
            tree.tag_configure(cid, background=color)

        # Insertar filas con tag = catalog_id
        for fila in procesos:
            cid = fila[0]
            tree.insert("", "end", values=fila, tags=(cid,))

    ctk.CTkButton(sel_frame, text="Mostrar", command=on_show).grid(row=0, column=4, padx=(20,0))

    tree_frame = ctk.CTkFrame(window, fg_color="transparent")
    tree_frame.pack(fill="both", expand=True, padx=20, pady=(0,20))

    style = ttk.Style()
    style.theme_use("clam")
    # Fuente del contenido de la tabla
        # Fuente del contenido de la tabla con texto negro
    style.configure(
        "Catalog.Treeview",
        background="#2b2b2b",
        foreground="black",
        rowheight=25,
        fieldbackground="#2b2b2b",
        font=CONTENT_FONT
    )
    style.map(
        "Catalog.Treeview",
        background=[("selected", "#3b8ed0")]
    )
    # Encabezados mantienen fuente separada
    style.configure(
        "Catalog.Treeview.Heading",
        font=("Segoe UI", 14, "bold")
    )

    cols = ("ID", "Catálogo", "PID", "Nombre", "Usuario", "Prioridad")
    tree = ttk.Treeview(
        tree_frame,
        columns=cols,
        show="headings",
        style="Catalog.Treeview"
    )
    for col, width in zip(cols, (60, 150, 80, 250, 200, 100)):
        tree.heading(col, text=col)
        tree.column(col, width=width, anchor="center")

    vsb = ctk.CTkScrollbar(tree_frame, orientation="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    tree.pack(fill="both", expand=True)

    ctk.CTkButton(window, text="Cerrar", command=window.destroy).pack(pady=(0,10))
