import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class LLMService:

    def generate_sql(self, prompt: str, schema: str):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0,
            messages=[{
                "role": "user",
                "content": f"""
Eres experto en SQL.

Reglas:
- SOLO SELECT
- SIEMPRE LIMIT 1000
- NO DELETE, UPDATE, DROP

Tabla: ventas

Columnas:
{schema}

Usuario: {prompt}

Responde SOLO SQL limpio.
"""
            }]
        )

        sql = response.choices[0].message.content.strip()
        return sql.replace("```", "").strip()

    def generate_insights(self, data_text: str):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.3,
            messages=[{
                "role": "user",
                "content": f"""
Eres analista de datos senior.

Analiza:

{data_text}

Dame:
- patrones
- anomalías
- recomendaciones
"""
            }]
        )

        return response.choices[0].message.content
