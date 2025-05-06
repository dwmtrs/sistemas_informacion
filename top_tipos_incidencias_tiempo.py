import pandas as pd
import sqlite3


def ejecutar(top_n=5):
    try:
        conn = sqlite3.connect('sistemas_info.db')

        query = """
        SELECT 
            ti.id_inci,
            ti.nombre,
            JULIANDAY(te.fecha_cierre) - JULIANDAY(te.fecha_apertura) as tiempo_resolucion
        FROM tickets_emitidos te
        JOIN tipos_incidentes ti ON te.tipo_incidencia = ti.id_inci
        """

        df = pd.read_sql(query, conn)

        resultado = df.groupby(['id_inci', 'nombre'])['tiempo_resolucion'].agg(['mean', 'count']).reset_index()
        resultado.columns = ['ID', 'Tipo de Incidencia', 'Tiempo Medio (días)', 'Cantidad']

        resultado = resultado.sort_values('Tiempo Medio (días)', ascending=False)

        print(f"Top {top_n} tipos de incidencias por tiempo de resolución:")
        top_resultados = resultado.head(top_n)
        print(top_resultados.to_string(index=False))

        conn.close()
        return top_resultados

    except Exception as e:
        print(f"Error: {str(e)}")
        return pd.DataFrame(columns=['ID', 'Tipo de Incidencia', 'Tiempo Medio (días)', 'Cantidad'])


if __name__ == "__main__":
    ejecutar()