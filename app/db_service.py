import pymysql, os
from app.config import Config
from werkzeug.utils import secure_filename
from flask import current_app
from datetime import datetime

def obtener_conexion():
    """Crea y devuelve una conexión a la base de datos."""
    return pymysql.connect(
        host=Config.MYSQL_HOST,
        port=Config.MYSQL_PORT,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB,
        cursorclass=pymysql.cursors.DictCursor
    )

def obtener_regiones():
    """Obtiene todas las regiones de la base de datos."""
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = "SELECT id, nombre FROM region ORDER BY id ASC"
            cursor.execute(sql)
            regiones = cursor.fetchall()
        return regiones
    except Exception as e:
        print(f"Error al obtener las regiones: {e}")
        return []
    finally:
        conexion.close()

def insertar_donacion(contacto, dispositivos):
    """
    Inserta una donación en la base de datos.

    :param contacto: Diccionario con los datos del contacto.
    :param dispositivos: Lista de diccionarios, cada uno con los datos de un dispositivo y sus archivos.
    """
    conexion = obtener_conexion()
    try:
        cursor = conexion.cursor()
        conexion.autocommit(False)  # Desactivar autocommit

        # Iniciar una transacción
        conexion.begin()

        # Obtener la fecha actual
        fecha_creacion = datetime.now()

        # Insertar el contacto y obtener su ID
        sql_contacto = """
            INSERT INTO contacto (nombre, email, celular, comuna_id, fecha_creacion)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql_contacto, (
            contacto['name'],
            contacto['email'],
            contacto['phone'],
            contacto['comuna'],
            fecha_creacion
        ))
        contacto_id = cursor.lastrowid  # Obtener el ID del contacto insertado

        # Iterar sobre los dispositivos
        for dispositivo in dispositivos:
            # Insertar el dispositivo y obtener su ID
            sql_dispositivo = """
                INSERT INTO dispositivo (contacto_id, nombre, descripcion, tipo, anos_uso, estado)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql_dispositivo, (
                contacto_id,
                dispositivo['nombreDispositivo'],
                dispositivo['descripcion'],
                dispositivo['tipo'],
                dispositivo['aniosUso'],
                dispositivo['estado']
            ))
            dispositivo_id = cursor.lastrowid  # Obtener el ID del dispositivo insertado

            # Manejar los archivos asociados al dispositivo
            archivos = dispositivo['fotos']
            for archivo in archivos:
                # Guardar el archivo en el servidor
                ruta_archivo, nombre_archivo = guardar_archivo(archivo, dispositivo_id)
                # Insertar registro en la tabla archivo
                sql_archivo = """
                    INSERT INTO archivo (ruta_archivo, nombre_archivo, dispositivo_id)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(sql_archivo, (
                    ruta_archivo,
                    nombre_archivo,
                    dispositivo_id
                ))

        # Confirmar la transacción
        conexion.commit()
    except Exception as e:
        # En caso de error, deshacer la transacción
        conexion.rollback()
        print(f"Error al insertar la donación: {e}")
        raise e  # Opcional: propagar la excepción para manejo externo
    finally:
        cursor.close()
        conexion.close()
    

def guardar_archivo(archivo, dispositivo_id):
    """
    Guarda un archivo en el servidor y devuelve la ruta y el nombre del archivo.

    :param archivo: Objeto FileStorage de Flask (archivo subido).
    :param dispositivo_id: ID del dispositivo al que pertenece el archivo.
    :return: Tupla (ruta_relativa, nombre_archivo)
    """
    # Directorio base de subida de archivos
    UPLOAD_FOLDER = os.path.join(current_app.root_path, 'static', 'uploads', f'dispositivo_{dispositivo_id}')
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Crear el directorio si no existe

    # Asegurar un nombre de archivo seguro
    nombre_archivo = secure_filename(archivo.filename)

    # Ruta completa del archivo
    ruta_archivo = os.path.join(UPLOAD_FOLDER, nombre_archivo)

    # Guardar el archivo en el servidor
    archivo.save(ruta_archivo)

    # Devolver la ruta relativa desde 'static'
    ruta_relativa = os.path.join('uploads', f'dispositivo_{dispositivo_id}', nombre_archivo)
    return ruta_relativa, nombre_archivo
