import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

load_dotenv()

class DBConnector:
    def __init__(self):
        self.engine = create_engine(os.getenv("DATABASE_URL"))

    def run_sql_query(self, query: str) -> str:
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(query))
                results = "\n".join(str(row) for row in result)
                print("\n##############################")
                print(f"[DB Result] input:\n{results}")
                return results

        except SQLAlchemyError as e:
            # Print the error message to the console
            print("\n########DB Error######################")
            print("[DB Error] An error occurred while executing the query:")
            print(str(e))
            return f"Error: {str(e)}"   
