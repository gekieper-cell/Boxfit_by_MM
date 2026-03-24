import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, timedelta

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'boxfit_pro_key_2026')

# Configuración de Base de Datos
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL or 'sqlite:///boxfit.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- MODELOS ---
class Alumno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    dni = db.Column(db.String(20), unique=True)
    plan_id = db.Column(db.Integer)
    vencimiento = db.Column(db.Date)

class Movimiento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(10)) # ingreso/egreso
    monto = db.Column(db.Float)
    fecha = db.Column(db.Date, default=date.today)

# --- RUTAS DE NAVEGACIÓN ---
@app.route('/')
def home():
    if 'user' not in session: return redirect(url_for('login_page'))
    return render_template('index.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

# --- API (Lo que el HTML necesita para mostrar datos) ---
@app.route('/api/stats')
def get_stats():
    # Esto llena los gráficos y contadores del index.html
    return jsonify({
        "alumnos_activos": Alumno.query.count(),
        "morosos": Alumno.query.filter(Alumno.vencimiento < date.today()).count(),
        "ingresos_mes": [12000, 15000, 18000, 22000, 19000, 25000], # Datos para el gráfico
        "labels_mes": ["Ene", "Feb", "Mar", "Abr", "May", "Jun"]
    })

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    if data.get('user') == 'admin' and data.get('pass') == 'admin123': # Cambia esto luego
        session['user'] = 'admin'
        return jsonify({"ok": True})
    return jsonify({"ok": False, "msg": "Usuario o clave incorrectos"}), 401

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)