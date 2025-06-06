from db.connect import DBConnector
from state import PatientVisitState

db = DBConnector()

def query_db_tool(state: PatientVisitState) -> PatientVisitState:
    """Runs SQL query on the database and handles DB errors."""
    try:
        result = db.run_sql_query(state.query)
        if result and not result.startswith("Error:"):
            state.result = result
            state.db_error = None
        else:
            # DB-specific error
            state.result = None
            state.db_error = result
    except Exception as e:
        state.result = None
        state.db_error = str(e)
    print(f"\n[DB Result] {state.result}\n[DB Error] {state.db_error}\n")
    return state