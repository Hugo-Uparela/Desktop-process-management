import sqlite3
import psutil
import time
from .proceso import Proceso

# Definición de cuentas del sistema
SYSTEM_ACCOUNTS = {"SYSTEM", "LOCALSERVICE", "NETWORKSERVICE"}

class DatabaseManager:
    def __init__(self, db_path="procesos.db"):
        self.conn = sqlite3.connect(db_path)
        self._crear_tablas()

    def _crear_tablas(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS cpu (
            catalog_id TEXT NOT NULL,
            nombre_catalogo TEXT NOT NULL,
            pid INTEGER NOT NULL,
            nombre TEXT NOT NULL,
            usuario TEXT NOT NULL,
            prioridad INTEGER NOT NULL
        )""")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS memoria (
            catalog_id TEXT NOT NULL,
            nombre_catalogo TEXT NOT NULL,
            pid INTEGER NOT NULL,
            nombre TEXT NOT NULL,
            usuario TEXT NOT NULL,
            prioridad INTEGER NOT NULL
        )""")
        self.conn.commit()

    def capture(self, n, criterio):
        procesos = list(psutil.process_iter(['pid', 'name', 'username']))
        raw_usages = []
        if criterio == "cpu":
            for p in procesos:
                try:
                    p.cpu_percent(None)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            time.sleep(0.1)
            for p in procesos:
                try:
                    uso = p.cpu_percent(None)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                raw_usages.append((p, uso))
        else:
            for p in procesos:
                try:
                    uso = p.memory_percent()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                raw_usages.append((p, uso))

        raw_usages.sort(key=lambda x: x[1], reverse=True)
        seleccion = raw_usages[:n]
        catalog_id = self.generate_catalog_id(criterio)
        resultado = []
        for p, _ in seleccion:
            try:
                info = p.info
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
            nombre_proc = info.get('name') or ''
            # Ignorar procesos sin nombre
            if not nombre_proc.strip():
                continue
            cuenta = (info.get('username') or '').upper().split('\\')[-1]
            prioridad_bin = 1 if cuenta in SYSTEM_ACCOUNTS else 0
            proc = Proceso(
                tipo=criterio,
                catalog_id=catalog_id,
                nombre_catalogo=catalog_id,
                pid=info.get('pid', 0),
                nombre=nombre_proc,
                usuario=info.get('username', ''),
                prioridad=prioridad_bin
            )
            resultado.append(proc)
        return resultado

    def generate_catalog_id(self, criterio):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT COUNT(DISTINCT catalog_id) FROM {criterio}")
        count = cursor.fetchone()[0] or 0
        siguiente = count + 1
        return f"{criterio}-{siguiente:02d}"

    def save(self, lista_procesos, criterio, nombre):
        for proc in lista_procesos:
            proc.nombre_catalogo = nombre
        self._insert_procesos(lista_procesos)
        return criterio, lista_procesos[0].catalog_id

    def _insert_procesos(self, lista_procesos):
        cursor = self.conn.cursor()
        tabla = lista_procesos[0].tipo
        for proc in lista_procesos:
            cursor.execute(
                f"""
                INSERT INTO {tabla} (
                  catalog_id,
                  nombre_catalogo,
                  pid,
                  nombre,
                  usuario,
                  prioridad
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                  proc.catalog_id,
                  proc.nombre_catalogo,
                  proc.pid,
                  proc.nombre,
                  proc.usuario,
                  proc.prioridad
                )
            )
        self.conn.commit()
