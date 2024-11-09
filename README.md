# Donaciones de Dispositivos Electrónicos

**Autor:** Fabián Castro Contreras

### Descripción

Este proyecto es una aplicación web que permite la gestión de donaciones de dispositivos electrónicos, implementado como parte de la **Tarea 3** del ramo **Desarrollo y Aplicaciones Web**. El sistema permite agregar donaciones de dispositivos, visualizar las donaciones registradas, y mostrar información detallada de los dispositivos donados. El proyecto se desarrolla en **Flask**, con validaciones tanto del lado del cliente (JavaScript) como del servidor. Además, se incluye un manejo seguro de archivos y consultas a la base de datos.

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
│   │   ├── infoDevice.js
│   │   └── index.js         # Nuevo archivo para manejar gráficos y estadísticas
│   └── uploads/             # Directorio donde se almacenan las imágenes subidas
│
├── sql                      # Esquemas y scripts SQL de la base de datos
├── venv                     # Entorno virtual con dependencias de Python
├── .gitignore               # Archivos y directorios ignorados por Git
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

#### Comentarios

Se ha implementado un sistema de comentarios para cada dispositivo donado, con las siguientes características:

- **Integración de Validaciones del Servidor**:
  - Se añadió un sistema de validaciones en el servidor para los comentarios, que verifica:
    - El nombre del comentarista tiene entre 3 y 80 caracteres.
    - El texto del comentario tiene entre 5 y 300 caracteres.
    - Se valida que el `dispositivo_id` sea válido.
  - Las respuestas del servidor incluyen mensajes de error detallados que el frontend puede manejar fácilmente.

- **Prevención de Spam**:
  - Se implementó una restricción de tiempo que previene que un mismo usuario publique comentarios demasiado rápido en un dispositivo (30 segundos entre comentarios).
  - Si un usuario intenta enviar un comentario dentro de este intervalo, se devuelve un código de estado `429 (Too Many Requests)`.

- **Carga Dinámica de Comentarios**:
  - Se añadió una funcionalidad para cargar comentarios de manera progresiva, mostrando los primeros 4 comentarios y cargando más en grupos de 4 al hacer clic en el botón "Mostrar más comentarios".
  - El botón "Mostrar más comentarios" se oculta automáticamente cuando no hay más comentarios que cargar.

#### Gráficos y Estadísticas

Se han integrado gráficos dinámicos en la aplicación para proporcionar información estadística relevante sobre las donaciones de dispositivos electrónicos.

- **Integración de Gráficos Dinámicos**:
  - Se añadieron gráficos en la página `index.html` que muestran información estadística relevante:
    - **Gráfico de Tipos de Dispositivos**: Representa la cantidad de dispositivos donados por tipo.
    - **Gráfico de Contactos por Comuna**: Muestra la distribución de contactos por comuna.
  - Los gráficos se generan utilizando la biblioteca **Highcharts** y se actualizan dinámicamente con datos obtenidos a través de AJAX.

- **Rutas Flask para Proveer Datos**:
  - Se añadieron dos nuevas rutas en `routes.py` que responden con datos JSON para alimentar los gráficos:
    - **`/datos_dispositivos`**: Devuelve la cantidad de dispositivos donados por tipo.
    - **`/datos_contactos`**: Devuelve la distribución de contactos por comuna.
  - Estas rutas realizan consultas a la base de datos y envían la información en un formato estructurado, adecuado para su uso con Highcharts.

- **Uso de AJAX con `fetch()` en el Frontend**:
  - Se implementó el uso de `fetch()` para realizar solicitudes AJAX desde `index.js` y obtener los datos necesarios de las nuevas rutas Flask.
  - El uso de `fetch()` permite que los gráficos se actualicen sin necesidad de recargar la página.

- **Optimización del Diseño con CSS**:
  - Se ajustaron los estilos CSS para asegurar que los gráficos se vean bien integrados en la página:
    - Bordes, sombras y esquinas redondeadas para darle un aspecto moderno.
    - Espaciado adicional en los encabezados y párrafos para una mejor presentación.

- **Mejora en la Experiencia del Usuario**:
  - La página `index.html` se ha actualizado para incluir las secciones de gráficos, ofreciendo información visual y fácil de interpretar sobre las donaciones.
  - El diseño se ha optimizado para asegurar una experiencia de usuario fluida y atractiva.

- **Descripción de las Rutas Flask Nuevas**:
  - **`/datos_dispositivos`**:
    - Realiza una consulta a la base de datos para contar la cantidad de dispositivos por tipo.
    - Responde con un objeto JSON que incluye el tipo de dispositivo y el total correspondiente.
  - **`/datos_contactos`**:
    - Realiza una consulta a la base de datos para contar la cantidad de contactos por comuna.
    - Responde con un objeto JSON que incluye la comuna y el total correspondiente.

---

### Seguridad

Se implementaron varias consideraciones de seguridad en la aplicación:

1. **Validación de archivos**: Las imágenes subidas son validadas usando la biblioteca **filetype** para asegurarse de que solo se acepten archivos válidos.
   
2. **Nombres de archivos**: Los nombres de los archivos se generan como hashes, lo que asegura que los nombres sean únicos y no revelen información sensible.

