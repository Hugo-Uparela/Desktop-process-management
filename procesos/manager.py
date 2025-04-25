import os
import json
import psutil
from procesos.proceso import Proceso

class ProcessManager:
    def __init__(self):
        self.catalog_counter = {"cpu": 1, "memoria": 1}
        self._init_counters()
        os.makedirs("catalogos/cpu", exist_ok=True)
        os.makedirs("catalogos/memoria", exist_ok=True)

    def _init_counters(self):
        for crit in ("cpu", "memoria"):
            path = os.path.join("catalogos", crit)
            maxn = 0
            if os.path.isdir(path):
                for f in os.listdir(path):
                    if f.endswith(".json"):
                        num = int(f.split("-", 2)[1])
                        maxn = max(maxn, num)
            self.catalog_counter[crit] = maxn + 1

    def generate_catalog_id(self, criterio):
        n = self.catalog_counter[criterio]
        return f"{criterio}-{n:02d}"

    def capture(self, cantidad, criterio):
        """
        Captura los procesos actuales, elimina duplicados por PID,
        los ordena según uso de CPU o memoria y devuelve los top `cantidad`
        como objetos Proceso.
        """
        raw = {}
        # 1) Recolectamos info única por PID
        for p in psutil.process_iter(['pid', 'name', 'username', 'memory_info', 'cpu_percent']):
            try:
                info = p.info
                pid = info['pid']
                # Si ya existe ese pid, lo ignoramos
                if pid not in raw:
                    raw[pid] = info
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        procs = list(raw.values())

        # 2) Elegimos la clave para ordenar
        if criterio == 'cpu':
            keyfunc = lambda x: x.get('cpu_percent', 0)
        else:
            keyfunc = lambda x: (x['memory_info'].rss if x.get('memory_info') else 0)

        # 3) Ordenamos descendente y seleccionamos los primeros N
        procs.sort(key=keyfunc, reverse=True)
        seleccionado = procs[:cantidad]

        # 4) Creamos objetos Proceso
        resultado = []
        cat_name = f"Catálogo {criterio.upper()} {self.catalog_counter[criterio]}"
        for idx, p in enumerate(seleccionado, 1):
            prio = 1 if 'system' in (p.get('username') or '').lower() else 0
            proc = Proceso(
                idx,
                cat_name,
                p['pid'],
                p.get('name', 'desconocido'),
                p.get('username', 'desconocido'),
                prio
            )
            resultado.append(proc)

        return resultado

    def save(self, procesos, catalog_name):
        crit = "cpu" if "CPU" in catalog_name.upper() else "memoria"
        cid = self.generate_catalog_id(crit)
        filename = f"{cid}-{catalog_name}.json"
        with open(os.path.join("catalogos", crit, filename), "w", encoding="utf-8") as f:
            json.dump([p.to_dict() for p in procesos], f, indent=4)
        self.catalog_counter[crit] += 1
        return crit, filename