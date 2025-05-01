import customtkinter as ctk
from tkinter import messagebox, simpledialog, ttk
from procesos.manager import DatabaseManager as ProcessManager
from ver_catalogos.mostrar_catalogos import mostrar_catalogos

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🛠️ Gestor de Procesos")
        self.geometry("900x650")
        self.minsize(800, 600)

        # Header
        header = ctk.CTkFrame(self, fg_color="#1f1f1f", corner_radius=0, height=80)
        header.pack(fill="x")
        ctk.CTkLabel(
            header,
            text="GESTOR DE PROCESOS",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white"
        ).place(relx=0.02, rely=0.3)

        # Contenedor principal
        container = ctk.CTkFrame(self, fg_color="#242424", corner_radius=12)
        container.pack(fill="both", expand=True, padx=20, pady=(10, 20))

        # Inputs: Cantidad + Criterio + Botón
        row = ctk.CTkFrame(container, fg_color="transparent")
        row.pack(fill="x", pady=(15, 5), padx=15)

        ctk.CTkLabel(row, text="Cantidad:", width=80).grid(row=0, column=0, sticky="w")
        self.entry_num = ctk.CTkEntry(row, width=80, placeholder_text="Ej: 5")
        self.entry_num.grid(row=0, column=1, padx=(5,20))

        self.criteria = ctk.StringVar(value="cpu")
        cpu_rb = ctk.CTkRadioButton(row, text="CPU", variable=self.criteria, value="cpu")
        mem_rb = ctk.CTkRadioButton(row, text="Memoria", variable=self.criteria, value="memoria")
        cpu_rb.grid(row=0, column=2, padx=5)
        mem_rb.grid(row=0, column=3, padx=5)

        ctk.CTkButton(
            row,
            text="🔍 Capturar",
            command=self.on_capture,
            corner_radius=8,
            width=120
        ).grid(row=0, column=4, padx=(20,0))

        # Treeview estilizado
        tree_frame = ctk.CTkFrame(container, fg_color="transparent")
        tree_frame.pack(fill="both", expand=True, padx=15, pady=10)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Custom.Treeview",
            background="#2b2b2b",
            foreground="white",
            rowheight=30,
            fieldbackground="#2b2b2b"
        )
        style.map("Custom.Treeview", background=[("selected", "#3b8ed0")])

        cols = ("PID", "Nombre", "Usuario", "Prioridad")
        self.tree = ttk.Treeview(
            tree_frame,
            columns=cols,
            show="headings",
            style="Custom.Treeview"
        )
        for c, w in zip(cols, (80, 250, 250, 100)):
            self.tree.heading(c, text=c)
            self.tree.column(c, width=w, anchor="center")

        vsb = ctk.CTkScrollbar(tree_frame, orientation="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y", pady=(0,5))
        self.tree.pack(fill="both", expand=True)

        # Botones de acción
        btns = ctk.CTkFrame(container, fg_color="transparent")
        btns.pack(fill="x", pady=(5,15), padx=15)
        ctk.CTkButton(btns, text="💾 Guardar", command=self.on_save, width=100).pack(side="left", padx=10)
        ctk.CTkButton(btns, text="📚 Catálogos", command=self.show_saved_catalogs, width=120).pack(side="left")

        # Status Bar
        self.status = ctk.CTkLabel(self, text="🔋 Listo", height=30, fg_color="#1f1f1f")
        self.status.pack(fill="x", side="bottom")

        # Lógica inicial
        self.manager = ProcessManager()
        self.procesos = []
        self.current_catalog_name = ""

    def on_capture(self):
        try:
            n = int(self.entry_num.get())
        except ValueError:
            return messagebox.showerror("Error", "Ingresa un número válido")

        crit = self.criteria.get()
        self.procesos = self.manager.capture(n, crit)
        if self.procesos:
            # Guardamos el nombre por defecto para el diálogo
            self.current_catalog_name = self.procesos[0].nombre_catalogo

        # Limpia y rellena el Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        for proc in self.procesos:
            self.tree.insert(
                "",
                "end",
                values=(proc.pid, proc.nombre, proc.usuario, proc.prioridad)
            )
        self.status.configure(text=f"🖥️ Capturados: {len(self.procesos)} procesos")

    def on_save(self):
        if not self.procesos:
            return messagebox.showwarning("Atención", "No hay procesos para guardar")

        criterio = self.criteria.get()
        preview_id = self.manager.generate_catalog_id(criterio)
        prompt = f"ID del catálogo: {preview_id}\nIngrese el nombre del catálogo:"
        # Valor por defecto en el diálogo
        nombre = simpledialog.askstring(
            "Guardar catálogo",
            prompt,
            initialvalue=self.current_catalog_name
        )
        if not nombre:
            return  # Usuario canceló o no ingresó

        crit, filename = self.manager.save(self.procesos, criterio, nombre)
        messagebox.showinfo("OK", f"Guardado en catalogos/{crit}/{filename}")

    def show_saved_catalogs(self):
        mostrar_catalogos()
