import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'boxfit_mm_secret_2024')

# Configuración de DB: Railway (Postgres) o Local (SQLite)
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL or 'sqlite:///boxfit.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# MODELOS REQUERIDOS
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))
    rol = db.Column(db.String(20)) # admin / operador

class Alumno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    dni = db.Column(db.String(20), unique=True)
    vencimiento = db.Column(db.Date)
    categoria = db.Column(db.String(50)) # Boxeo / Funcional

class Movimiento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(10)) # ingreso / egreso
    descripcion = db.Column(db.String(200))
    monto = db.Column(db.Float)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def home():
    return "<h1>Boxfit_by_MM - Sistema en Linea</h1><p>Plataforma de Administracion Activa.</p>"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
