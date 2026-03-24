import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'boxfit_mm_PRO_2026')

# Base de Datos
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL or 'sqlite:///boxfit_pro.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- MODELOS PARA EL DISEÑO AVANZADO ---
class Alumno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    dni = db.Column(db.String(20), unique=True)
    plan_id = db.Column(db.Integer)
    vencimiento = db.Column(db.Date)
    ultimo_pago = db.Column(db.DateTime, default=datetime.utcnow)

class Plan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    precio = db.Column(db.Float)

# --- RUTAS ---
@app.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

# API para los gráficos y datos que pide tu index.html
@app.route('/api/stats')
def stats():
    return jsonify({
        "alumnos_activos": Alumno.query.count(),
        "ingresos_mes": 150500.0, # Ejemplo para el gráfico
        "morosos": 5
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)