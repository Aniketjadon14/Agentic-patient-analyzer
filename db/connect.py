import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
load_dotenv()

class DBConnector:
    def __init__(self):
        self.engine = create_engine(os.getenv("DATABASE_URL"))

    def run_sql_query(self, query: str) -> str:
        with self.engine.connect() as conn:
            result = conn.execute(text(query))
            return "\n".join(str(row) for row in result)
