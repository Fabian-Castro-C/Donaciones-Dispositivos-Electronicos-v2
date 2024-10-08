from flask import render_template
from app import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/agregar_donacion')
def agregar_donacion():
    return print('Agregar donacion')

@app.route('/ver_dispositivos')
def ver_dispositivos():
    return print('ver_dispositivos')