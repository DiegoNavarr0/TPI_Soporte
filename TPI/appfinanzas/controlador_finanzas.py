from datetime import datetime

from conector_db import obtener_conexion

def obtener_saldo(id_usuario):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    query = "SELECT saldo FROM usuario WHERE id_usuario = %s"
    cursor.execute(query, (id_usuario,))
    saldo = cursor.fetchone()[0]
    conexion.close()
    return saldo

def obtener_historial_transacciones(id_usuario):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    query = "SELECT id_transaccion, descripcion, monto FROM operacion WHERE id_usuario = %s"
    cursor.execute(query, (id_usuario,))
    historial = cursor.fetchall()
    conexion.close()
    return historial

def insertar_usuario(usuario, password):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    # Insertar el usuario
    query = "INSERT INTO usuario (usuario, pwd, saldo) VALUES (%s, %s, %s)"
    values = (usuario, password, 0)

    try:
        cursor.execute(query, values)
        conexion.commit()
        conexion.close()
        return True  # User registration successful
    except conexion.Error as err:
        print("Error inserting user:", err)
        conexion.rollback()
        conexion.close()
        return False  # User registration failed

def validar_usuario(usuario, password):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    query = "SELECT id_usuario FROM usuario WHERE usuario = %s AND pwd = %s"
    cursor.execute(query, (usuario, password))
    result = cursor.fetchone()
    print("Authentication result:", result)  # Para debugging
    conexion.close()
    if result is not None:
        return result
    else:
        return False

def obtener_usuarios_registrados():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    query = "SELECT id_usuario, usuario FROM usuario"
    cursor.execute(query)
    usuarios = cursor.fetchall()
    cursor.close()
    conexion.close()
    return usuarios


def insertar_transaccion(id_usuario, descripcion, monto, tipo_transaccion):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    fecha_hora = datetime.now()

    query = "INSERT INTO operacion (id_usuario, id_transaccion, descripcion, monto, fecha_hora) VALUES (%s, %s, %s, %s, %s)"
    values = (id_usuario, tipo_transaccion, descripcion, monto, fecha_hora)

    query_modificar_saldo = None  # Initialize the query_modificar_saldo variable

    if tipo_transaccion == 1:  # Ingreso
        query_modificar_saldo = "UPDATE usuario SET saldo = saldo + %s WHERE id_usuario = %s"
    elif tipo_transaccion == 2:  # Egreso
        query_modificar_saldo = "UPDATE usuario SET saldo = saldo - %s WHERE id_usuario = %s"

    try:
        cursor.execute(query, values)
        if query_modificar_saldo is not None:
            cursor.execute(query_modificar_saldo, (monto, id_usuario))

        conexion.commit()
        conexion.close()
        return True
    except conexion.Error as err:
        print("Error inserting transaction:", err)
        conexion.rollback()
        conexion.close()
        return False

