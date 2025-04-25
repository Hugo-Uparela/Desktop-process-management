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