import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'boxfit_mm_2026_security')

# Configuración DB: Soporta SQLite local y Postgres en Railway
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL or 'sqlite:///boxfit.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# MODELOS
class Alumno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=False)
    vencimiento = db.Column(db.Date, nullable=False)
    tipo_clase = db.Column(db.String(50)) # Boxeo o Funcional

class Venta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(100)) # Bebidas, Equipamiento
    monto = db.Column(db.Float)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def home():
    return "<h1>Boxfit_by_MM</h1><p>Sistema de gestion de Boxeo y Funcional activo.</p>"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
