from fastapi import FastAPI
from pydantic import BaseModel
from services.duckdb_service import DuckDBService
from services.llm_service import LLMService
from services.insight_service import InsightService
from utils.schema import get_schema

app = FastAPI()

duck = DuckDBService()
llm = LLMService()
insight = InsightService()

class QueryRequest(BaseModel):
    prompt: str

@app.post("/chat")
def chat(request: QueryRequest):
    try:
        # 1. esquema
        schema = get_schema()

        # 2. generar SQL
        sql = llm.generate_sql(request.prompt, schema)

        # 🔥 importante: envolver con postgres_scan
        final_sql = f"""
        SELECT * FROM (
            {sql.replace("FROM ventas", f"FROM ({duck.get_table()}) as ventas")}
        )
        LIMIT 1000
        """

        # 3. ejecutar
        df = duck.run_query(final_sql)

        # 4. insights
        data_sample = insight.summarize(df)
        insights = llm.generate_insights(data_sample)

        return {
            "sql": sql,
            "rows": df.to_dict(orient="records"),
            "insights": insights
        }

    except Exception as e:
        return {"error": str(e)}
