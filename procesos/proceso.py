class Proceso:
    def __init__(self, tipo, catalog_id, nombre_catalogo, pid, nombre, usuario, prioridad):
        """
        Representa un proceso capturado con:
        - tipo: "cpu" o "memoria"
        - catalog_id: e.g. "cpu-01"
        - nombre_catalogo: nombre descriptivo opcional
        - pid, nombre, usuario, prioridad
        """
        self.tipo = tipo
        self.catalog_id = catalog_id
        self.nombre_catalogo = nombre_catalogo
        self.pid = pid
        self.nombre = nombre
        self.usuario = usuario
        self.prioridad = prioridad

    def to_dict(self):
        return {
            'tipo': self.tipo,
            'catalog_id': self.catalog_id,
            'nombre_catalogo': self.nombre_catalogo,
            'pid': self.pid,
            'nombre': self.nombre,
            'usuario': self.usuario,
            'prioridad': self.prioridad
        }