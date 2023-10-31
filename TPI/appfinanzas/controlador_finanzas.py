from datetime import datetime
from conector_db import obtener_conexion

def obtener_saldo(id_usuario):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    query = "SELECT saldo FROM usuario WHERE id_usuario = %s"
    cursor.execute(query, (id_usuario))
    saldo = cursor.fetchone()[0]
    conexion.close()
    return saldo

def obtener_historial_transacciones(id_usuario):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    query = "SELECT id_transaccion, descripcion, monto, fecha_hora FROM operacion WHERE id_usuario = %s"
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
        print("Error registrando usuario:", err)
        conexion.rollback()
        conexion.close()
        return False  # User registration failed

def validar_usuario(usuario, password):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    query = "SELECT id_usuario FROM usuario WHERE usuario = %s AND pwd = %s"
    cursor.execute(query, (usuario, password))
    result = cursor.fetchone()
    conexion.close()
    if result is not None:
        return result
    else:
        return False

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
    print(query_modificar_saldo)
    try:
        cursor.execute(query, values)
        if query_modificar_saldo is not None:
            print(monto, id_usuario)
            cursor.execute(query_modificar_saldo, (monto, id_usuario))
        conexion.commit()
        conexion.close()
        return True
    except conexion.Error as err:
        print("Error agregando transaccion:", err)
        conexion.rollback()
        conexion.close()
        return False

def agregar_wish(id_usuario, motivo, monto):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    fecha_creacion = datetime.now().date()

    query = "INSERT INTO wish (id_usuario, motivo, monto, fecha_creacion) VALUES (%s, %s, %s, %s)"
    values = (id_usuario, motivo, monto, fecha_creacion)

    try:
        cursor.execute(query, values)
        conexion.commit()
        conexion.close()
        return True
    except conexion.Error as err:
        print("Error agregando wish:", err)
        conexion.rollback()
        conexion.close()
        return False

def obtener_wishes(id_usuario):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    query = "SELECT * FROM wish WHERE id_usuario = %s"
    cursor.execute(query, (id_usuario))
    wishes = cursor.fetchall()
    conexion.close()
    return wishes

def editar_wish(id_usuario, id_wish, motivo, monto):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    query = "UPDATE wish SET motivo = %s, monto = %s WHERE id_wish = %s AND id_usuario = %s"
    values = (motivo, monto, id_wish, id_usuario)

    try:
        cursor.execute(query, values)
        conexion.commit()
        conexion.close()
        return True
    except conexion.Error as err:
        print("Error editando wish:", err)
        conexion.rollback()
        conexion.close()
        return False

def obtener_wish(id_wish):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    query = "SELECT * FROM wish WHERE id_wish = %s"
    cursor.execute(query, (id_wish,))
    result = cursor.fetchone()
    conexion.close()
    return result

def eliminar_wish(id_wish):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute("SELECT id_wish FROM wish WHERE id_wish = %s", id_wish)
        if cursor.fetchone():
            cursor.execute("DELETE FROM wish WHERE id_wish = %s", (id_wish,))
            conexion.commit()
            conexion.close()
            return True
        else:
            conexion.close()
            return False
    except conexion.Error as err:
        print("Error eliminando wish:", err)
        conexion.rollback()
        conexion.close()
        return False

def obtener_gastos(id_usuario):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    query = "SELECT * FROM gastosfijos WHERE id_usuario = %s"
    cursor.execute(query, id_usuario)
    gastos = cursor.fetchall()
    conexion.close()
    return gastos

def eliminar_gasto_fijo(id_gasto_fijo):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute("SELECT id_gastosfijos FROM gastosfijos WHERE id_gastosfijos = %s", id_gasto_fijo)
        if cursor.fetchone():
            cursor.execute("DELETE FROM gastosfijos WHERE id_gastosfijos = %s", (id_gasto_fijo,))
            conexion.commit()
            conexion.close()
            return True
        else:
            conexion.close()
            return False
    except conexion.Error as err:
        print("Error eliminando gasto fijo:", err)
        conexion.rollback()
        conexion.close()
        return False

def editar_gasto_fijo(id_usuario, id_gastosfijos, descripcion, monto, fecha_vencimiento):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    query = "UPDATE gastosfijos SET descripcion = %s, monto = %s, fecha_vencimiento = %s WHERE id_gastosfijos = %s AND id_usuario = %s"
    values = (descripcion, monto, fecha_vencimiento, id_gastosfijos, id_usuario)

    try:
        cursor.execute(query, values)
        conexion.commit()
        conexion.close()
        return True
    except conexion.Error as err:
        print("Error editando gasto fijo:", err)
        conexion.rollback()
        conexion.close()
        return False

def obtener_gasto_fijo(id_gastosfijos):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    query = "SELECT * FROM gastosfijos WHERE id_gastosfijos = %s"
    cursor.execute(query, (id_gastosfijos,))
    result = cursor.fetchone()
    conexion.close()
    return result

def agregar_gasto_fijo(id_usuario, descripcion, monto, fecha_vencimiento):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    query = "INSERT INTO gastosfijos (id_usuario, descripcion, monto, fecha_vencimiento) VALUES (%s, %s, %s, %s)"
    values = (id_usuario, descripcion, monto, fecha_vencimiento)
    try:
        cursor.execute(query, values)
        conexion.commit()
        conexion.close()
        return True
    except conexion.Error as err:
        print("Error agregando gasto fijo:", err)
        conexion.rollback()
        conexion.close()
        return False


def obtener_nombre_usuario(id_usuario):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    query = "SELECT usuario FROM usuario WHERE id_usuario = %s"
    cursor.execute(query, id_usuario)
    result = cursor.fetchone()
    nombre_usuario = result[0]
    conexion.close()
    return nombre_usuario