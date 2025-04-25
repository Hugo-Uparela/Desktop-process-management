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
                        try:
                            num = int(f.split("-", 2)[1])
                            maxn = max(maxn, num)
                        except ValueError:
                            continue
            self.catalog_counter[crit] = maxn + 1

    def generate_catalog_id(self, criterio):
        n = self.catalog_counter[criterio]
        return f"{criterio}-{n:02d}"

    def capture(self, cantidad, criterio):
        """
        Captura procesos únicos (por PID), los ordena por uso de CPU o memoria
        y devuelve los primeros `cantidad` como lista de Proceso.
        """
        raw = {}
        for p in psutil.process_iter(['pid', 'name', 'username', 'memory_info', 'cpu_percent']):
            try:
                info = p.info
                pid = info['pid']
                if pid not in raw:
                    raw[pid] = info
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        procs = list(raw.values())
        if criterio == 'cpu':
            keyfunc = lambda x: x.get('cpu_percent', 0)
        else:
            keyfunc = lambda x: (x['memory_info'].rss if x.get('memory_info') else 0)

        procs.sort(key=keyfunc, reverse=True)
        seleccionado = procs[:cantidad]

        resultado = []
        cat_name = f"Catálogo {criterio.upper()} {self.catalog_counter[criterio]}"
        for idx, p in enumerate(seleccionado, 1):
            prio = 1 if 'system' in (p.get('username') or '').lower() else 0
            proc_obj = Proceso(
                idx,
                cat_name,
                p['pid'],
                p.get('name', 'desconocido'),
                p.get('username', 'desconocido'),
                prio
            )
            resultado.append(proc_obj)

        return resultado

    def save(self, procesos, criterio, nombre_catalogo):
        """
        Guarda el listado de procesos en catalogos/{criterio}/,
        usando un ID generado y el nombre (por defecto o personalizado).
        """
        cid = self.generate_catalog_id(criterio)
        filename = f"{cid}-{nombre_catalogo}.json"
        ruta = os.path.join("catalogos", criterio, filename)
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump([p.to_dict() for p in procesos], f, indent=4)
        self.catalog_counter[criterio] += 1
        return criterio, filename
