from flask import Flask, render_template, redirect, url_for, request, session
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

app = Flask (__name__, static_url_path='/static ')
load_dotenv()
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SECRET_KEY'] = '4848'


mysql= MySQL(app)

#----VISTA PÁGINA PRINCIPAL----#
@app.route('/')
def pagPrincipal():
    return render_template ('pagPrincipal.html')

#----VISTA INICIAR SESIÓN----# NO DEJAR ENTRAR DESDE EL URL.... IMPORT FUNC
@app.route ('/iniciarSesion')
def iniciarSesion():
    return render_template('iniciarSesion.html')

#----VISTA REGISTRO----#
@app.route("/registro")
def registro():
    return render_template("registro.html") 

#----VISTA LISTA DE PACIENTES----#
@app.route('/listaPacientes')
def listaPacientes():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM pacientes')
    data = cur.fetchall()
    cur.close()
    return render_template('listaPacientes.html', pacientes = data)

#----VISTA EDITAR DATOS PACIENTE---#
@app.route('/editarDatos/<indice>')
def editarDatos(indice):
    cur= mysql.connection.cursor()
    cur.execute('SELECT * FROM pacientes WHERE indice = %s', (indice,))
    data= cur.fetchone()
    cur.close()
    return render_template('editarDatos.html', datos = data)

#----VISTA AÑADIR PACIENTE---# MANEJO DE ERRORES  CUANDO HAY REPETICION
@app.route('/añadirPaciente')
def añadirPaciente():
    return render_template ('añadirPaciente.html')

#----VISTA GRÁFICO----# AGREGAR GRAFICOS POR EDAD SEXO ETC
@app.route('/grafico')
def grafico():
    cur = mysql.connection.cursor()
    cur.execute('SELECT caso, COUNT(*) FROM pacientes GROUP BY caso')
    data = cur.fetchall()
    cur.close()
    
    labels = [row['caso'] for row in data]
    values = [row['COUNT(*)'] for row in data]
    
    return render_template('grafico.html', labels=labels, values=values)

#----FUNCION INICIAR SESIÓN----#
@app.route('/func_iniciarSesion', methods=['POST', 'GET'])
def func_iniciarSesion():
    error= None
    if request.method == 'POST' and 'email' in request.form and 'contrasenia' in request.form:
        email = request.form['email']
        contrasenia = request.form['contrasenia']
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE email = %s and contrasenia = %s', (email, contrasenia,))
        account = cur.fetchone()
        cur.close()
        if account:
            return redirect(url_for('listaPacientes'))
        else:
            error = 'Email o contraseña incorrectos. Por favor, intenta nuevamente.'
            return render_template('iniciarSesion.html', error=error)

#----FUCIÓN REGISTRO----#
@app.route("/func_registro",methods= ["GET", "POST"])
def func_registro():
    error= None
    if request.method =="POST":
        nombre= request.form["nombre"]
        apellido= request.form["apellido"]
        dni= request.form["dni"]
        contrasenia= request.form["contrasenia"]
        email= request.form["email"]

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        email_existente= cur.fetchone()
        cur.close()

        if email_existente:
            error = 'El email ya está en uso. Por favor, utiliza otro.'
            return render_template('registro.html', error=error)
        else:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO usuarios (nombre, apellido, dni, contrasenia ,email)VALUES(%s,%s,%s,%s,%s)",
                        (nombre, apellido, dni, contrasenia, email))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for("listaPacientes"))

#----FUCIÓN EDITAR DATOS PACIENTE----#
@app.route('/func_editarDatos/<indice>', methods=['POST'])
def func_editarDatos(indice):
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        dni = request.form['dni']
        provincia = request.form['provincia']
        departamento = request.form['departamento']
        barrio = request.form['barrio']
        calle = request.form['calle']
        numeracion = request.form['numeracion']
        caso = request.form['caso']
        cur= mysql.connection.cursor()
        cur.execute('''UPDATE pacientes SET nombre = %s, apellido= %s, dni= %s, provincia= %s,
                    departamento= %s, barrio= %s, calle= %s, numeracion= %s, caso= %s WHERE indice= %s''', 
                    (nombre, apellido, dni, provincia, departamento, barrio, 
                    calle, numeracion, caso, indice))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('listaPacientes'))

#----FUNCIÓN AÑADIR PACIENTE----#
@app.route('/func_añadirPaciente', methods=['POST'])
def func_añadirPaciente():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        dni = request.form['dni']
        provincia = request.form['provincia']
        departamento = request.form['departamento']
        barrio = request.form['barrio']
        calle = request.form['calle']
        numeracion = request.form['numeracion']
        caso = request.form['caso']
        
        cur = mysql.connection.cursor()
        cur.execute('''INSERT INTO pacientes (nombre, apellido, dni, provincia, 
        departamento, barrio, calle, numeracion, caso) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
        (nombre,apellido,dni,provincia,departamento,barrio,calle,numeracion,caso))
        
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('listaPacientes'))

#----FUNCIÓN ELIMINAR PACIENTE----#
@app.route('/eliminarPaciente/<indice>')
def eliminarPaciente(indice):
    cur= mysql.connection.cursor()
    cur.execute('DELETE FROM pacientes WHERE indice = %s', (indice,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('listaPacientes'))

if __name__ == '__main__':
    app.run(port = 5000, debug = True)