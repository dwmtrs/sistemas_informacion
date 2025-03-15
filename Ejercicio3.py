import json
import pandas as pd
import numpy as np

# Cargar los datos desde el archivo JSON
with open("datos_Pr1.json", "r") as file:
    data = json.load(file)

# Convertir los datos en DataFrames
df_tickets = pd.DataFrame(data["tickets_emitidos"])
df_empleados = pd.DataFrame(data["empleados"])
df_tipos_incidentes = pd.DataFrame(data["tipos_incidentes"])

# Expandir la lista de contactos en un DataFrame
contactos = []
for ticket in data["tickets_emitidos"]:
    for contacto in ticket["contactos_con_empleados"]:
        contactos.append({
            "id_ticket": ticket["tipo_incidencia"],
            "cliente": ticket["cliente"],
            "tipo_incidencia": ticket["tipo_incidencia"],
            "fecha_apertura": ticket["fecha_apertura"],
            "fecha_cierre": ticket["fecha_cierre"],
            "id_emp": contacto["id_emp"],
            "fecha_contacto": contacto["fecha"],
            "tiempo": contacto["tiempo"]
        })

df_contactos = pd.DataFrame(contactos)

# Convertir fechas a formato datetime
df_contactos["fecha_apertura"] = pd.to_datetime(df_contactos["fecha_apertura"])
df_contactos["fecha_cierre"] = pd.to_datetime(df_contactos["fecha_cierre"])
df_contactos["fecha_contacto"] = pd.to_datetime(df_contactos["fecha_contacto"])

# Agregar columna de día de la semana
df_contactos["dia_semana"] = df_contactos["fecha_apertura"].dt.day_name()

# Calcular tiempo de resolución (en horas)
df_contactos["tiempo_resolucion"] = (df_contactos["fecha_cierre"] - df_contactos["fecha_apertura"]).dt.total_seconds() / 3600

# Filtrar solo los incidentes de tipo "Fraude" (id_inci = 5)
df_fraude = df_contactos[df_contactos["tipo_incidencia"] == 5]

# **Número total de incidentes de Fraude**
num_incidentes_fraude = df_fraude["id_ticket"].nunique()

# **Número de actuaciones realizadas por los empleados (contactos)**
num_actuaciones_por_empleado = df_fraude.groupby("id_emp")["id_ticket"].count().reset_index()
num_actuaciones_por_empleado.columns = ["id_emp", "num_actuaciones"]

# **Agrupación por empleado**
fraude_por_empleado = df_fraude.groupby("id_emp").agg(
    num_incidentes=("id_ticket", "nunique"),
    num_actuaciones=("id_ticket", "count"),
    media_tiempo_resolucion=("tiempo_resolucion", "mean"),
    mediana_tiempo_resolucion=("tiempo_resolucion", "median"),
    varianza_tiempo_resolucion=("tiempo_resolucion", "var"),
    min_tiempo_resolucion=("tiempo_resolucion", "min"),
    max_tiempo_resolucion=("tiempo_resolucion", "max")
).reset_index()

# **Agrupación por nivel de empleado**
df_fraude = df_fraude.merge(df_empleados[["id_emp", "nivel"]], on="id_emp", how="left")
fraude_por_nivel = df_fraude.groupby("nivel").agg(
    num_incidentes=("id_ticket", "nunique"),
    num_actuaciones=("id_ticket", "count"),
    media_tiempo_resolucion=("tiempo_resolucion", "mean"),
    mediana_tiempo_resolucion=("tiempo_resolucion", "median"),
    varianza_tiempo_resolucion=("tiempo_resolucion", "var"),
    min_tiempo_resolucion=("tiempo_resolucion", "min"),
    max_tiempo_resolucion=("tiempo_resolucion", "max")
).reset_index()

# **Agrupación por cliente**
fraude_por_cliente = df_fraude.groupby("cliente").agg(
    num_incidentes=("id_ticket", "nunique"),
    num_actuaciones=("id_ticket", "count"),
    media_tiempo_resolucion=("tiempo_resolucion", "mean"),
    mediana_tiempo_resolucion=("tiempo_resolucion", "median"),
    varianza_tiempo_resolucion=("tiempo_resolucion", "var"),
    min_tiempo_resolucion=("tiempo_resolucion", "min"),
    max_tiempo_resolucion=("tiempo_resolucion", "max")
).reset_index()

# **Agrupación por día de la semana**
fraude_por_dia_semana = df_fraude.groupby("dia_semana").agg(
    num_incidentes=("id_ticket", "nunique"),
    num_actuaciones=("id_ticket", "count"),
    media_tiempo_resolucion=("tiempo_resolucion", "mean"),
    mediana_tiempo_resolucion=("tiempo_resolucion", "median"),
    varianza_tiempo_resolucion=("tiempo_resolucion", "var"),
    min_tiempo_resolucion=("tiempo_resolucion", "min"),
    max_tiempo_resolucion=("tiempo_resolucion", "max")
).reset_index()

# Ordenar los días de la semana correctamente
dias_orden = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
fraude_por_dia_semana["dia_semana"] = pd.Categorical(fraude_por_dia_semana["dia_semana"], categories=dias_orden, ordered=True)
fraude_por_dia_semana = fraude_por_dia_semana.sort_values("dia_semana")

# **Resultados**
print("\n📌 Número total de incidentes de tipo 'Fraude':", num_incidentes_fraude)
print("\n📌 Número de actuaciones por empleado:")
print(num_actuaciones_por_empleado)

print("\n📌 Análisis por empleado:")
print(fraude_por_empleado)

print("\n📌 Análisis por nivel de empleado:")
print(fraude_por_nivel)

print("\n📌 Análisis por cliente:")
print(fraude_por_cliente)

print("\n📌 Análisis por día de la semana:")
print(fraude_por_dia_semana)
