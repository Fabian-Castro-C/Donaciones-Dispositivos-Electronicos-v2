from app.db_service import obtener_conexion
from flask import request
import re

def get_contact():
    """Obtiene los datos del contacto desde el formulario"""
    name = request.form.get('nombre')
    email = request.form.get('email')
    phone = request.form.get('telefono')
    region = request.form.get('region')
    comuna = request.form.get('comuna')

    return {
        'name': name,
        'email': email,
        'phone': phone,
        'region': region,
        'comuna': comuna
    }

def get_deviceEntry(index):
    """Obtiene los datos del dispositivo desde el formulario"""
    name_device = request.form.get(f'dispositivos[{index}][nombreDispositivo]')
    description = request.form.get(f'dispositivos[{index}][descripcion]')
    type_device = request.form.get(f'dispositivos[{index}][tipo]')
    years = request.form.get(f'dispositivos[{index}][aniosUso]')
    status = request.form.get(f'dispositivos[{index}][estado]')
    files = request.files.getlist(f'dispositivos[{index}][fotos]')

    return {
        'nombreDispositivo': name_device,
        'descripcion': description,
        'tipo': type_device,
        'aniosUso': years,
        'estado': status,
        'fotos': files
    }

def validate_contact(name, email, phone, region, comuna):
    """Valida los datos del contacto y devuelve la lista de errores"""
    errores = []

    # Validar nombre
    if not name or len(name) < 3 or len(name) > 80:
        errores.append({
            'campo': 'nombre',
            'mensaje':'El nombre del donante debe tener entre 3 y 80 caracteres.'
        })
    
    # Validar email
    if not validate_email(email):
        errores.append({
            'campo': 'email',
            'mensaje': 'El email del donante no es válido.'
        })
    
    # Validar teléfono
    if phone and not validate_phone(phone):
        errores.append({
            'campo': 'telefono',
            'mensaje': 'El número de celular debe contener entre 10 y 15 dígitos y solo números.'
        })

    if not validate_region(region):
        errores.append({
            'campo': 'region',
            'mensaje': 'Por favor, selecciona una región.'
        })

    if not validate_comuna(comuna):
        errores.append({
            'campo': 'comuna',
            'mensaje': 'Por favor, selecciona una comuna.'
        })
    
    return errores

def validate_deviceEntry(name_device, description, type_device, years, status, files):
    """Valida los datos del dispositivo y devuelve la lista de errores"""
    errores = []

    # Validar nombre del dispositivo
    tipos_validos = ["Pantalla", "Notebook", "Tablet", "Celular", "Consola", "Mouse", "Teclado", "Impresora", "Parlante", "Audifonos", "Otro"]
    if type_device not in tipos_validos:
        errores.append({
            'campo': 'tipo',
            'mensaje': 'El nombre del dispositivo debe tener entre 3 y 80 caracteres.'
        })

    # Validar descripción
    if description and len(description) > 300:
        errores.append({
            'campo': 'descripcion',
            'mensaje': 'La descripción del dispositivo debe tener máximo 300 caracteres.'
        })

    # Validar años de uso
    if not (years.isdigit() and 0 <= int(years)):
        errores.append({
            'campo': 'aniosUso',
            'mensaje': 'Por favor, introduce un número válido de años de uso.'
        })

    # Validar estado de funcionamiento
    estados_validos = ["Funciona perfecto", "Funciona a medias", "No funciona"]
    if status not in estados_validos:
        errores.append({
            'campo': 'estado',
            'mensaje': 'Por favor, selecciona el estado del dispositivo.'
        })

    # Validar fotos
    if validate_files(files):
        errores.append({
            'campo': 'fotos',
            'mensaje': 'Puedes subir un máximo de 3 imágenes.'
        })

    return

def validate_email(email):
    """Valida el email del contacto"""
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

def validate_phone(phone):
    """Valida el número de teléfono del contacto"""
    phone_regex = r'^\d{10,15}$'
    return re.match(phone_regex, phone) is not None

def validate_region(region):
    """Valida la region comparando con la base de datos"""
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = "SELECT nombre FROM region"
            cursor.execute(sql)
            for row in cursor.fetchall():
                if region == row['nombre']:
                    return True
                else:
                    return False
    except Exception as e:
        print(f"Error al obtener las regiones: {e}")
        return False

def validate_comuna(comuna, region):
    """Valida la comuna comparando con la base de datos"""
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = """
                SELECT comuna.nombre
                FROM comuna
                JOIN region ON comuna.region_id = region.id
                WHERE region.nombre = %s
            """
            cursor.execute(sql, (region,))
            for row in cursor.fetchall():
                if comuna == row['nombre']:
                    return True
                else:
                    return False
    except Exception as e:
        print(f"Error al obtener las comunas: {e}")
        return False
    
def validate_files(files):
    # TODO implementar validación de archivos
    return False