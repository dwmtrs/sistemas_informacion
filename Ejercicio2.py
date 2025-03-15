import sqlite3
import pandas as pd
import numpy as np

cnx = sqlite3.connect('sistemas_info.db')

df_tickets = pd.read_sql_query("SELECT COUNT(*) AS total_tickets FROM tickets_emitidos", cnx)
total_tickets = df_tickets['total_tickets'].iloc[0]

df_incidentes = pd.read_sql_query("""
SELECT satisfaccion_cliente 
FROM tickets_emitidos
WHERE satisfaccion_cliente >= 5
""", cnx)
media_incidentes_5 = df_incidentes['satisfaccion_cliente'].mean()
desviacion_incidentes_5 = df_incidentes['satisfaccion_cliente'].std()

df_incidentes_por_cliente = pd.read_sql_query("""
SELECT cliente, COUNT(*) AS total_incidentes
FROM tickets_emitidos
GROUP BY cliente
""", cnx)
media_incidentes_cliente = df_incidentes_por_cliente['total_incidentes'].mean()
desviacion_incidentes_cliente = df_incidentes_por_cliente['total_incidentes'].std()

df_horas_totales = pd.read_sql_query("""
SELECT ticket_id, SUM(tiempo) AS total_horas
FROM contactos_con_empleados
GROUP BY ticket_id
""", cnx)
media_horas_totales = df_horas_totales['total_horas'].mean()
desviacion_horas_totales = df_horas_totales['total_horas'].std()

df_horas_por_empleado = pd.read_sql_query("""
SELECT id_emp, SUM(tiempo) AS total_horas
FROM contactos_con_empleados
GROUP BY id_emp
""", cnx)
min_horas_empleado = df_horas_por_empleado['total_horas'].min()
max_horas_empleado = df_horas_por_empleado['total_horas'].max()

df_tiempos_incidente = pd.read_sql_query("""
SELECT fecha_apertura, fecha_cierre
FROM tickets_emitidos
WHERE fecha_apertura IS NOT NULL AND fecha_cierre IS NOT NULL
""", cnx)

df_tiempos_incidente['fecha_apertura'] = pd.to_datetime(df_tiempos_incidente['fecha_apertura'])
df_tiempos_incidente['fecha_cierre'] = pd.to_datetime(df_tiempos_incidente['fecha_cierre'])
df_tiempos_incidente['tiempo_abierto'] = (df_tiempos_incidente['fecha_cierre'] - df_tiempos_incidente['fecha_apertura']).dt.total_seconds() / 3600

min_tiempo_incidente = df_tiempos_incidente['tiempo_abierto'].min()
max_tiempo_incidente = df_tiempos_incidente['tiempo_abierto'].max()

df_incidentes_atendidos_por_empleado = pd.read_sql_query("""
SELECT id_emp, COUNT(*) AS total_incidentes
FROM contactos_con_empleados
GROUP BY id_emp
""", cnx)

min_incidentes_empleado = df_incidentes_atendidos_por_empleado['total_incidentes'].min()
max_incidentes_empleado = df_incidentes_atendidos_por_empleado['total_incidentes'].max()

cnx.close()

print("Número de muestras totales:", total_tickets)
print("Media y desviación estándar de incidentes con valoración >= 5:")
print("Media:", media_incidentes_5)
print("Desviación estándar:", desviacion_incidentes_5)
print("Media y desviación estándar de incidentes por cliente:")
print("Media:", media_incidentes_cliente)
print("Desviación estándar:", desviacion_incidentes_cliente)
print("Media y desviación estándar de horas totales realizadas por incidente:")
print("Media:", media_horas_totales)
print("Desviación estándar:", desviacion_horas_totales)
print("Valor mínimo y valor máximo de horas realizadas por los empleados:")
print("Mínimo:", min_horas_empleado)
print("Máximo:", max_horas_empleado)
print("Valor mínimo y valor máximo del tiempo entre apertura y cierre de incidente (en horas):")
print("Mínimo:", min_tiempo_incidente)
print("Máximo:", max_tiempo_incidente)
print("Valor mínimo y valor máximo del número de incidentes atendidos por cada empleado:")
print("Mínimo:", min_incidentes_empleado)
print("Máximo:", max_incidentes_empleado)
