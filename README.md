# Donaciones de Dispositivos Electrónicos

**Autor:** Fabián Castro Contreras

### Descripción

Este proyecto es una aplicación web que permite la gestión de donaciones de dispositivos electrónicos, implementado como parte de la **Tarea 2** del ramo **Desarrollo y Aplicaciones Web**. El sistema permite agregar donaciones de dispositivos, visualizar las donaciones registradas, y mostrar información detallada de los dispositivos donados. El proyecto se desarrolla en **Flask**, con validaciones tanto del lado del cliente (JavaScript) como del servidor. Además, se incluye un manejo seguro de archivos y consultas a la base de datos.

---

### Estructura del Proyecto

```
/Donaciones-Dispositivos-Electronicos
│
├── app
│   ├── __init__.py          # Inicialización de la aplicación Flask
│   ├── routes.py            # Rutas principales de la aplicación
│   ├── config.py            # Configuración del acceso a la base de datos
│   ├── db_service.py        # Servicios para manejo de la base de datos
│   ├── validations.py       # Validaciones de los formularios en el servidor
│   └── templates/           # Plantillas HTML dinámicas usando Jinja
│
├── static
│   ├── css/                 # Archivos CSS para el estilo del sitio
│   │   ├── agregar-donacion.css
│   │   ├── index.css
│   │   ├── informacion-dispositivo.css
│   │   └── ver-dispositivos.css
│   ├── js/                  # Archivos JavaScript para la interacción cliente
│   │   ├── donationForm.js
│   │   └── infoDevice.js
│   └── uploads/             # Directorio donde se almacenan las imágenes subidas
│
├── sql                      # Esquemas y scripts SQL de la base de datos
├── venv                     # Entorno virtual con dependencias de Python
├── .gitignore                # Archivos y directorios ignorados por Git
├── app.py                   # Archivo principal para ejecutar la aplicación Flask
├── README.md                # Documento de referencia para el proyecto
└── requirements.txt         # Dependencias del proyecto
```

---

### Creación de la Base de Datos

La base de datos fue creada siguiendo las siguientes instrucciones:

```sql
CREATE DATABASE tarea2;
USE tarea2; 
```

Las tablas fueron creadas usando:

```sql
SOURCE ubicacion_proyecto/sql/tarea2.sql;
SOURCE ubicacion_proyecto/sql/region-comuna.sql;
```

---

### Configuración del Proyecto Flask

Se creó un usuario en el sistema operativo específicamente para ser usado en el proyecto.

```python
class Config:
    MYSQL_HOST = 'localhost'
    MYSQL_PORT = 3306 # Puerto de MySQL
    MYSQL_USER = 'fabiancastro' # Usuario creado
    MYSQL_PASSWORD = 'oiAc66zUgSvgIM9KiEbV' # Contraseña del usuario
    MYSQL_DB = 'tarea2' # Nombre de la base de datos
    MYSQL_CURSORCLASS = 'DictCursor' # Solicitamos que las respuestas sean en forma de diccionario
```

---

### Instalación

1. **Clona el repositorio** en tu máquina local:

   ```bash
   git clone https://github.com/usuario/proyecto-donaciones.git
   cd proyecto-donaciones
   ```

2. **Crea un entorno virtual** e instala las dependencias del proyecto:

   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configura la base de datos MySQL**:

   - Asegúrate de configurar correctamente las credenciales de acceso en `config.py`.

   - Ejecuta los scripts SQL para crear las tablas necesarias:
     ```sql
     SOURCE ubicacion_proyecto/sql/tarea2.sql;
     SOURCE ubicacion_proyecto/sql/region-comuna.sql;
     ```

---

### Funcionalidades

#### Agregar Donaciones

El sistema permite agregar una donación de dispositivos a través de un formulario. Las validaciones son realizadas tanto en el lado del cliente como en el servidor.

- **Validaciones en el cliente**: 
  - Uso de JavaScript para validar la longitud de campos, tipos de dispositivos, estados, y número máximo de imágenes (3 por dispositivo).
  - Mensajes de error y éxito son mostrados dinámicamente en la interfaz del usuario.
  - Se asegura que los datos ingresados por el usuario sigan las restricciones indicadas antes de enviar el formulario.

- **Validaciones en el servidor**: 
  - Verificación de que los datos enviados cumplan con las reglas de negocio.
  - Las imágenes subidas son verificadas utilizando la biblioteca **filetype** para asegurarse de que solo se suben archivos de imagen.
  - Las entradas en los formularios son sanitizadas para evitar inyecciones SQL.
  - Si hay errores, se muestran en el front para que el usuario corrija los errores.

- **Almacenamiento de archivos**: 
  - Las imágenes se almacenan en una estructura organizada en subcarpetas basadas en el ID del dispositivo.
  - Los nombres de los archivos se generan mediante un hash basado en los primeros 8 KB del archivo para evitar conflictos y mejorar la seguridad.
  - Se crean diferentes resoluciones de las imágenes cargadas con el formato `hash_resolucion.extension`.

#### Ver Dispositivos

- Los dispositivos donados se muestran en una tabla paginada (5 dispositivos por página), con navegación entre páginas.
- Cada fila de la tabla se enlaza a una página detallada que muestra información completa del dispositivo.

#### Información Detallada del Dispositivo

- En esta vista se muestran los detalles completos de cada dispositivo, incluyendo:
  - **Nombre del dispositivo**
  - **Descripción**
  - **Años de uso**
  - **Estado**
  - **Imágenes** (que se pueden expandir)
- Se muestra también la información del donante, como el nombre, correo electrónico y región.

---

### Seguridad

Se implementaron varias consideraciones de seguridad en la aplicación:

1. **Validación de archivos**: Las imágenes subidas son validadas usando la biblioteca **filetype** para asegurarse de que solo se acepten archivos válidos.
   
2. **Nombres de archivos**: Los nombres de los archivos se generan como hashes, lo que asegura que los nombres sean únicos y no revelen información sensible.

3. **Sanitización de entradas**: Todas las entradas de los formularios son limpiadas antes de ser usadas en consultas SQL para prevenir ataques de inyección SQL.

4. **Paginación segura**: Se valida que las páginas solicitadas en la vista de dispositivos existan, y en caso de un número de página fuera de rango, se lanza un error 404.

---

### Estilos y Usabilidad

1. **Información del dispositivo**: Se mejoraron los estilos en la página de detalle del dispositivo, mejorando la visualización y haciéndola más atractiva y clara para el usuario.

2. **Estilo de paginación**: Los botones de paginación fueron diseñados de forma clara, mostrando cuándo una página no está disponible (deshabilitada) y resaltando la página actual.

---

### Consideraciones Adicionales

- **Comentarios**: Aunque se incluyeron en la interfaz, los comentarios aún no se manejan en el servidor en esta versión del proyecto por indicaciones de la tarea. Actualmente, son gestionados en el cliente usando JavaScript, sin persistencia en la base de datos.
