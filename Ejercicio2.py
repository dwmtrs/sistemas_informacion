import sqlite3
import numpy as np

cnx = sqlite3.connect('sistemas_info.db')
cursor = cnx.cursor()

cursor.execute("SELECT COUNT(*) FROM tickets_emitidos")
num_muestras_totales = cursor.fetchone()[0]
print(f"Numero de muestras totales: {num_muestras_totales}")

cursor.execute("SELECT satisfaccion_cliente FROM tickets_emitidos WHERE satisfaccion_cliente >= 5")
satisfacciones = [row[0] for row in cursor.fetchall()]

media_satisfaccion = np.mean(satisfacciones)
desviacion_satisfaccion = np.std(satisfacciones)
print(f"Media de satisfacción (valoración >= 5): {media_satisfaccion}")
print(f"Desviación estándar de satisfacción (valoración >= 5): {desviacion_satisfaccion}")

cursor.execute("SELECT cliente, COUNT(*) FROM tickets_emitidos GROUP BY cliente")
num_incidentes = [row[1] for row in cursor.fetchall()]

media_incidentes_cliente = np.mean(num_incidentes)
desviacion_incidentes_cliente = np.std(num_incidentes)
print(f"Media de incidentes por cliente: {media_incidentes_cliente}")
print(f"Desviación estándar de incidentes por cliente: {desviacion_incidentes_cliente}")

cursor.execute("SELECT ticket_id, SUM(tiempo) FROM contactos_con_empleados GROUP BY ticket_id")
horas_totales = [row[1] for row in cursor.fetchall()]

media_horas_incidente = np.mean(horas_totales)
desviacion_horas_incidente = np.std(horas_totales)
print(f"Media de horas por incidente: {media_horas_incidente}")
print(f"Desviación estándar de horas por incidente: {desviacion_horas_incidente}")

cursor.execute("SELECT id_emp, SUM(tiempo) FROM contactos_con_empleados GROUP BY id_emp")
horas_empleado = [row[1] for row in cursor.fetchall()]

min_horas_empleado = np.min(horas_empleado)
max_horas_empleado = np.max(horas_empleado)
print(f"Valor mínimo de horas por empleado: {min_horas_empleado}")
print(f"Valor máximo de horas por empleado: {max_horas_empleado}")

cursor.execute("SELECT JULIANDAY(fecha_cierre) - JULIANDAY(fecha_apertura) FROM tickets_emitidos")
duraciones = [row[0] for row in cursor.fetchall()]

min_duracion = np.min(duraciones)
max_duracion = np.max(duraciones)
print(f"Valor mínimo de duración (en días): {min_duracion}")
print(f"Valor máximo de duración (en días): {max_duracion}")

cursor.execute("SELECT id_emp, COUNT(ticket_id) FROM contactos_con_empleados GROUP BY id_emp")
incidentes_atendidos = [row[1] for row in cursor.fetchall()]

min_incidentes_atendidos = np.min(incidentes_atendidos)
max_incidentes_atendidos = np.max(incidentes_atendidos)
print(f"Valor mínimo de incidentes atendidos: {min_incidentes_atendidos}")
print(f"Valor máximo de incidentes atendidos: {max_incidentes_atendidos}")

cursor.close()
cnx.close()
