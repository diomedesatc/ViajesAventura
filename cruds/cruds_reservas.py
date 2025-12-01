from .conexionmysql import ConexionMysql

conexion = ConexionMysql()

def insertar_reserva(fecha, id_usuario, id_paquete, estado):
    try:
        sql = 'INSERT INTO reservas (fecha, id_usuario, id_paquete, estado) VALUES (%s, %s, %s, %s)'
        conexion.cursor.execute(sql, (fecha, id_usuario, id_paquete, estado))
        conexion.conexion.commit()
        return True
    except Exception as e:
        conexion.conexion.rollback()
        print(f"Error al insertar reserva: {e}")
        return False

def ver_reservas():
    try:
        sql = ('SELECT r.id, r.fecha, u.nombre, p.nombre, r.estado FROM reservas as r '
               'INNER JOIN usuarios as u ON r.id_usuario = u.id '
               'INNER JOIN paquetes as p ON r.id_paquete = p.id ')
        conexion.cursor.execute(sql)
        resultado = conexion.cursor.fetchall()
        return resultado
    except Exception as e:
        raise e

def editar_reserva(id, fecha, id_usuario, id_paquete, estado):
    try:
        sql = 'UPDATE reservas SET fecha=%s, id_usuario=%s, id_paquete=%s, estado=%s WHERE id=%s'
        datos = (fecha, id_usuario, id_paquete, estado, id)
        conexion.cursor.execute(sql, datos)
        conexion.conexion.commit()
    except Exception as e:
        conexion.conexion.rollback()
        raise e
    
def cancelar_reserva(id_reserva):
    try:
        sql = "UPDATE reservas SET estado = 'Cancelada' WHERE id = %s"
        datos = (id_reserva,)
        conexion.cursor.execute(sql, datos)
        conexion.conexion.commit()
        return True
    except Exception as e:
        conexion.conexion.rollback()
        print(f"Error al cancelar reserva: {e}")
        return False

def eliminar_reserva(id):
    try:
        sql = 'DELETE FROM reservas WHERE id=%s'
        datos = (id,)
        conexion.cursor.execute(sql, datos)
        conexion.conexion.commit()
    except Exception as e:
        conexion.conexion.rollback()
        raise e
    
def obtener_reservas_por_usuario(id_usuario):
    try:
        sql = """
            SELECT 
                r.id AS id_reserva, 
                r.fecha, 
                p.nombre AS nombre_paquete, 
                r.estado 
            FROM reservas r
            JOIN paquetes p ON r.id_paquete = p.id
            WHERE r.id_usuario = %s
        """
        datos = (id_usuario,)
        conexion.cursor.execute(sql, datos)
        resultado = conexion.cursor.fetchall()
        return resultado
    except Exception as e:
        raise e


def obtener_informacion_reserva(id_reserva):
    try:
        sql = 'SELECT * FROM reservas WHERE id = %s'
        datos = (id_reserva,)
        conexion.cursor.execute(sql, datos)
        resultado = conexion.cursor.fetchall()
        return resultado
    except Exception as e:
        raise e


def confirmar_reserva(id_reserva):
    print(f"--- INICIANDO PAGO PARA RESERVA ID: {id_reserva} ---")

    try:
        id_final = id_reserva
        if isinstance(id_reserva, tuple):
            id_final = id_reserva[0]

        consulta = f"UPDATE reservas SET estado = 'Confirmada' WHERE id = {id_final}"

        print(f"EJECUTANDO SQL: {consulta}")
        conexion.cursor.execute(consulta)
        conexion.conexion.commit()

        return True

    except Exception as e:
        print(f"ERROR CRÍTICO AL PAGAR: {e}")
        try:
            conexion.conexion.rollback()
        except:
            pass