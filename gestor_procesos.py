import os
import json
import psutil
import customtkinter as ctk
from tkinter import messagebox, simpledialog, ttk

ctk.set_appearance_mode("dark")               
ctk.set_default_color_theme("green")         

class Proceso:
    def __init__(self, idx, nombre_catalogo, pid, nombre, usuario, prioridad):
        self.catalogo = idx
        self.nombre_catalogo = nombre_catalogo
        self.pid = pid
        self.nombre = nombre
        self.usuario = usuario
        self.prioridad = prioridad

    def to_dict(self):
        return self.__dict__


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
            command=self.start_capture,
            corner_radius=8,
            width=120
        ).grid(row=0, column=4, padx=(20,0))

        # Treeview estilizado
        tree_frame = ctk.CTkFrame(container, fg_color="transparent")
        tree_frame.pack(fill="both", expand=True, padx=15, pady=10)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.Treeview",
                        background="#2b2b2b",
                        foreground="white",
                        rowheight=30,
                        fieldbackground="#2b2b2b")
        style.map("Custom.Treeview",
                  background=[("selected", "#3b8ed0")])

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
        ctk.CTkButton(btns, text="💾 Guardar", command=self.save_processes, width=100).pack(side="left", padx=10)
        ctk.CTkButton(btns, text="📚 Catálogos", command=self.show_saved_catalogs, width=120).pack(side="left")

        # Status Bar
        self.status = ctk.CTkLabel(self, text="🔋 Listo", height=30, fg_color="#1f1f1f")
        self.status.pack(fill="x", side="bottom")

        # Lógica inicial
        self.procesos = []
        self.catalog_counter = {"cpu":1, "memoria":1}
        self.current_catalog_name = ""
        self.inicializar_contadores()
        os.makedirs("catalogos/cpu", exist_ok=True)
        os.makedirs("catalogos/memoria", exist_ok=True)

    def inicializar_contadores(self):
        for criterio in ["cpu","memoria"]:
            path = os.path.join("catalogos",criterio)
            maxn = 0
            if os.path.exists(path):
                for f in os.listdir(path):
                    if f.endswith(".json"):
                        num = int(f.split("-",2)[1])
                        maxn = max(maxn, num)
            self.catalog_counter[criterio] = maxn+1

    def generar_catalogo_id(self, criterio):
        n = self.catalog_counter[criterio]
        return f"{criterio}-{n:02d}"

    def start_capture(self):
        try:
            n = int(self.entry_num.get())
        except:
            messagebox.showerror("Error","Ingresa un número válido")
            return

        procs = []
        for p in psutil.process_iter(['pid','name','username','memory_info','cpu_percent']):
            try: procs.append(p.info)
            except: pass

        key = 'cpu_percent' if self.criteria.get()=="cpu" else 'memory_info'
        procs.sort(key=lambda x: x[key] if key=='cpu_percent' else (x['memory_info'].rss if x['memory_info'] else 0),
                   reverse=True)
        sel = procs[:n]

        for r in self.tree.get_children(): self.tree.delete(r)
        self.procesos.clear()

        crit = self.criteria.get()
        cat_name = f"Catálogo {crit.upper()} {self.catalog_counter[crit]}"
        self.current_catalog_name = cat_name
        for idx,p in enumerate(sel,1):
            prio = 1 if 'system' in (p.get('username') or '').lower() else 0
            proc = Proceso(idx, cat_name, p['pid'], p['name'], p.get('username','desconocido'), prio)
            self.procesos.append(proc)
            self.tree.insert("", "end", values=(proc.pid, proc.nombre, proc.usuario, proc.prioridad))

        self.status.configure(text=f"🖥️ Capturados: {len(sel)} procesos")

    def save_processes(self):
        if not self.procesos:
            messagebox.showwarning("Atención","No hay procesos para guardar")
            return
        crit = "cpu" if "CPU" in self.current_catalog_name.upper() else "memoria"
        cid = self.generar_catalogo_id(crit)
        
        # Pregunta con valor por defecto
        name = simpledialog.askstring(
            "Guardar catálogo",
            f"ID del catálogo: {cid}\nIngrese el nombre del catálogo:",
            initialvalue=self.current_catalog_name
        )

        if not name:
            return
        filename = f"{cid}-{name}.json"
        with open(os.path.join("catalogos",crit,filename),"w",encoding="utf-8") as f:
            json.dump([p.to_dict() for p in self.procesos], f, indent=4)
        self.catalog_counter[crit] += 1
        messagebox.showinfo("OK",f"Guardado en catalogos/{crit}/{filename}")

    def show_saved_catalogs(self):
        from ver_catalogos.mostrar_catalogos import mostrar_catalogos
        mostrar_catalogos()

if __name__ == "__main__":
    app = App()
    app.mainloop()
