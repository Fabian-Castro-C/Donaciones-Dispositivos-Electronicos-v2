from flask import render_template, request
from app import app
from app.db_service import *

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/agregar_donacion', methods=['GET', 'POST'])
def agregar_donacion():
    regiones = obtener_regiones()
    if request.method == 'POST':
        # Lógica de manejo de formulario aquí
        pass
    return render_template('agregar-donacion.html', regiones=regiones)

@app.route('/ver_dispositivos')
def ver_dispositivos():
    return print('ver-dispositivos')