3. **Sanitización de entradas**: Todas las entradas de los formularios son limpiadas antes de ser usadas en consultas SQL para prevenir ataques de inyección SQL.

4. **Paginación segura**: Se valida que las páginas solicitadas en la vista de dispositivos existan, y en caso de un número de página fuera de rango, se lanza un error 404.

5. **Prevención de Spam en Comentarios**:
   - Restricción de tiempo entre publicaciones de comentarios para evitar el spam.
   - Respuestas adecuadas (`429 Too Many Requests`) cuando se excede el límite.

---

### Estilos y Usabilidad

1. **Información del dispositivo**: Se mejoraron los estilos en la página de detalle del dispositivo, mejorando la visualización y haciéndola más atractiva y clara para el usuario.

2. **Estilo de paginación**: Los botones de paginación fueron diseñados de forma clara, mostrando cuándo una página no está disponible (deshabilitada) y resaltando la página actual.

3. **Mejoras en el Diseño del Botón de Comentarios**:
   - El botón "Mostrar más comentarios" se estilizó para que tenga un diseño coherente con el botón del formulario de comentarios.
   - Se añadió un `margin-bottom` al botón para evitar que esté demasiado cerca del texto "Agregar Comentario".

4. **Optimización del Diseño de Gráficos**:
   - Los gráficos en la página `index.html` cuentan con bordes, sombras y esquinas redondeadas para un aspecto moderno.
   - Se añadió espaciado adicional en los encabezados y secciones de gráficos para una mejor presentación.

---

### Consideraciones Adicionales

- **Comentarios**: Aunque se incluyeron en la interfaz, los comentarios ahora son manejados de manera más robusta con validaciones en el servidor y prevención de spam.
---

### Instrucciones de Uso

- **Carga de Comentarios**: Los comentarios se cargan inicialmente en grupos de 4 y se pueden cargar más comentarios haciendo clic en el botón "Mostrar más comentarios".
- **Optimización de la Carga**: La carga progresiva mejora la experiencia del usuario al evitar la carga de todos los comentarios de una sola vez.
- **Visualización de Gráficos**: En la página principal (`index.html`), se muestran gráficos dinámicos que representan estadísticas sobre las donaciones de dispositivos y la distribución de contactos por comuna. Los gráficos se actualizan automáticamente sin necesidad de recargar la página.

---

### Actualización del Código JavaScript

Se realizaron las siguientes modificaciones en el código JavaScript para mejorar la funcionalidad de los comentarios y la integración de gráficos:

- **Envío de Comentarios**:
  - Se modificó el JavaScript para enviar comentarios al servidor usando `fetch` con solicitudes `POST`.
  - Se maneja la respuesta del servidor para mostrar mensajes de éxito o errores específicos en el formulario.
  - Se añadió un retraso de 1.5 segundos antes de recargar la página para dar tiempo al usuario de ver el mensaje de éxito.
  - Se obtiene el `device_id` directamente desde un atributo `data-device-id` en el formulario HTML, lo que simplifica el manejo de la información.

- **Carga Dinámica de Comentarios**:
  - Se agregó una función para cargar comentarios de forma dinámica en grupos de 4, haciendo uso de `fetch` para obtener más comentarios sin recargar la página.

- **Integración de Gráficos con AJAX**:
  - En el archivo `index.js`, se implementaron funciones para realizar solicitudes `fetch` a las nuevas rutas Flask (`/datos_dispositivos` y `/datos_contactos`) y obtener los datos necesarios para los gráficos.
  - Se inicializan los gráficos de Highcharts con los datos recibidos y se configuran para actualizarse dinámicamente según se obtengan nuevos datos.

---

### Actualización de la Ruta en Flask

Se realizaron las siguientes actualizaciones en las rutas de Flask para soportar la nueva funcionalidad de comentarios y gráficos:

- **Ruta `informacion_dispositivo`**:
  - Optimizada para cargar solo los primeros 4 comentarios inicialmente.

- **Nueva Ruta `/get_comments`**:
  - Creada para manejar la carga paginada de comentarios, permitiendo la carga de comentarios adicionales de manera eficiente.

- **Nuevas Rutas para Gráficos**:
  - **`/datos_dispositivos`**:
    - Realiza una consulta a la base de datos para contar la cantidad de dispositivos por tipo.
    - Responde con un objeto JSON que incluye el tipo de dispositivo y el total correspondiente.
  
  - **`/datos_contactos`**:
    - Realiza una consulta a la base de datos para contar la cantidad de contactos por comuna.
    - Responde con un objeto JSON que incluye la comuna y el total correspondiente.

Estas rutas permiten que los gráficos en el frontend se actualicen dinámicamente con información precisa y actualizada sobre las donaciones y los contactos.

---

Con estos cambios, la aplicación no solo gestiona las donaciones de dispositivos electrónicos de manera eficiente y segura, sino que también proporciona una experiencia de usuario enriquecida mediante la incorporación de funcionalidades avanzadas de comentarios y gráficos dinámicos que facilitan la interpretación de datos estadísticos relevantes.

---

### Dependencias Adicionales
En el frontend, se incluye la biblioteca de Highcharts en el archivo HTML principal (`index.html`):

```html
<script src="https://code.highcharts.com/highcharts.js"></script>
```

---