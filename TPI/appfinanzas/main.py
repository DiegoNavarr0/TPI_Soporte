from datetime import datetime

from flask import Flask, render_template, request, redirect, session, flash
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
        saldo_actual = controlador_finanzas.obtener_saldo(id_usuario)
        historial = controlador_finanzas.obtener_historial_transacciones(id_usuario)
        nombre_usuario = controlador_finanzas.obtener_nombre_usuario(id_usuario)

        # Renderiza la plantilla HTML e incluye el saldo actual y el historial de transacciones como datos
        return render_template('inicio.html', usuario= nombre_usuario, saldo_actual=saldo_actual, historial=historial)
    else:
        return redirect('/')

@app.route('/agregar_transaccion', methods=['GET', 'POST'])
def agregar_transaccion():
    if request.method == 'POST':
        if 'id_usuario' in session:
            id_usuario = session['id_usuario']
            descripcion = request.form.get('descripcion')
            monto = float(request.form.get('monto'))
            tipo_transaccion = int(request.form.get('tipo_transaccion'))

            if controlador_finanzas.insertar_transaccion(id_usuario, descripcion, monto, tipo_transaccion):
                return redirect('/inicio')
            else:
                return render_template('agregar_transaccion.html', error="Error al agregar la transacción")

    else:
        return render_template('agregar_transaccion.html')

@app.route('/wish')
def wish():
    if 'id_usuario' in session:
        id_usuario = session['id_usuario']
        wishes = controlador_finanzas.obtener_wishes(id_usuario)
        return render_template('wish.html', wishes=wishes)
    else:
        return redirect('/')

@app.route('/agregar_wish', methods=['GET', 'POST'])
def agregar_wish():
    if request.method == 'POST':
        if 'id_usuario' in session:
            id_usuario = session['id_usuario']
            motivo = request.form.get('motivo')
            monto = float(request.form.get('monto'))

            if controlador_finanzas.agregar_wish(id_usuario, motivo, monto):
                return redirect('/wish')
            else:
                return render_template('wish.html', error="Error al agregar el wish")

    else:
        return render_template('agregar_wish.html')



@app.route('/editar_wish/<int:id_wish>', methods=['GET', 'POST'])
def editar_wish(id_wish):
    if 'id_usuario' in session:
        if request.method == 'POST':
            id_usuario = session['id_usuario']
            motivo = request.form.get('motivo')
            monto = float(request.form.get('monto'))

            if controlador_finanzas.editar_wish(id_usuario, id_wish, motivo, monto):
                return redirect('/wish')
            else:
                return render_template('editar_wish.html', error="Error al editar el wish")
        else:
            wish_obtenido = controlador_finanzas.obtener_wish(id_wish)
            if wish_obtenido:
                return render_template('editar_wish.html', wish=wish_obtenido)
            else:
                return redirect('/wish')
    else:
        return redirect('/')

@app.route('/eliminar_wish/<int:id_wish>', methods=['GET'])
def eliminar_wish(id_wish):
    if controlador_finanzas.eliminar_wish(id_wish):
        return redirect('/wish')
    else:
        flash("Error eliminando wish", "error")
        return redirect('/wish')

@app.route('/gastos_fijos', methods=['GET', 'POST'])
def gastos_fijos():
    if 'id_usuario' in session:
        id_usuario = session['id_usuario']
        gastos = controlador_finanzas.obtener_gastos(id_usuario)
        return render_template('gastos_fijos.html', gastos=gastos)
    else:
        return redirect('/')

@app.route('/agregar_gasto_fijo', methods=['GET', 'POST'])
def agregar_gasto_fijo():
    if request.method == 'POST':
        if 'id_usuario' in session:
            id_usuario = session['id_usuario']
            descripcion = request.form.get('descripcion')
            monto = float(request.form.get('monto'))
            fecha_vencimiento = datetime.strptime(request.form.get('fecha_vencimiento'), '%d')

            if controlador_finanzas.agregar_gasto_fijo(id_usuario, descripcion, monto, fecha_vencimiento):
                return redirect('/gastos_fijos')
            else:
                return render_template('gastos_fijos.html', error="Error al agregar el wish")

    else:
        return render_template('agregar_gasto_fijo.html')

@app.route('/editar_gasto_fijo/<int:id_gastosfijos>', methods=['GET', 'POST'])
def editar_gasto_fijo(id_gastosfijos):
    if 'id_usuario' in session:
        if request.method == 'POST':
            id_usuario = session['id_usuario']
            descripcion = request.form.get('descripcion')
            monto = float(request.form.get('monto'))
            fecha_vencimiento = datetime.strptime(request.form.get('fecha_vencimiento'), '%d')

            if controlador_finanzas.editar_gasto_fijo(id_usuario, id_gastosfijos, descripcion, monto, fecha_vencimiento):
                return redirect('/gastos_fijos')
            else:
                return render_template('editar_gastos_fijos.html', error="Error al editar el gasto fijo")
        else:
            gasto_obtenido = controlador_finanzas.obtener_gasto_fijo(id_gastosfijos)
            if gasto_obtenido:
                return render_template('editar_gasto_fijo.html', gasto=gasto_obtenido)
            else:
                return redirect('/gastos_fijos')
    else:
        return redirect('/')

@app.route('/eliminar_gasto_fijo/<int:id_gastosfijos>', methods=['GET'])
def eliminar_gasto_fijo(id_gastosfijos):
    if controlador_finanzas.eliminar_gasto_fijo(id_gastosfijos):
        return redirect('/gastos_fijos')
    else:
        flash("Error eliminando el gasto fijo", "error")
        return redirect('/gastos_fijos')

if __name__ == "__main__":
    app.run(host= '0.0.0.0', port = 8000, debug=True)