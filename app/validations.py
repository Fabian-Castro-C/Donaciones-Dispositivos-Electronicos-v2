from flask import request

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
    # TODO Implementar validacion del dispositivo
    print(name_device)
    return

def validate_email(email):
    # TODO Implementar validacion del email
    return

def validate_phone(phone):
    # TODO Implementar validacion del telefono
    return

def validate_region(region):
    # TODO Implementar validacion de la region
    return

def validate_comuna(comuna):
    # TODO Implementar validacion de la comuna
    return

