import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Conectar a la base de datos
cnx = sqlite3.connect('sistemas_info.db')

# 1. Tiempo medio de resolución por tipo de incidente (mantenimiento o no)
df_tiempos = pd.read_sql_query("""
SELECT es_mantenimiento, 
       AVG((JULIANDAY(fecha_cierre) - JULIANDAY(fecha_apertura)) * 24) AS tiempo_medio
FROM tickets_emitidos
WHERE fecha_apertura IS NOT NULL AND fecha_cierre IS NOT NULL
GROUP BY es_mantenimiento
""", cnx)

plt.figure(figsize=(8, 6))
sns.barplot(data=df_tiempos, x='es_mantenimiento', y='tiempo_medio')
plt.xticks([0, 1], ['No Mantenimiento', 'Mantenimiento'])
plt.ylabel('Tiempo Medio de Resolución (horas)')
plt.title('Tiempo Medio de Resolución por Tipo de Incidente')
plt.savefig('tiempo_resolucion_incidentes.png')
plt.close()

# 2. Boxplot del tiempo de resolución por tipo de incidente
df_boxplot = pd.read_sql_query("""
SELECT tipo_incidencia, 
       (JULIANDAY(fecha_cierre) - JULIANDAY(fecha_apertura)) * 24 AS tiempo_resolucion
FROM tickets_emitidos
WHERE fecha_apertura IS NOT NULL AND fecha_cierre IS NOT NULL
""", cnx)

df_boxplot.dropna(inplace=True)
plt.figure(figsize=(10, 6))
sns.boxplot(data=df_boxplot, x='tipo_incidencia', y='tiempo_resolucion', showfliers=False)
plt.ylabel('Tiempo de Resolución (horas)')
plt.title('Distribución del Tiempo de Resolución por Tipo de Incidente')
plt.savefig('boxplot_tiempo_resolucion.png')
plt.close()

# 3. Los 5 clientes más críticos (con más incidentes de mantenimiento y tipo != 1)
df_criticos = pd.read_sql_query("""
SELECT cliente, COUNT(*) AS total_incidentes
FROM tickets_emitidos
WHERE es_mantenimiento = 1 AND tipo_incidencia != '1'
GROUP BY cliente
ORDER BY total_incidentes DESC
LIMIT 5
""", cnx)

plt.figure(figsize=(8, 6))
sns.barplot(data=df_criticos, x='cliente', y='total_incidentes')
plt.ylabel('Cantidad de Incidentes')
plt.title('Top 5 Clientes Más Críticos')
plt.savefig('clientes_criticos.png')
plt.close()

# 4. Número total de actuaciones realizadas por empleados
df_actuaciones = pd.read_sql_query("""
SELECT id_emp, COUNT(*) AS total_actuaciones
FROM contactos_con_empleados
GROUP BY id_emp
""", cnx)

plt.figure(figsize=(10, 6))
sns.barplot(data=df_actuaciones, x='id_emp', y='total_actuaciones')
plt.xticks(rotation=45)
plt.ylabel('Total de Actuaciones')
plt.title('Número Total de Actuaciones por Empleado')
plt.savefig('actuaciones_empleados.png')
plt.close()

# 5. Actuaciones según el día de la semana
df_dias = pd.read_sql_query("""
SELECT strftime('%w', fecha) AS dia_semana, COUNT(*) AS total_actuaciones
FROM contactos_con_empleados
GROUP BY dia_semana
ORDER BY dia_semana
""", cnx)

plt.figure(figsize=(8, 6))
sns.barplot(data=df_dias, x='dia_semana', y='total_actuaciones')
plt.xticks([0, 1, 2, 3, 4, 5, 6], ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb'])
plt.ylabel('Total de Actuaciones')
plt.title('Total de Actuaciones por Día de la Semana')
plt.savefig('actuaciones_por_dia.png')
plt.close()

# Cerrar conexión
cnx.close()
