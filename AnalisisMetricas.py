import sqlite3
import pandas as pd

def ejecutar():
    try:
        with sqlite3.connect('sistemas_info.db') as cnx:
            # Diccionario para almacenar todas las métricas
            metricas = {}

            # 1. Métricas básicas
            df_tickets = pd.read_sql_query("SELECT COUNT(*) AS total_tickets FROM tickets_emitidos", cnx)
            metricas['total_tickets'] = df_tickets['total_tickets'].iloc[0]

            # 2. Análisis de satisfacción
            df_satisfaccion = pd.read_sql_query("""
                SELECT satisfaccion_cliente 
                FROM tickets_emitidos
                WHERE satisfaccion_cliente >= 5
            """, cnx)
            metricas['satisfaccion_media'] = df_satisfaccion['satisfaccion_cliente'].mean()
            metricas['satisfaccion_desviacion'] = df_satisfaccion['satisfaccion_cliente'].std()

            # 3. Distribución de incidentes por cliente
            df_incidentes_cliente = pd.read_sql_query("""
                SELECT cliente, COUNT(*) AS total_incidentes
                FROM tickets_emitidos
                GROUP BY cliente
            """, cnx)
            stats_cliente = df_incidentes_cliente['total_incidentes'].describe()

            # 4. Tiempos de resolución
            df_tiempos = pd.read_sql_query("""
                SELECT 
                    JULIANDAY(fecha_cierre) - JULIANDAY(fecha_apertura) AS horas_resolucion
                FROM tickets_emitidos
                WHERE fecha_apertura IS NOT NULL AND fecha_cierre IS NOT NULL
            """, cnx)
            stats_tiempos = df_tiempos['horas_resolucion'].describe() * 24  # Convertir días a horas

            # 5. Carga de trabajo de empleados
            df_carga_empleados = pd.read_sql_query("""
                SELECT 
                    id_emp,
                    COUNT(*) AS total_incidentes,
                    SUM(tiempo) AS total_horas
                FROM contactos_con_empleados
                GROUP BY id_emp
            """, cnx)
            stats_horas = df_carga_empleados['total_horas'].describe()

            # Crear DataFrames para visualización
            df_resumen = pd.DataFrame({
                'Métrica': [
                    'Total tickets',
                    'Satisfacción media (≥5)',
                    'Desviación satisfacción',
                    'Media incidentes/cliente',
                    'Máximo incidentes/cliente',
                    'Media horas/resolución',
                    'Máximo horas/resolución',
                    'Media horas/empleado'
                ],
                'Valor': [
                    metricas['total_tickets'],
                    round(metricas['satisfaccion_media'], 2),
                    round(metricas['satisfaccion_desviacion'], 2),
                    round(stats_cliente['mean'], 2),
                    stats_cliente['max'],
                    round(stats_tiempos['mean'], 2),
                    round(stats_tiempos['max'], 2),
                    round(stats_horas['mean'], 2)
                ]
            })

            df_detalle_empleados = df_carga_empleados.sort_values('total_horas', ascending=False).head(10)

            return [df_resumen, df_detalle_empleados]

    except Exception as e:
        print(f"Error: {str(e)}")
        return pd.DataFrame()  # Devuelve DataFrame vacío en caso de error

