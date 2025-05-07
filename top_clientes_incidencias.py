import pandas as pd
import sqlite3


def ejecutar(top_n=5, tipo="clientes"):
    try:
        conn = sqlite3.connect('sistemas_info.db')

        if tipo == "clientes":
            query = """
            SELECT 
                c.id_cli,
                c.nombre,
                COUNT(*) as num_incidencias
            FROM tickets_emitidos t
            JOIN clientes c ON t.cliente = c.id_cli
            GROUP BY c.id_cli, c.nombre
            ORDER BY num_incidencias DESC
            LIMIT ?
            """

            df = pd.read_sql(query, conn, params=(top_n,))
            df.columns = ['ID', 'Cliente', 'Incidencias']

            print(f"Top {top_n} clientes con más incidencias:")
            print(df.to_string(index=False))

        elif tipo == "empleados":
            query = """
            SELECT 
                e.id_emp,
                e.nombre,
                SUM(ce.tiempo) as tiempo_total,
                COUNT(DISTINCT ce.ticket_id) as num_incidencias,
                ROUND(SUM(ce.tiempo) / COUNT(DISTINCT ce.ticket_id), 2) as tiempo_promedio
            FROM contactos_con_empleados ce
            JOIN empleados e ON ce.id_emp = e.id_emp
            GROUP BY e.id_emp, e.nombre
            ORDER BY tiempo_total DESC
            LIMIT ?
            """

            df = pd.read_sql(query, conn, params=(top_n,))
            df.columns = ['ID', 'Empleado', 'Tiempo Total (h)', 'Incidencias Atendidas', 'Tiempo Promedio (h)']

            print(f"Top {top_n} empleados que más tiempo han dedicado a la resolución de incidentes:")
            print(df.to_string(index=False))

        else:
            print(f"Tipo de consulta no válido: {tipo}")
            df = pd.DataFrame()

        conn.close()
        return df

    except Exception as e:
        print(f"Error: {str(e)}")
        return pd.DataFrame()