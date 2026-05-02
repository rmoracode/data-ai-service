from sqlalchemy import create_engine, text
import os

DB_URL = (
    f"postgresql+psycopg2://postgres:{os.getenv('PG_PASSWORD')}"
    f"@72.61.2.146:5432/ventas_aje"
)

engine = create_engine(DB_URL)

def get_schema():
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = 'ventas'
        """))
        cols = result.fetchall()

    return "\n".join([f"- {c[0]} ({c[1]})" for c in cols])
