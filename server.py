from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask (__name__, static_url_path='/static ')
load_dotenv()

#----CONEXIÓN MYSQL----#
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SECRET_KEY'] = '4848'


mysql= MySQL(app)

#----CONFIGURACIÓN FLASK-LOGIN----#
app.secret_key= "mysecretkey"
login_manager = LoginManager(app)
login_manager.login_view = 'iniciarSesion'
login_manager.login_message = "Por favor inicie sesión para acceder a esta página."

#----MODELO DE USUARIO----#
class User(UserMixin):
    def __init__(self, id, nombre, apellido, email, contrasenia):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.contrasenia = contrasenia

@login_manager.user_loader
def load_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, nombre, apellido, email, contrasenia FROM usuarios WHERE id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    if user:
        return User(user['id'], user['nombre'], user['apellido'], user['email'], user['contrasenia'])
    return None

#----VISTA PÁGINA PRINCIPAL----#
@app.route('/')
def pagPrincipal():
    return render_template ('pagPrincipal.html')

#----VISTA INICIAR SESIÓN----#
@app.route ('/iniciarSesion')
def iniciarSesion():
    return render_template('iniciarSesion.html')

#----VISTA REGISTRO----#
@app.route("/registro")
def registro():
    return render_template("registro.html") 

#----VISTA LISTA DE PACIENTES----#
@app.route('/listaPacientes')
@login_required
def listaPacientes():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM pacientes')
    data = cur.fetchall()
    cur.close()
    return render_template('listaPacientes.html', pacientes = data)

#----VISTA EDITAR DATOS PACIENTE---#
@app.route('/editarDatos/<indice>')
@login_required
def editarDatos(indice):
    cur= mysql.connection.cursor()
    cur.execute('SELECT * FROM pacientes WHERE indice = %s', (indice,))
    data= cur.fetchone()
    cur.close()
    return render_template('editarDatos.html', datos = data)

#----VISTA AÑADIR PACIENTE---#
@app.route('/añadirPaciente')
@login_required
def añadirPaciente():
    return render_template ('añadirPaciente.html')

#----VISTA GRÁFICO----#
@app.route('/grafico')
@login_required
def grafico():
    cur = mysql.connection.cursor()
    cur.execute('SELECT caso, COUNT(*) FROM pacientes GROUP BY caso')
    casos_data = cur.fetchall()

    cur.execute('SELECT sexo, COUNT(*) FROM pacientes GROUP BY sexo')
    sexo_data = cur.fetchall()
    
    cur.execute('SELECT departamento, COUNT(*) FROM pacientes GROUP BY departamento')
    departamentos_data = cur.fetchall()

    cur.execute('''
        SELECT
            CASE
                WHEN edad BETWEEN 0 AND 9 THEN '0-9'
                WHEN edad BETWEEN 10 AND 19 THEN '10-19'
                WHEN edad BETWEEN 20 AND 29 THEN '20-29'
                WHEN edad BETWEEN 30 AND 39 THEN '30-39'
                WHEN edad BETWEEN 40 AND 49 THEN '40-49'
                WHEN edad BETWEEN 50 AND 59 THEN '50-59'
                WHEN edad >= 60 THEN '60+'
            END AS rango_edad,
            COUNT(*) AS cantidad
        FROM pacientes
        GROUP BY rango_edad
        ORDER BY FIELD(rango_edad, '0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60+');
    ''')
    edades_data = cur.fetchall()

    cur.close()
    
    casos_labels = [row['caso'] for row in casos_data]
    casos_values = [row['COUNT(*)'] for row in casos_data]

    sexo_labels = [row['sexo'] for row in sexo_data]
    sexo_values = [row['COUNT(*)'] for row in sexo_data]

    departamentos_labels = [row['departamento'] for row in departamentos_data]
    departamentos_values = [row['COUNT(*)'] for row in departamentos_data]

    edades_labels = [row['rango_edad'] for row in edades_data]
    edades_values = [row['cantidad'] for row in edades_data]


    
    return render_template('grafico.html', casos_labels=casos_labels, casos_values=casos_values, 
                           sexo_labels=sexo_labels, sexo_values=sexo_values,
                           departamentos_labels=departamentos_labels, departamentos_values=departamentos_values,
                           edades_labels=edades_labels, edades_values=edades_values)

#----FUNCION INICIAR SESIÓN----#
@app.route('/func_iniciarSesion', methods=['POST', 'GET'])
def func_iniciarSesion():
    if request.method == 'POST' and 'email' in request.form and 'contrasenia' in request.form:
        email = request.form['email']
        contrasenia = request.form['contrasenia']

        cur = mysql.connection.cursor()
        cur.execute('SELECT id, nombre, apellido, email, contrasenia FROM usuarios WHERE email = %s and contrasenia = %s', (email, contrasenia,))
        user = cur.fetchone()

        if user:
            user_obj = User(user['id'], user['nombre'], user['apellido'], user['email'], user['contrasenia'])
            login_user(user_obj)
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('listaPacientes'))
        else:
            flash('Email o contraseña incorrectos. Por favor, intenta nuevamente.', 'error')
    return redirect(url_for('listaPacientes'))

