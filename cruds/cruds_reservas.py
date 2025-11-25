from .conexionmysql import ConexionMysql

conexion = ConexionMysql()


def ver_reservas():
    try:
        sql = 'SELECT * FROM reservas'
        conexion.cursor.execute(sql)
        resultado = conexion.cursor.fetchall()
        return resultado
    except Exception as e:
        raise e

def eliminar_reserva(id):
    try:
        sql = 'DELETE FROM reservas WHERE id=%s'
        datos = (id,)
        conexion.cursor.execute(sql, datos)
        conexion.conexion.commit()
    except Exception as e:
        conexion.conexion.rollback()
        raise e