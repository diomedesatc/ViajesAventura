from cruds.cruds_paquetes import insertar_paquete, actualizar_paquete_db

class Paquetes:
    def __init__(self, nombre, fecha_inicio, fecha_fin, destinos, precio, cupos_disponibles):
        self.nombre = nombre
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.destinos = destinos
        self.precio = precio
        self.cupos_disponibles = cupos_disponibles


    def insertar_paquetes(self):
        insertar_paquete(
            self.nombre,
            self.fecha_inicio,
            self.fecha_fin,
            self.destinos,
            self.precio,
            self.cupos_disponibles
        )

    def actualizar_paquetes(self, id_paquete):
        actualizar_paquete_db(
            id_paquete,
            self.nombre,
            self.fecha_inicio,
            self.fecha_fin,
            self.precio,
            self.cupos_disponibles,
            self.destinos
        )