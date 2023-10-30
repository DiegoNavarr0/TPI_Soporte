import hashlib

from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from datetime import datetime

app = Flask(__name__)

class FinanzasApp:
    def __init__(self):
        self.esta_validado = False
        # Conexión a la base de datos
        self.db = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="123456",
            database="tpi_soporte"
        )
        self.cursor = self.db.cursor()

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

    def insertar_usuario(self, usuario, password):
        # Hashear la contraseña
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Insertar el usuario
        query = "INSERT INTO usuario (usuario, pwd) VALUES (%s, %s)"
        values = (usuario, hashed_password)

        try:
            self.cursor.execute(query, values)
            self.db.commit()
            return True  # User registration successful
        except mysql.connector.Error as err:
            print("Error inserting user:", err)
            self.db.rollback()
            return False  # User registration failed

    def registro_exitoso(self):
        # You can create a method that redirects to the login page after a successful registration
        return redirect(url_for('login'))

    def validar_usuario(self, usuario, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        query = "SELECT id_usuario FROM usuario WHERE usuario = %s AND pwd = %s"
        self.cursor.execute(query, (usuario, hashed_password))
        result = self.cursor.fetchone()
        print("Authentication result:", result)  # Add this line for debugging
        if result is not None:
            return True
        else:
            return False

app_finanzas = FinanzasApp()

@app.route('/inicio')
def inicio():

    if not app_finanzas.esta_validado:
        return redirect('/')

    # Utiliza la lógica de la clase FinanzasApp para obtener el saldo actual y el historial de transacciones
    saldo_actual = app_finanzas.obtener_saldo(id_usuario=1)  # Reemplaza '1' con el ID del usuario actual
    historial = app_finanzas.obtener_historial_transacciones(id_usuario=1)  # Reemplaza '1' con el ID del usuario actual

    # Renderiza la plantilla HTML e incluye el saldo actual y el historial de transacciones como datos
    return render_template('inicio.html', saldo_actual=saldo_actual, historial=historial)

# Ruta para mostrar la página de inicio de sesión
@app.route('/', methods=['GET', 'POST'])
def login():
    if app_finanzas.esta_validado:
        return redirect('/inicio')

    if request.method == 'POST':
        # Si el método de solicitud es POST, significa que se envió el formulario de inicio de sesión.

        # Obtén los datos del formulario
        usuario = request.form.get('usuario')
        password = request.form.get('password')

        # Lógica de autenticación (aquí debes implementar la autenticación de usuario)
        usuario_autenticado = app_finanzas.validar_usuario(usuario, password)
        if usuario_autenticado:
            # El usuario se autenticó correctamente, redirige a la página de inicio.
            return redirect('/inicio')
        else:
            # La autenticación falló, muestra un mensaje de error.
            return render_template('login.html', error="Usuario o contraseña incorrectos")

    else:
        # Si el método de solicitud es GET, muestra el formulario de inicio de sesión.
        return render_template('login.html')

@app.route('/registro')
def registro():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        password = request.form.get('password')

        if app_finanzas.insertar_usuario(usuario, password):
            # Registration successful, redirect to login page
            return app_finanzas.registro_exitoso()

    return render_template('registro.html')


@app.route('/agregar_transaccion', methods=['GET', 'POST'])
def agregar_transaccion():
    if request.method == 'POST':
        # Obten los datos del formulario.
        descripcion = request.form.get('descripcion')
        monto = float(request.form.get('monto'))

        # Crea una instancia de la clase FinanzasApp
        app_finanzas = FinanzasApp()

        #Agregar la transacción
        app_finanzas.agregar_transaccion(id_usuario, descripcion, monto)

        # Después de agregar la transacción, podrías redirigir al usuario a la página de inicio
        return redirect('/')
    else:
        # Si el método de solicitud es GET, muestra el formulario para agregar una transacción.
        return render_template('agregar_transaccion.html')

@app.route('/agregar_servicio', methods=['GET', 'POST'])
def agregar_servicio():
    if request.method == 'POST':
        # Procesa los datos del formulario para agregar un servicio.
        # Utiliza la lógica de tu clase FinanzasApp para agregar el servicio.
        return redirect('/')
    else:
        # Muestra el formulario para agregar un servicio (puede ser un formulario HTML).
        return render_template('agregar_servicio.html')

# Implementa más rutas y vistas para mostrar dinero disponible y el historial de transacciones.
# Asegúrate de conectarte a tu clase FinanzasApp para obtener los datos necesarios.

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=3306)
