from cruds.cruds_destinos import insertar_destino, actualizar_destino

class Destinos:
    def __init__(self, nombre, descripcion, actividades, costo, capacidad):
        self.nombre = nombre
        self.descripcion = descripcion
        self.actividades = actividades
        self.costo = costo
        self.capacidad = capacidad

    def insertar_destino(self):
        insertar_destino(self.nombre, self.descripcion, self.actividades, self.costo)

    def actualizar_destino(self, id_destino):
        actualizar_destino(id_destino, self.nombre, self.descripcion, self.actividades, self.costo)

