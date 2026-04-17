import datetime

from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL

app = Flask(__name__,
            template_folder='../frontend/templates',
            static_folder='../frontend/static')

app.secret_key = "barberslot_secret"

# MYSQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'barberslot'
app.config['MYSQL_PORT'] = 3307

mysql = MySQL(app)

# 🏠 HOME
@app.route('/')
def home():
    return render_template('home.html')

# 📝 REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuarios(nombre, correo, password) VALUES (%s,%s,%s)",
                    (nombre, correo, password))
        mysql.connection.commit()
        cur.close()

        return redirect('/login')

    return render_template('register.html')

# 🔐 LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT id, nombre, rol FROM usuarios WHERE correo=%s AND password=%s",
                    (correo, password))

        user = cur.fetchone()
        cur.close()

        if user:
            session['user_id'] = user[0]
            session['user'] = user[1]
            session['rol'] = user[2]

            if user[2] == 'admin':
                return redirect('/admin')
            return redirect('/dashboard')

    return render_template('login.html')

# 👤 DASHBOARD CLIENTE
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', user=session['user'])

# 📅 RESERVAR
@app.route('/reservas', methods=['GET', 'POST'])
def reservas():
    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM servicios")
    servicios = cur.fetchall()

    cur.execute("SELECT * FROM barberos")
    barberos = cur.fetchall()

    if request.method == 'POST':
        fecha = request.form['fecha']  # yyyy-mm-dd
        hora = request.form['hora']
        servicio_id = request.form['servicio']
        barbero_id = request.form['barbero']

        # 🔥 CONVERTIR FECHA → DÍA
        fecha_obj = datetime.datetime.strptime(fecha, "%Y-%m-%d")
        dias = ["Lunes","Martes","Miercoles","Jueves","Viernes","Sabado","Domingo"]
        dia = dias[fecha_obj.weekday()]

        # 🔥 VALIDAR HORARIO (AHORA SÍ BIEN)
        cur.execute("""
            SELECT * FROM horarios
            WHERE barbero_id=%s
            AND LOWER(dia) = LOWER(%s)
            AND hora_inicio <= %s
            AND hora_fin >= %s
        """, (barbero_id, dia, hora, hora))

        horario = cur.fetchone()

        if not horario:
            return f"No hay horario disponible para {dia}"

        # 🔥 CREAR CITA
        cur.execute("""
            INSERT INTO citas (fecha, hora, servicio, usuario_id)
            VALUES (%s,%s,%s,%s)
        """, (fecha, hora, servicio_id, session['user_id']))

        cita_id = cur.lastrowid

        # 🔥 PRECIO
        cur.execute("SELECT precio FROM servicios WHERE id=%s", (servicio_id,))
        precio = cur.fetchone()[0]

        # 🔥 PAGO
        cur.execute("""
            INSERT INTO pagos (cita_id, monto, metodo, estado)
            VALUES (%s, %s, %s, %s)
        """, (cita_id, precio, 'Efectivo', 'Pendiente'))

        mysql.connection.commit()
        cur.close()

        return redirect('/mis_citas')

    return render_template('dashboard_reservas.html',
                           servicios=servicios,
                           barberos=barberos)


# 📋 MIS CITAS
@app.route('/mis_citas')
def mis_citas():
    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT c.fecha, c.hora, s.nombre, 'Pendiente'
        FROM citas c
        JOIN servicios s ON c.servicio = s.id
        WHERE c.usuario_id = %s
    """, (session['user_id'],))

    datos = cur.fetchall()
    cur.close()

    citas = []
    for d in datos:
        citas.append({
            'fecha': d[0],
            'hora': d[1],
            'servicio': d[2],  # 👈 ahora sí nombre
            'estado': d[3]
        })

    return render_template('dashboard_mis_citas.html', citas=citas)

# 🛠 ADMIN DASHBOARD
@app.route('/admin')
def admin():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT u.nombre, c.fecha, c.hora, s.nombre, p.monto, p.estado
        FROM citas c
        JOIN usuarios u ON c.usuario_id = u.id
        JOIN servicios s ON c.servicio = s.id
        JOIN pagos p ON p.cita_id = c.id
        """)
    citas = cur.fetchall()
    cur.close()

    return render_template('admin_dashboard.html', citas=citas)

# 💈 ADMIN BARBEROS
@app.route('/admin/barberos', methods=['GET','POST'])
def admin_barberos():
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']

        cur.execute("INSERT INTO barberos(nombre, telefono) VALUES (%s,%s)",
                    (nombre, telefono))
        mysql.connection.commit()

    cur.execute("SELECT * FROM barberos")
    barberos = cur.fetchall()

    return render_template('admin_barberos.html', barberos=barberos)

# ✂️ ADMIN SERVICIOS
@app.route('/admin/servicios', methods=['GET','POST'])
def admin_servicios():
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']

        cur.execute("INSERT INTO servicios(nombre, precio) VALUES (%s,%s)",
                    (nombre, precio))
        mysql.connection.commit()

    cur.execute("SELECT * FROM servicios")
    servicios = cur.fetchall()

    return render_template('admin_servicios.html', servicios=servicios)

# ⏰ ADMIN HORARIOS
@app.route('/admin/horarios', methods=['GET','POST'])
def admin_horarios():
    cur = mysql.connection.cursor()

    # traer barberos
    cur.execute("SELECT * FROM barberos")
    barberos = cur.fetchall()

    if request.method == 'POST':
        barbero_id = request.form['barbero']
        dia = request.form['dia']
        hora_inicio = request.form['hora_inicio']
        hora_fin = request.form['hora_fin']

        cur.execute("""
            INSERT INTO horarios (barbero_id, dia, hora_inicio, hora_fin)
            VALUES (%s,%s,%s,%s)
        """, (barbero_id, dia, hora_inicio, hora_fin))

        mysql.connection.commit()

    # mostrar horarios
    cur.execute("""
        SELECT h.id, b.nombre, h.dia, h.hora_inicio, h.hora_fin
        FROM horarios h
        JOIN barberos b ON h.barbero_id = b.id
    """)
    horarios = cur.fetchall()

    return render_template('admin_horarios.html',
                           horarios=horarios,
                           barberos=barberos)

# 🚪 LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

