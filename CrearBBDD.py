import sqlite3
import json

with open('datos_Pr1.json', 'r') as file:
    data = json.load(file)

cnx = sqlite3.connect('sistemas_info.db')
cursor = cnx.cursor()

create_tables_query = """
CREATE TABLE IF NOT EXISTS clientes (
    id_cli TEXT PRIMARY KEY,
    nombre TEXT,
    telefono TEXT,
    provincia TEXT
);

CREATE TABLE IF NOT EXISTS empleados (
    id_emp TEXT PRIMARY KEY,
    nombre TEXT,
    nivel INTEGER,
    fecha_contrato TEXT
);

CREATE TABLE IF NOT EXISTS tipos_incidentes (
    id_inci TEXT PRIMARY KEY,
    nombre TEXT
);

CREATE TABLE IF NOT EXISTS tickets_emitidos (
    id_ticket INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente TEXT,
    fecha_apertura TEXT,
    fecha_cierre TEXT,
    es_mantenimiento BOOLEAN,
    satisfaccion_cliente INTEGER,
    tipo_incidencia TEXT,
    FOREIGN KEY (cliente) REFERENCES clientes(id_cli),
    FOREIGN KEY (tipo_incidencia) REFERENCES tipos_incidentes(id_inci)
);

CREATE TABLE IF NOT EXISTS contactos_con_empleados (
    id_contacto INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id INTEGER,
    id_emp TEXT,
    fecha TEXT,
    tiempo REAL,
    FOREIGN KEY (ticket_id) REFERENCES tickets_emitidos(id_ticket),
    FOREIGN KEY (id_emp) REFERENCES empleados(id_emp)
);
"""

for query in create_tables_query.split(';'):
    if query.strip():
        cursor.execute(query)

for cliente in data['clientes']:
    query = ("INSERT INTO clientes (id_cli, nombre, telefono, provincia) "
             "VALUES (?, ?, ?, ?)")
    cursor.execute(query, (cliente['id_cli'], cliente['nombre'], cliente['telefono'], cliente['provincia']))

for empleado in data['empleados']:
    query = ("INSERT INTO empleados (id_emp, nombre, nivel, fecha_contrato) "
             "VALUES (?, ?, ?, ?)")
    cursor.execute(query, (empleado['id_emp'], empleado['nombre'], empleado['nivel'], empleado['fecha_contrato']))

for tipo_incidente in data['tipos_incidentes']:
    query = ("INSERT INTO tipos_incidentes (id_inci, nombre) "
             "VALUES (?, ?)")
    cursor.execute(query, (tipo_incidente['id_inci'], tipo_incidente['nombre']))

for ticket in data['tickets_emitidos']:
    query = ("INSERT INTO tickets_emitidos (cliente, fecha_apertura, fecha_cierre, es_mantenimiento, satisfaccion_cliente, tipo_incidencia) "
             "VALUES (?, ?, ?, ?, ?, ?)")
    cursor.execute(query, (ticket['cliente'], ticket['fecha_apertura'], ticket['fecha_cierre'], ticket['es_mantenimiento'], ticket['satisfaccion_cliente'], ticket['tipo_incidencia']))

    ticket_id = cursor.lastrowid

    for contacto in ticket['contactos_con_empleados']:
        query = ("INSERT INTO contactos_con_empleados (ticket_id, id_emp, fecha, tiempo) "
                 "VALUES (?, ?, ?, ?)")
        cursor.execute(query, (ticket_id, contacto['id_emp'], contacto['fecha'], contacto['tiempo']))

cnx.commit()

cursor.close()
cnx.close()
