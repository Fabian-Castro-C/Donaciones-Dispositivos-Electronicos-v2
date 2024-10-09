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
        # TODO implementar la lógica para guardar la donación
        print('Validar datos')
        pass
    return render_template('agregar-donacion.html', regiones=regiones)

@app.route('/get_comunas/<int:region_id>')
def get_comunas(region_id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = "SELECT id, nombre FROM comuna WHERE region_id = %s ORDER BY nombre ASC"
            cursor.execute(sql, (region_id,)) # Evita SQL Injection
            comunas = cursor.fetchall()
        return {'comunas': comunas}
    except Exception as e:
        print(f"Error al obtener las comunas: {e}")
        return {'error': 'No se pudieron cargar las comunas.'}
    finally:
        conexion.close()


@app.route('/ver_dispositivos')
def ver_dispositivos():
    return print('ver-dispositivos')