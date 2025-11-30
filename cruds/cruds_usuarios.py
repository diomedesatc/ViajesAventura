from .conexionmysql import ConexionMysql
import bcrypt

conexion = ConexionMysql()

def hashear_contrasena(contrasena):
    sal = bcrypt.gensalt()
    contrasena_hasheada = bcrypt.hashpw(contrasena.encode('utf-8'), sal)
    return contrasena_hasheada.decode('utf-8')

def validar_contrasena(contrasena_ingresada, contrasena_almacenada):
    return bcrypt.checkpw(contrasena_ingresada.encode('utf-8'), contrasena_almacenada.encode('utf-8'))


def crear_usuario(nombre, apellido, direccion, telefono, correo, password, rut, rol):
    try:
        password_str = str(password)
        contrasena_hash = hashear_contrasena(password_str)
        sql = ('INSERT INTO usuarios(nombre, apellido, direccion, telefono, correo, password, rut, rol)'
               'VALUES(%s, %s, %s, %s, %s, %s, %s, %s)')
        datos = (nombre, apellido, direccion, telefono, correo, contrasena_hash, rut, rol)
        conexion.cursor.execute(sql, datos)
        conexion.conexion.commit()
    except Exception as e:
        conexion.conexion.rollback()
        raise e

def buscar_usuario(correo):
    try:
        sql = "SELECT * FROM usuarios WHERE correo = %s"
        datos = (correo,)
        conexion.cursor.execute(sql, datos)
        resultado = conexion.cursor.fetchone()
        return resultado
    except Exception as e:
        conexion.conexion.rollback()
        raise e

def mostrar_nombres_usuario():
    try:
        sql = "SELECT nombre FROM usuarios"
        conexion.cursor.execute(sql)
        resultado = conexion.cursor.fetchall()
        return resultado
    except Exception as e:
        raise e

def buscar_usuario_por_nombre(nombre):
    try:
        sql = "SELECT * FROM usuarios WHERE nombre = %s"
        datos = (nombre,)
        conexion.cursor.execute(sql, datos)
        resultado = conexion.cursor.fetchone()
        return resultado[0]
    except Exception as e:
        raise e
