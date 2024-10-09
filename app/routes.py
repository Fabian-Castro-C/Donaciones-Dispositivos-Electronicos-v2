from flask import render_template, request, jsonify
from app import app
from app.db_service import obtener_regiones, obtener_conexion
from app.validations import get_contact, get_deviceEntry, validate_contact, validate_deviceEntry

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/agregar_donacion', methods=['GET', 'POST'])
def agregar_donacion():
    regiones = obtener_regiones()
    if request.method == 'POST':
        # Obtenemos los datos de contacto
        contacto = get_contact()

        # Validamos los datos de contacto
        errores = validate_contact(
            contacto['name'], 
            contacto['email'], 
            contacto['phone'], 
            contacto['region'], 
            contacto['comuna']
        )

        # Obtenemos los datos de los dispositivos
        index = 0
        dispositivos = []
        while True:
            # Tratamos de obtener el nombre del dispositivo a partir del índice
            nombre_dispositivo = request.form.get(f'dispositivos[{index}][nombreDispositivo]')

            if not nombre_dispositivo:
                break # Si no hay nombre de dispositivo, salimos del ciclo

            # Obtenemos los datos del dispositivo
            dispositivo = get_deviceEntry(index)
            errores_device = validate_deviceEntry(
                dispositivo['nombreDispositivo'],
                dispositivo['descripcion'],
                dispositivo['tipo'],
                dispositivo['aniosUso'],
                dispositivo['estado'],
                dispositivo['fotos'],
                index
            )

            # Si hay errores en el dispositivo, los agregamos a la lista de errores
            if errores_device:
                errores.extend(errores_device)
            
            # Agregamos el dispositivo a la lista de dispositivos
            dispositivos.append(dispositivo)
            index += 1
        pass

        if errores:
            return jsonify({'status': 'error', 'errores': errores})
    
        # Si no hay errores, guardamos la donación en la base de datos
        # insertar_donacion(contacto, dispositivos)
        return jsonify({'status': 'success', 'message': 'Donación registrada exitosamente.'})
    
    if request.method == 'GET':
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