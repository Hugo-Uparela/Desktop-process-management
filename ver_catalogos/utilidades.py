import sqlite3

class CatalogosDB:
    def __init__(self, db_path="procesos.db"):
        # Conecta a la base de datos SQLite
        self.conn = sqlite3.connect(db_path)

    def listar_catalogos(self, criterio):
        """
        Devuelve una lista de nombres de catálogo (catalog_id) distintos para el criterio dado.
        """
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT DISTINCT catalog_id FROM {criterio} ORDER BY catalog_id")
        return [row[0] for row in cursor.fetchall()]

    def listar_catalogos_con_id(self, criterio):
        """
        Devuelve una lista de tuplas (catalog_id, nombre_catalogo) distintos para el criterio dado.
        """
        cursor = self.conn.cursor()
        cursor.execute(
            f"SELECT DISTINCT catalog_id, nombre_catalogo FROM {criterio} ORDER BY catalog_id"
        )
        return cursor.fetchall()

    def obtener_procesos(self, criterio, catalog_id):
        """
        Devuelve los procesos de un catálogo específico: [(pid, nombre, usuario, prioridad), ...]
        """
        cursor = self.conn.cursor()
        cursor.execute(
            f"SELECT pid, nombre, usuario, prioridad FROM {criterio} WHERE catalog_id = ?",
            (catalog_id,)
        )
        return cursor.fetchall()

    def obtener_procesos_completos(self, criterio, catalog_id):
        """
        Devuelve procesos incluyendo ID y nombre de catálogo:
        [(catalog_id, nombre_catalogo, pid, nombre, usuario, prioridad), ...]
        """
        cursor = self.conn.cursor()
        cursor.execute(
            f"SELECT catalog_id, nombre_catalogo, pid, nombre, usuario, prioridad FROM {criterio} WHERE catalog_id = ?",
            (catalog_id,)
        )
        return cursor.fetchall()
