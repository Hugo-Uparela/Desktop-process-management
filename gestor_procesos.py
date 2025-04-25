import psutil
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json
import os
from mostrar_catalogos import mostrar_catalogos


class Proceso:
    def __init__(self, catalogo, nombre_catalogo, pid, nombre, usuario, prioridad):
        self.catalogo = catalogo
        self.nombre_catalogo = nombre_catalogo
        self.pid = pid
        self.nombre = nombre
        self.usuario = usuario
        self.prioridad = prioridad

    def to_dict(self):
        return self.__dict__


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Procesos")
        self.root.geometry("800x600")

        self.label_num = tk.Label(root, text="Número de procesos a capturar:")
        self.label_num.pack(pady=5)
        self.entry_num = tk.Entry(root)
        self.entry_num.pack(pady=5)

        self.label_info = tk.Label(
            root, text="Seleccione el criterio de selección de procesos:")
        self.label_info.pack(pady=5)

        self.criteria_var = tk.StringVar(value="cpu")
        self.radio_cpu = tk.Radiobutton(
            root, text="Mayor uso de CPU", variable=self.criteria_var, value="cpu")
        self.radio_memory = tk.Radiobutton(
            root, text="Mayor uso de Memoria", variable=self.criteria_var, value="memoria")
        self.radio_cpu.pack()
        self.radio_memory.pack()

        self.button_start = tk.Button(
            root, text="Iniciar Captura", command=self.start_capture)
        self.button_start.pack(pady=10)

        self.label_processes = tk.Label(
            root, text="Procesos capturados aparecerán aquí")
        self.label_processes.pack(pady=10)

        self.tree = ttk.Treeview(root, columns=(
            "PID", "Nombre", "Usuario", "Prioridad"), show="headings")
        self.tree.heading("PID", text="PID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Usuario", text="Usuario")
        self.tree.heading("Prioridad", text="Prioridad")
        self.tree.column("PID", width=100)
        self.tree.column("Nombre", width=200)
        self.tree.column("Usuario", width=250)
        self.tree.column("Prioridad", width=100)
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

        self.button_save = tk.Button(
            root, text="Guardar Procesos", command=self.save_processes)
        self.button_save.pack(pady=10)

        self.button_show_catalogs = tk.Button(
            root, text="Mostrar Catálogos Guardados", command=self.show_saved_catalogs)
        self.button_show_catalogs.pack(pady=10)

        self.procesos = []
        self.catalog_counter = {"cpu": 1, "memoria": 1}
        self.inicializar_contadores()

        self.current_catalog_name = ""

        os.makedirs("catalogos/cpu", exist_ok=True)
        os.makedirs("catalogos/memoria", exist_ok=True)

    def inicializar_contadores(self):
        for criterio in ["cpu", "memoria"]:
            path = os.path.join("catalogos", criterio)
            max_num = 0
            if os.path.exists(path):
                for archivo in os.listdir(path):
                    if archivo.endswith(".json"):
                        partes = archivo.replace(".json", "").split("-", 2)
                        if len(partes) >= 2 and partes[1].isdigit():
                            num = int(partes[1])
                            if num > max_num:
                                max_num = num
            self.catalog_counter[criterio] = max_num + 1

    def generar_catalogo_id(self, criterio):
        contador = self.catalog_counter[criterio]
        return f"{criterio}-{'{:02d}'.format(contador)}"

    def start_capture(self):
        try:
            self.num_procesos = int(self.entry_num.get())
        except ValueError:
            messagebox.showerror(
                "Error", "Ingrese un número válido de procesos.")
            return

        criterio = self.criteria_var.get()

        all_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'username', 'memory_info', 'cpu_percent']):
            try:
                proc_info = proc.info
                all_processes.append(proc_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        if criterio == "cpu":
            all_processes.sort(key=lambda p: p['cpu_percent'], reverse=True)
        else:
            all_processes.sort(
                key=lambda p: p['memory_info'].rss if p['memory_info'] else 0, reverse=True)

        selected_processes = all_processes[:self.num_procesos]

        for row in self.tree.get_children():
            self.tree.delete(row)

        self.procesos.clear()

        self.label_processes.config(
            text=f"Mostrando {len(selected_processes)} procesos seleccionados:")

        self.current_catalog_name = f"Catalogo {criterio.upper()} {self.catalog_counter[criterio]}"

        for idx, proc in enumerate(selected_processes, start=1):
            prioridad = 1 if 'system' in (
                proc.get('username') or '').lower() else 0
            proceso = Proceso(
                catalogo=idx,
                nombre_catalogo=self.current_catalog_name,
                pid=proc['pid'],
                nombre=proc['name'],
                usuario=proc.get('username', 'desconocido'),
                prioridad=prioridad
            )
            self.procesos.append(proceso)
            self.tree.insert("", tk.END, values=(
                proceso.pid, proceso.nombre, proceso.usuario, proceso.prioridad))

    def save_processes(self):
        if not self.procesos:
            messagebox.showwarning(
                "Advertencia", "No hay procesos para guardar.")
            return

        # criterio = "cpu" if "CPU" in self.current_catalog_name.upper() else "memory"
        criterio = "cpu" if "CPU" in self.current_catalog_name.upper() else "memoria"
        catalog_id = self.generar_catalogo_id(criterio)

        nombre_catalogo_usuario = simpledialog.askstring(
            "Guardar catálogo",
            f"ID del Catálogo: {catalog_id}\nIngrese el nombre del catálogo:",
            initialvalue=self.current_catalog_name
        )

        if not nombre_catalogo_usuario:
            messagebox.showwarning(
                "Advertencia", "Debe ingresar un nombre para el catálogo.")
            return

        nombre_final = f"{catalog_id}-{nombre_catalogo_usuario}"
        filepath = os.path.join("catalogos", criterio, f"{nombre_final}.json")

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump([p.to_dict() for p in self.procesos], f, indent=4)

        self.catalog_counter[criterio] += 1
        messagebox.showinfo("Éxito", f"Procesos guardados en {filepath}.")

    def show_saved_catalogs(self):
        mostrar_catalogos()  # <-- Llamamos la función externa para mostrar los catálogos


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
