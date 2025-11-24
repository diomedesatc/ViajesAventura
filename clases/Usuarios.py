from cruds.cruds_usuarios import crear_usuario
from cruds.cruds_destinos import ver_los_destinos

class Usuarios:
    def __init__(self, nombre, apellido, direccion, telefono, correo, contrasena, rut, rol):
        self.nombre = nombre,
        self.apellido = apellido
        self.direccion = direccion
        self.telefono = telefono
        self.correo = correo
        self.contrasena = contrasena
        self.rut = rut
        self.rol = rol

    def insertar_usuario(self):
        try:
            crear_usuario(self.nombre, self.apellido, self.direccion, self.telefono, self.correo, self.contrasena,self.rut, self.rol)
        except Exception as e:
            raise e

    def ver_destinos(self):
        ver_los_destinos()

