from cruds.cruds_reservas import insertar_reserva, editar_reserva


class Reserva:
    def __init__(self, fecha, id_usuario, id_paquete, estado="Pendiente"):
        self.fecha = fecha
        self.id_usuario = id_usuario
        self.id_paquete = id_paquete
        self.estado = estado
    
    def guardar(self):
        insertar_reserva(self.fecha, self.id_usuario, self.id_paquete, self.estado)
        print("Reserva guardada exitosamente.")

    def actualizar(self, id):
        editar_reserva(id, self.fecha, self.id_usuario, self.id_paquete, self.estado)