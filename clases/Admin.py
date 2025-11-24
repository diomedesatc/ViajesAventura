from clases.Usuarios import Usuarios
from cruds.cruds_destinos import insertar_destino


class Admin(Usuarios):
    def __init__(self, nombre, apellido, direccion, telefono, correo, contrasena, rut, rol):
        super().__init__(nombre, apellido, direccion, telefono, correo, contrasena, rut, rol)


    def crear_destino(self, nombre, descripcion, actividades, costo):
        try:
            insertar_destino(nombre, descripcion, actividades, costo)
        except Exception as e:
            raise e
