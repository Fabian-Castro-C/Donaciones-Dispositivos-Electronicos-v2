import pymysql
from app.config import Config

def obtener_conexion():
    """Crea y devuelve una conexión a la base de datos."""
    return pymysql.connect(
        host=Config.MYSQL_HOST,
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
