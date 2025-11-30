from .conexionmysql import ConexionMysql

conexion = ConexionMysql()


def insertar_paquete(nombre, fecha_inicio, fecha_fin, destinos, precio, cupos_disponibles):
    try:
        sql = ('INSERT INTO paquetes(nombre, fecha_inicio, fecha_fin, precio, cupos_disponibles)'
               ' VALUES (%s, %s, %s, %s, %s)')
        datos = (nombre, fecha_inicio, fecha_fin, precio, cupos_disponibles)
        conexion.cursor.execute(sql, datos)
        id_paquete_generado = conexion.cursor.lastrowid

        sql_relacion = 'INSERT INTO paquete_destinos(id_paquete, id_destino) VALUES (%s, %s)'
        for id_destino in destinos:
            conexion.cursor.execute(sql_relacion, (id_paquete_generado,id_destino))

        conexion.conexion.commit()
    except Exception as e:
        conexion.conexion.rollback()
        raise e


def ver_paquetes():
    try:
        sql = ('SELECT * FROM paquetes')
        conexion.cursor.execute(sql)
        respuesta = conexion.cursor.fetchall()
        return respuesta
    except Exception as e:
        raise e

def ver_nombre_paquetes():
    try:
        sql = 'SELECT nombre FROM paquetes'
        conexion.cursor.execute(sql)
        respuesta = conexion.cursor.fetchall()
        return respuesta
    except Exception as e:
        raise e

def eliminar_paquete(id):
    try:
        sql = 'DELETE FROM paquetes WHERE id=%s'
        datos = (id,)
        conexion.cursor.execute(sql, datos)
        conexion.conexion.commit()
    except Exception as e:
        conexion.conexion.rollback()
        raise e

def buscar_paquete(id):
    try:
        sql = 'SELECT * FROM paquetes WHERE id=%s'
        datos = (id,)
        conexion.cursor.execute(sql,datos)
        respuesta = conexion.cursor.fetchone()
        return respuesta
    except Exception as e:
        raise e

def obtener_destinos_de_paquete(id_paquete):
    """Recupera los destinos asociados a un paquete específico"""
    try:
        # Hacemos un JOIN para traer el nombre del destino también
        sql = ('SELECT d.id, d.nombre, d.costo '
               'FROM destinos d '
               'INNER JOIN paquete_destinos pd ON d.id = pd.id_destino '
               'WHERE pd.id_paquete = %s')
        conexion.cursor.execute(sql, (id_paquete,))
        return conexion.cursor.fetchall() # Devuelve lista de tuplas [(1, 'Paris'), (5, 'Roma')]
    except Exception as e:
        print(f"Error al obtener destinos del paquete: {e}")
        return []

def actualizar_paquete_db(id_paquete, nombre, f_inicio, f_fin, precio, cupos, lista_destinos):
    """Actualiza info básica y regenera la lista de destinos"""
    try:
        # 1. Actualizar datos básicos
        sql_update = ('UPDATE paquetes '
                      'SET nombre=%s, fecha_inicio=%s, fecha_fin=%s, precio=%s, cupos_disponibles=%s '
                      'WHERE id=%s')
        datos_basicos = (nombre, f_inicio, f_fin, precio, cupos, id_paquete)
        conexion.cursor.execute(sql_update, datos_basicos)

        # 2. ELIMINAR todas las relaciones viejas en la tabla intermedia
        sql_delete_rel = 'DELETE FROM paquete_destinos WHERE id_paquete = %s'
        conexion.cursor.execute(sql_delete_rel, (id_paquete,))

        # 3. INSERTAR las nuevas relaciones (sean las mismas o nuevas)
        sql_insert_rel = 'INSERT INTO paquete_destinos(id_paquete, id_destino) VALUES (%s, %s)'
        for id_destino in lista_destinos:
            conexion.cursor.execute(sql_insert_rel, (id_paquete, id_destino))

        conexion.conexion.commit()
        return True
    except Exception as e:
        conexion.conexion.rollback()
        print(f"Error al actualizar paquete: {e}")
        raise e

def buscar_paquete_por_nombre(nombre):
    try:
        sql = 'SELECT * FROM paquetes WHERE nombre=%s'
        datos = (nombre,)
        conexion.cursor.execute(sql, datos)
        respuesta = conexion.cursor.fetchone()
        return respuesta[0]
    except Exception as e:
        raise e