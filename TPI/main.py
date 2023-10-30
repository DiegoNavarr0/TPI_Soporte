import mysql.connector
from datetime import datetime

# Conexión a la base de datos
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="123456",
    database="tpi_soporte"
)

cursor = db.cursor()

class FinanzasApp:
    def __init__(self, host, user, password, database):
        self.db = mysql.connector.connect(host=host, user=user, password=password, database=database)
        self.cursor = self.db.cursor()

    def agregar_operacion(self, id_usuario, id_transaccion, descripcion, monto, fecha_hora):
        query = "INSERT INTO operacion (id_usuario, id_transaccion, descripcion, monto, fecha_hora) VALUES (%s, %s, %s, %s, %s)"
        values = (id_usuario, id_transaccion, descripcion, monto, fecha_hora)
        self.cursor.execute(query, values)
        self.db.commit()

    def agregar_gastofijo(self, id_usuario, descripcion, monto, dia):
        query = "INSERT INTO gastosfijos (id_usuario, descripcion, monto, dia) VALUES (%s, %s, %s, %s)"
        values = (id_usuario, descripcion, monto, dia)
        self.cursor.execute(query, values)
        self.db.commit()

    def obtener_saldo(self, id_usuario):
        query = "SELECT saldo FROM usuario WHERE id_usuario = %s"
        self.cursor.execute(query, (id_usuario,))
        saldo = self.cursor.fetchone()[0]
        return saldo

    def obtener_historial_transacciones(self, id_usuario):
        query = "SELECT id_transaccion, descripcion, monto FROM operacion WHERE id_usuario = %s"
        self.cursor.execute(query, (id_usuario,))
        historial = self.cursor.fetchall()
        return historial

    def restar_gastos_fijos(self, id_usuario, fecha):
        # Calcular el día del mes de la fecha
        dia_del_mes = fecha.day

        # Obtener los gastos fijos que corresponden al día del mes especificado
        query = "SELECT monto FROM gastosfijos WHERE id_usuario = %s AND dia = %s"
        self.cursor.execute(query, (id_usuario, dia_del_mes))
        gastos_fijos = self.cursor.fetchall()

        # Calcular el total de gastos fijos para ese día
        total_gastos = sum(gasto[0] for gasto in gastos_fijos)

        # Obtener el saldo actual del usuario
        saldo_actual = self.obtener_saldo(id_usuario)

        if saldo_actual is not None:
            # Actualizar el saldo restando los gastos fijos
            nuevo_saldo = saldo_actual - total_gastos
            query = "UPDATE usuario SET saldo = %s WHERE id_usuario = %s"
            self.cursor.execute(query, (nuevo_saldo, id_usuario))
            self.db.commit()
            return nuevo_saldo
        else:
            return None

if __name__ == "__main__":
    app = FinanzasApp("127.0.0.1", "root", "123456", "tpi_soporte")




