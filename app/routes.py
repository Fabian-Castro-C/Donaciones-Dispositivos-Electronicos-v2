from flask import render_template, request, jsonify, abort
from app import app
from app.db_service import obtener_regiones, obtener_conexion, insertar_donacion
from app.validations import get_contact, get_deviceEntry, validate_contact, validate_deviceEntry
from datetime import datetime, timedelta

@app.route('/', methods=['GET'])
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
        insertar_donacion(contacto, dispositivos)
        return jsonify({'status': 'success', 'message': 'Donación registrada exitosamente.'})
    
    if request.method == 'GET':
        return render_template('agregar-donacion.html', regiones=regiones)

@app.route('/get_comunas/<int:region_id>', methods=['GET'])
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

@app.route('/ver_dispositivos', methods=['GET'])
def ver_dispositivos():
    page = request.args.get('page', 1, type=int)
    per_page = 5  # Número de dispositivos por página
    offset = (page - 1) * per_page

    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        # Obtener el número total de dispositivos
        sql = "SELECT COUNT(*) AS total FROM dispositivo"
        cursor.execute(sql)
        total_dispositivos = cursor.fetchone()['total']

        # Calcular el número total de páginas
        total_pages = (total_dispositivos + per_page - 1) // per_page  # Redondeo hacia arriba

        # Verificar si la página solicitada es válida
        if page > total_pages or page < 1:
            # Redirigir a la última página si la página es demasiado grande
            return abort(404)

        # Consulta para obtener dispositivos y una sola imagen (la primera) con paginación
        dispositivos_query = """
            SELECT
                d.id,
                d.tipo,
                d.nombre AS nombre_dispositivo,
                d.estado,
                c.nombre AS nombre_comuna,
                a.ruta_archivo,
                a.nombre_archivo
            FROM dispositivo d
            JOIN contacto ct ON d.contacto_id = ct.id
            JOIN comuna c ON ct.comuna_id = c.id
            LEFT JOIN (
                SELECT dispositivo_id, ruta_archivo, nombre_archivo
                FROM archivo
                WHERE id IN (
                    SELECT MIN(id)
                    FROM archivo
                    GROUP BY dispositivo_id
                )
            ) a ON d.id = a.dispositivo_id
            ORDER BY d.id
            LIMIT %s OFFSET %s;
        """
        cursor.execute(dispositivos_query, (per_page, offset))
        dispositivos = cursor.fetchall()

        # Verificar si hay más dispositivos después de la página actual
        has_next = page < total_pages

    return render_template('ver-dispositivos.html', dispositivos=dispositivos, page=page, has_next=has_next)

@app.route('/informacion_dispositivo/<int:dispositivo_id>')
def informacion_dispositivo(dispositivo_id):
    conexion = obtener_conexion()
    comentarios_iniciales = 4  # Número de comentarios a cargar inicialmente

    try:
        with conexion.cursor() as cursor:
            # Consulta para obtener la información del dispositivo
            dispositivo_query = """
                SELECT d.id, d.nombre, d.descripcion, d.tipo, d.anos_uso, d.estado, 
                       c.nombre AS nombre_donante, c.email, c.celular, comuna.nombre AS comuna, 
                       region.nombre AS region 
                FROM dispositivo d
                JOIN contacto c ON d.contacto_id = c.id
                JOIN comuna ON c.comuna_id = comuna.id
                JOIN region ON comuna.region_id = region.id
                WHERE d.id = %s
            """
            cursor.execute(dispositivo_query, (dispositivo_id,))
            dispositivo = cursor.fetchone()

            # Consulta para obtener las fotos del dispositivo
            fotos_query = "SELECT ruta_archivo, nombre_archivo FROM archivo WHERE dispositivo_id = %s"
            cursor.execute(fotos_query, (dispositivo_id,))
            fotos = cursor.fetchall()

            # Consulta para obtener los primeros 4 comentarios
            comentarios_query = """
                SELECT nombre, texto, fecha 
                FROM comentario 
                WHERE dispositivo_id = %s 
                ORDER BY fecha DESC
                LIMIT %s
            """
            cursor.execute(comentarios_query, (dispositivo_id, comentarios_iniciales))
            comentarios = cursor.fetchall()

    except Exception as e:
        print(f"Error al obtener la información del dispositivo: {e}")
        return "Error al obtener la información del dispositivo", 500
    
    finally:
        conexion.close()

    # Verificamos si existe el dispositivo
    if not dispositivo:
        return abort(404)
    
    # Renderizamos la página con la información del dispositivo y los primeros 4 comentarios
    return render_template('informacion-dispositivo.html', 
                           dispositivo=dispositivo, 
                           fotos=fotos, 
                           comentarios=comentarios)

