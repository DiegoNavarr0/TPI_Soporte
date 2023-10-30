import pymysql
def obtener_conexion():
    return pymysql.connect(host = "127.0.0.1", user="root", password="123456", db="tpi_soporte")

