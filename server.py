from flask import Flask, render_template, redirect, url_for, request
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask (__name__, static_url_path='/static ')
load_dotenv()

app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


mysql= MySQL(app)

#----VISTAS----#
@app.route('/')
def inicio():
    return render_template ('index.html')

@app.route('/view_add_sick')
def view_add_sick():
    return render_template ('add_sick.html')

@app.route('/view_sicks')
def view_sicks():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM enfermos')
    data = cur.fetchall()
    print(data)
    return render_template('list_sicks.html', pacientes = data)

@app.route("/registro")
def register():
    return render_template("register.html") 


#----Actualizar datos de paciente----#
@app.route('/editarDatos/<indice>')
def editarDatos(indice):
    cur= mysql.connection.cursor()
    cur.execute('SELECT * FROM enfermos WHERE indice = %s', (indice,))
    data= cur.fetchall()
    cur.close()
    return render_template('editarDatos.html', datos = data[0])

@app.route('/actualizarDatos/<indice>', methods=['POST'])
def actualizarLista(indice):
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
        cur.execute('''UPDATE enfermos SET nombre = %s, apellido= %s, dni= %s, provincia= %s,
                    departamento= %s, barrio= %s, calle= %s, numeracion= %s, caso= %s WHERE indice= %s''', 
                    (nombre, apellido, dni, provincia, departamento, barrio, 
                    calle, numeracion, caso, indice))
        mysql.connection.commit()
        return redirect(url_for('view_sicks'))


#----Eliminar paciente----#
@app.route('/eliminarPaciente/<indice>')
def eliminarPaciente(indice):
    cur= mysql.connection.cursor()
    cur.execute('DELETE FROM enfermos WHERE indice = %s', (indice,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('view_sicks'))


#----Agregar enfermo----#
@app.route('/add_sick', methods=['POST'])
def add_sick():
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
        cur.execute('''INSERT INTO enfermos (nombre, apellido, dni, provincia, 
        departamento, barrio, calle, numeracion, caso) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
        (nombre,apellido,dni,provincia,departamento,barrio,calle,numeracion,caso))
        
        mysql.connection.commit()
        return redirect(url_for('view_sicks'))

@app.route("/add_contact",methods= ["GET", "POST"])
def add_contact():
    if request.method =="POST":
        nombre= request.form["nombre"]
        apellido= request.form["apellido"]
        dni= request.form["dni"]
        contraseña= request.form["contraseña"]
        email= request.form["email"]

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuarios (nombre, apellido, dni, contraseña ,email)VALUES(%s,%s,%s,%s,%s)",
        (nombre, apellido, dni, contraseña, email))
        mysql.connection.commit()
    return redirect(url_for("register"))


#----Grafico----#
@app.route('/grafico')
def grafico():
    cur = mysql.connection.cursor()
    cur.execute('SELECT caso, COUNT(*) FROM enfermos GROUP BY caso')
    data = cur.fetchall()
    #imprimir los datos de la bd
    print(data)
    
    labels = [row['caso'] for row in data]
    values = [row['COUNT(*)'] for row in data]
    
    return render_template('graph.html', labels=labels, values=values)


if __name__ == '__main__':
    app.run(port = 5000, debug = True)