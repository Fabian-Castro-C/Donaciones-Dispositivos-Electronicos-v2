import pymysql, os
from app.config import Config
from werkzeug.utils import secure_filename
from flask import current_app
from datetime import datetime
import hashlib
from PIL import Image


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
    """ Inserta una donación en la base de datos."""
    
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

def generar_hash_contenido(archivo):
    """Genera un hash SHA-256 del contenido del archivo."""
    hasher = hashlib.sha256()
    archivo.stream.seek(0)  # Asegurarse de que estamos al principio del archivo
    while True:
        chunk = archivo.stream.read(8192)
        if not chunk:
            break
        hasher.update(chunk)
    archivo_hash = hasher.hexdigest()
    archivo.stream.seek(0)  # Volver al inicio del archivo para poder usarlo luego
    return archivo_hash

def guardar_archivo(archivo, dispositivo_id):
    """ Guarda un archivo en el servidor y devuelve la ruta y el nombre original del archivo.
    Crea versiones redimensionadas de la imagen en tamaños 1280x1024, 640x480 y 120x120."""

    # Directorio base de subida de archivos
    UPLOAD_FOLDER = os.path.join(current_app.root_path, 'static', 'uploads', f'dispositivo_{dispositivo_id}')
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Crear el directorio si no existe

    # Asegurar un nombre de archivo seguro
    nombre_archivo_original = secure_filename(archivo.filename)

    # Obtener la extensión del archivo de manera segura
    _, extension = os.path.splitext(nombre_archivo_original)

    # Generar el hash del contenido del archivo para asegurar nombres únicos
    archivo_hash = generar_hash_contenido(archivo)

    # Crear un nombre de archivo basado en el hash del contenido
    base_filename = f"{archivo_hash}{extension}"

    # Ruta completa del archivo base (imagen original)
    ruta_base = os.path.join(UPLOAD_FOLDER, base_filename)

    # Leer el archivo en PIL Image
    try:
        image = Image.open(archivo.stream)
    except IOError:
        raise ValueError('El archivo subido no es una imagen válida')

    # Guardar la imagen original
    archivo.stream.seek(0)  # Volver al inicio para guardar el archivo original
    archivo.save(ruta_base)

    # Crear y guardar las imágenes redimensionadas
    tamanos = [(1280, 1024), (640, 480), (120, 120)]
    for ancho, alto in tamanos:
        # Calcular la relación de aspecto deseada
        aspect_ratio_desired = ancho / alto

        # Obtener las dimensiones actuales de la imagen
        ancho_original, alto_original = image.size
        aspect_ratio_original = ancho_original / alto_original

        # Determinar las dimensiones para el recorte
        if aspect_ratio_original > aspect_ratio_desired:
            # La imagen es más ancha que la relación de aspecto deseada
            nuevo_ancho = int(alto_original * aspect_ratio_desired)
            nuevo_alto = alto_original
            offset_x = int((ancho_original - nuevo_ancho) / 2)
            offset_y = 0
        else:
            # La imagen es más alta que la relación de aspecto deseada
            nuevo_ancho = ancho_original
            nuevo_alto = int(ancho_original / aspect_ratio_desired)
            offset_x = 0
            offset_y = int((alto_original - nuevo_alto) / 2)

        # Recortar la imagen al área calculada
        box = (offset_x, offset_y, offset_x + nuevo_ancho, offset_y + nuevo_alto)
        image_cropped = image.crop(box)

        # Redimensionar la imagen al tamaño deseado
        image_resized = image_cropped.resize((ancho, alto), Image.LANCZOS)

   # Guardar la imagen redimensionada
        size_suffix = f"_{ancho}x{alto}"
        filename_resized = base_filename.replace(extension, f"{size_suffix}{extension}")
        ruta_resized = os.path.join(UPLOAD_FOLDER, filename_resized)
        image_resized.save(ruta_resized)

    # Devolver la ruta relativa base (incluyendo la extensión), y el nombre de archivo original
    ruta_relativa_base = os.path.join('uploads', f'dispositivo_{dispositivo_id}', base_filename)
    return ruta_relativa_base, nombre_archivo_original