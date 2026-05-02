import duckdb
import os

class DuckDBService:

    def __init__(self):
        self.con = duckdb.connect()
        self.con.execute("INSTALL postgres;")
        self.con.execute("LOAD postgres;")

        self.conn_string = (
            f"host=72.61.2.146 "
            f"dbname=ventas_aje "
            f"user=postgres "
            f"password={os.getenv('PG_PASSWORD')}"
        )

    def run_query(self, sql: str):
        try:
            result = self.con.execute(sql).df()
            return result
        except Exception as e:
            raise Exception(f"Error ejecutando SQL: {str(e)}")

    def get_table(self):
        return f"""
        SELECT * FROM postgres_scan(
            '{self.conn_string}',
            'public',
            'ventas'
        )
        """
