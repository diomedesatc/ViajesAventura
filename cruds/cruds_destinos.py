from .conexionmysql import ConexionMysql

conexion = ConexionMysql()


def insertar_destino(nombre, descripcion, actividades, costo):
    try:
        sql = ('INSERT INTO destinos(nombre, descripcion, actividades, costo)'
               ' VALUES (%s, %s, %s, %s)')

        datos = (nombre, descripcion, actividades, costo)
        conexion.cursor.execute(sql, datos)
        conexion.conexion.commit()
    except Exception as e:
        raise e

def ver_los_destinos():
    try:
        sql = 'SELECT * FROM destinos'
        conexion.cursor.execute(sql)
        resultado = conexion.cursor.fetchall()
        return resultado
    except Exception as e:
        raise e

def actualizar_destino(id,nombre, descripcion, actividades, costo):
    try:
        sql = ('UPDATE destinos(nombre, descripcion, actividades, costo)'
               'SET nombre=%s, descripcion=%s, actividades=%s, costo=%s'
               'WHERE id=%s')
        datos = (nombre, descripcion, actividades, costo, id)
        conexion.cursor.execute(sql, datos)
        conexion.conexion.commit()
    except Exception as e:
        raise e
