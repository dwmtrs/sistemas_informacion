import pandas as pd
import sqlite3


def ejecutar(top_n=5):
    try:
        conn = sqlite3.connect('sistemas_info.db')

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

        conn.close()
        return df

    except Exception as e:
        print(f"Error: {str(e)}")
        return pd.DataFrame(columns=['ID', 'Cliente', 'Incidencias'])


if __name__ == "__main__":
    ejecutar()