@app.route('/get_comments/<int:dispositivo_id>/<int:page>', methods=['GET'])
def get_comments(dispositivo_id, page):
    conexion = obtener_conexion()
    comments_per_page = 4  # Número de comentarios por página
    offset = (page - 1) * comments_per_page

    try:
        with conexion.cursor() as cursor:
            # Consulta paginada para obtener los comentarios
            comentarios_query = """
                SELECT nombre, texto, fecha 
                FROM comentario 
                WHERE dispositivo_id = %s 
                ORDER BY fecha DESC
                LIMIT %s OFFSET %s
            """
            cursor.execute(comentarios_query, (dispositivo_id, comments_per_page, offset))
            comentarios = cursor.fetchall()
    except Exception as e:
        print(f"Error al obtener los comentarios: {e}")
        return jsonify({'status': 'error', 'message': 'Error al obtener los comentarios.'}), 500
    finally:
        conexion.close()

    return jsonify({'status': 'success', 'comentarios': comentarios})

@app.route('/add_comment', methods=['POST'])
def add_comment():
    data = request.get_json()
    errors = []

    MAX_LENGTH_COMMENTS = 300
    MIN_LENGTH_COMMENTS = 5
    COMMENT_LIMIT_INTERVAL = timedelta(seconds=30)
    MAX_LENGTH_USERNAME = 80
    MIN_LENGTH_USERNAME = 3

    # Obtenemos y validamos los datos del comentario
    nombre = data.get('nombre', '').strip()
    texto = data.get('texto', '').strip()
    dispositivo_id = data.get('dispositivo_id')

    # Validaciones de longitud
    if not (3 <= len(nombre) <= 80):
        errors.append({"campo": "commenterName", "message": "El nombre debe tener entre 3 y 80 caracteres."})
    if not (5 <= len(texto) <= 300):
        errors.append({"campo": "commentText", "message": "El comentario debe tener entre 5 y 300 caracteres."})
    if not dispositivo_id:
        errors.append({"campo": "commentForm", "message": "ID de dispositivo inválido."})

    # Si hay errores, los devolvemos
    if errors:
        return jsonify({'status': 'error', 'errors': errors}), 400

    # Verificar frecuencia de comentarios (prevenir spam)
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            # Comprobamos la fecha del último comentario del mismo nombre y dispositivo
            cursor.execute(
                "SELECT fecha FROM comentario WHERE nombre = %s AND dispositivo_id = %s ORDER BY fecha DESC LIMIT 1",
                (nombre, dispositivo_id)
            )

            # Si existe un comentario anterior, verificamos el tiempo transcurrido
            last_comment = cursor.fetchone()
            if last_comment:
                last_comment_time = last_comment['fecha']
                if datetime.now() - last_comment_time < COMMENT_LIMIT_INTERVAL:
                    errors.append({"campo": "commentForm", "message": "Por favor, espere antes de agregar otro comentario."})
            
            # Si se detecta spam, devolvemos un error
            if errors:
                return jsonify({'status': 'error', 'errors': errors}), 429

            # Insertar el nuevo comentario en la base de datos
            cursor.execute(
                "INSERT INTO comentario (nombre, texto, fecha, dispositivo_id) VALUES (%s, %s, NOW(), %s)",
                (nombre, texto, dispositivo_id)
            )
            conexion.commit()
    except Exception as e:
        conexion.rollback()
        print(f"Error al insertar el comentario: {e}")
        return jsonify({'status': 'error', 'message': 'Error al insertar el comentario en la base de datos.'}), 500
    finally:
        conexion.close()

    return jsonify({'status': 'success', 'message': 'Comentario agregado exitosamente.'}), 201