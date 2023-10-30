from flask import Flask, render_template, request, redirect, session
import controlador_finanzas

app= Flask(__name__)
app.config['SECRET_KEY'] = '446644'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Si el método de solicitud es POST, significa que se envió el formulario de inicio de sesión.

        # Obtén los datos del formulario
        usuario = request.form.get('usuario')
        password = request.form.get('password')

        # Lógica de autenticación
        usuario_id = controlador_finanzas.validar_usuario(usuario, password)
        if usuario_id:
            session['id_usuario'] = usuario_id
            return redirect('/inicio')
        else:
            # La autenticación falló, muestra un mensaje de error.
            return render_template('login.html', error="Usuario o contraseña incorrectos")

    else:
        # Si el método de solicitud es GET, muestra el formulario de inicio de sesión.
        return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        password = request.form.get('password')

        if controlador_finanzas.insertar_usuario(usuario, password):
            return redirect('/')
    return render_template('registro.html')

@app.route('/inicio')
def inicio():
    if 'id_usuario' in session:
        id_usuario = session['id_usuario']
        saldo_actual = controlador_finanzas.obtener_saldo(id_usuario)  # Reemplaza '1' con el ID del usuario actual
        historial = controlador_finanzas.obtener_historial_transacciones(id_usuario)  # Reemplaza '1' con el ID del usuario actual

        # Renderiza la plantilla HTML e incluye el saldo actual y el historial de transacciones como datos
        return render_template('inicio.html', saldo_actual=saldo_actual, historial=historial)
    else:
        return redirect('/')

@app.route('/agregar_transaccion', methods=['GET', 'POST'])
def agregar_transaccion():
    if request.method == 'POST':
        if 'id_usuario' in session:
            id_usuario = session['id_usuario']
            descripcion = request.form.get('descripcion')
            monto = float(request.form.get('monto'))
            tipo_transaccion = request.form.get('tipo_transaccion')

            if controlador_finanzas.insertar_transaccion(id_usuario, descripcion, monto, tipo_transaccion):
                return redirect('/inicio')
            else:
                return render_template('agregar_transaccion.html', error="Error al agregar la transacción")

    else:
        return render_template('agregar_transaccion.html')

@app.route('/usuarios')
def mostrar_usuarios():
    usuarios = controlador_finanzas.obtener_usuarios_registrados()
    return render_template('usuarios.html', usuarios=usuarios)

if __name__ == "__main__":
    app.run(host= '0.0.0.0', port = 8000, debug=True)