#----FUCIÓN REGISTRO----#
@app.route("/func_registro",methods= ["GET", "POST"])
def func_registro():
    if request.method =="POST":
        nombre= request.form["nombre"]
        apellido= request.form["apellido"]
        email= request.form["email"]
        contrasenia= request.form["contrasenia"]

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        email_existente = cur.fetchone()
        cur.close()

        if email_existente:
            flash(f'El email {email} ya está en uso. Por favor, utiliza otro.', 'error')
            return redirect(url_for('registro'))
        else:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO usuarios (nombre, apellido, email, contrasenia)VALUES(%s,%s,%s,%s)",
                        (nombre, apellido, email, contrasenia))
            mysql.connection.commit()

            nuevo_usuario_id = cur.lastrowid
            user_obj = User(nuevo_usuario_id, nombre, apellido, email, contrasenia)
            login_user(user_obj)
            flash('Registro exitoso. ¡Bienvenido!', 'success')
    return redirect(url_for('listaPacientes'))

#----FUCIÓN EDITAR DATOS PACIENTE----#
@app.route('/func_editarDatos/<indice>', methods=['POST'])
def func_editarDatos(indice):
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        dni = request.form['dni']
        edad = request.form['edad']
        sexo = request.form['sexo']
        telefono = request.form['telefono']
        provincia = request.form['provincia']
        departamento = request.form['departamento']
        caso = request.form['caso']
        
        cur= mysql.connection.cursor()
        cur.execute('SELECT * FROM pacientes WHERE dni = %s AND indice != %s', (dni, indice))
        dniExistente= cur.fetchone()
        cur.close()

        if dniExistente:
            flash(f'El DNI {dni} ya está asociado a otro paciente.', 'error')
            return redirect(url_for('editarDatos', indice = indice))
        else:
            cur= mysql.connection.cursor()
            cur.execute('''UPDATE pacientes SET nombre = %s, apellido= %s, dni= %s,  edad= %s,
                    sexo= %s,  telefono= %s, provincia= %s, departamento= %s,
                    caso= %s WHERE indice= %s''', 
                    (nombre, apellido, dni, edad, sexo, telefono, provincia, departamento, caso, indice))
            mysql.connection.commit()
            cur.close()
            flash(f'Datos del paciente con DNI {dni} editados correctamente.', 'success')
    return redirect(url_for('listaPacientes'))

#----FUNCIÓN AÑADIR PACIENTE----#
@app.route('/func_añadirPaciente', methods=['POST'])
def func_añadirPaciente():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        dni = request.form['dni']
        edad = request.form['edad']
        sexo = request.form['sexo']
        telefono = request.form['telefono']
        provincia = request.form['provincia']
        departamento = request.form['departamento']
        caso = request.form['caso']

        cur= mysql.connection.cursor()
        cur.execute('SELECT * FROM pacientes WHERE dni = %s', (dni,))
        dniExistente= cur.fetchone()
        cur.close()

        if dniExistente:
            flash(f'El DNI {dni} ya está asociado a otro paciente', 'error')
            return redirect(url_for('añadirPaciente'))
        else:
            cur = mysql.connection.cursor()
            cur.execute('''INSERT INTO pacientes (nombre, apellido, dni, edad, sexo, telefono, provincia, 
                        departamento, caso) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                        (nombre,apellido,dni,edad,sexo,telefono,provincia,departamento,caso))
            mysql.connection.commit()
            cur.close()
            flash(f'Paciente con DNI {dni} agregado correctamente.', 'success')
    return redirect(url_for('listaPacientes'))

#----FUNCIÓN ELIMINAR PACIENTE----# BOTON DE CONFIRMACION QUIERE O CANCELAR
@app.route('/eliminarPaciente/<indice>')
def eliminarPaciente(indice):
    cur= mysql.connection.cursor()
    cur.execute('SELECT dni FROM pacientes WHERE indice = %s', (indice,))
    dniEliminado = cur.fetchone()['dni']
    cur.execute('DELETE FROM pacientes WHERE indice = %s', (indice,))
    mysql.connection.commit()
    cur.close()
    flash(f'Paciente con DNI {dniEliminado} eliminado correctamente', 'success')
    return redirect(url_for('listaPacientes'))

#----FUCIÓN CERRAR SESIÓN----#LO MISMO ACA
@app.route('/cerrarSesion')
@login_required
def cerrarSesion():
    logout_user()
    flash('Has cerrado sesión.', 'success')
    return redirect(url_for('pagPrincipal'))

if __name__ == '__main__':
    app.run(port = 5000, debug = True)