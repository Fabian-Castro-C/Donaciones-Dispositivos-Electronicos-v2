-- CONTACTO
-- agregar
INSERT INTO contacto (nombre, email, celular, comuna_id, fecha_creacion) VALUES (?, ?, ?, ?, ?)
-- obtener contactos ordenados desde el mas reciente insertado al más antiguo
SELECT id, nombre, email, celular, comuna_id, fecha_creacion FROM contacto ORDER BY id DESC

-- DISPOSITIVO
INSERT INTO dispositivo (contacto_id, nombre, descripcion, tipo, anos_uso, estado) VALUES (?,?,?,?,?,?)
-- obtener dispositivos asociados a un contacto
SELECT id, contacto_id, nombre, descripcion, tipo, anos_uso, estado FROM dispositivo WHERE contacto_id=?
-- obtener listado de dispositivos ordenados desde el mas reciente insertado al más antiguo limitado
-- a los primeros 5
SELECT id, contacto_id, nombre, descripcion, tipo, anos_uso, estado FROM dispositivo ORDER BY id DESC LIMIT 0, 5
-- listado de los siguientes 5
SELECT id, contacto_id, nombre, descripcion, tipo, anos_uso, estado FROM dispositivo ORDER BY id DESC LIMIT 5, 5
-- idem, incluyendo nombre de comuna
SELECT id, contacto_id, COM.nombre, nombre, descripcion, tipo, anos_uso, estado FROM dispositivo, contacto CO, comuna COM WHERE contacto_id=CO.id AND CO.comuna_id=COM.id ORDER BY id DESC LIMIT 5, 5


-- ARCHIVO
-- insertar
INSERT INTO archivo (ruta_archivo, nombre_archivo, dispositivo_id) VALUES (?,?,?)
-- obtener archivos asociados a un dispositivo
SELECT id, ruta_archivo, nombre_archivo FROM archivo WHERE dispositivo_id=?
