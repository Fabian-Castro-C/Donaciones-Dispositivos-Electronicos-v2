# Donaciones-Dispositivos-Electronicos-v2
Tarea 2 Desarrollo de Aplicaciones Web

### Creación de la base de datos
La base de datos fue creada siguiendo las siguientes instrucciones

```sql
CREATE DATABASE tarea2;
USE tarea2; 
```

Las tablas fueron creadas usando:
```sql
SOURCE ubicacion_proyecto/sql/tarea2.sql;
SOURCE ubicacion_proyecto/sql/region-comuna.sql;
```

### Configuración proyecto flask
Se creo un usuario en mi sistema operativo especialmente para ser usado en el proyecto.

```python
class Config:
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'fabiancastro' # Usuario creado
    MYSQL_PASSWORD = 'oiAc66zUgSvgIM9KiEbV' # Contraseña del usuario
    MYSQL_DB = 'tarea2' # Nombre de la base de datos
    MYSQL_CURSORCLASS = 'DictCursor' # Solicitamos que las respuestas sean en forma de diccionario
    SECRET_KEY = 'eec74d429e889a8e8297794d9462183e' # Llave secreta generada por secrets.token_hex(16)
```