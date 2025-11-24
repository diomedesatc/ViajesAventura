import pymysql

class ConexionMysql:
    def __init__(self):
        try:
            self.conexion = pymysql.connect(
                host='localhost',
                port=3306,
                user='root',
                password='',
                database='viajes_aventura_db'
            )

            self.cursor = self.conexion.cursor()
        except Exception as e:
            raise e