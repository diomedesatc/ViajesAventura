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

    def realizar_reserva(self, id_paquete, fecha_viaje):
        nueva_reserva = Reserva(
            fecha=fecha_viaje,
            id_usuario=self.rut,
            id_paquete=id_paquete,
            estado="Confirmada"
        )
        nueva_reserva.guardar()
        return True

    def ver_destinos(self):
        ver_los_destinos()

