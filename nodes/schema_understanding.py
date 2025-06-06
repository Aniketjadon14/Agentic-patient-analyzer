from db.connect import DBConnector
from state import PatientVisitState

db = DBConnector()

def schema_understanding_tool(state: PatientVisitState) -> PatientVisitState:
    """
    Extracts schema metadata from the DB and formats it for LLM prompt.
    """
    # Example: Get table and column info from PostgreSQL
    query = """
    SELECT table_name, column_name, data_type
    FROM information_schema.columns
    WHERE table_schema = 'public'
    ORDER BY table_name, ordinal_position;
    """
    result = db.run_sql_query(query)
    print("\n[Schema Raw Result]\n", result) 
    # Format as dict or string for LLM
    schema_lines = []
    current_table = None
    for row in result.splitlines():
        # row format: ('table_name', 'column_name', 'data_type')
        parts = row.strip("()").split(",")
        if len(parts) < 3:
            continue
        table, col, dtype = [p.strip(" '") for p in parts]
        if table != current_table:
            schema_lines.append(f"\nTable: {table}")
            current_table = table
        schema_lines.append(f"  - {col}: {dtype}")
    schema_str = "\n".join(schema_lines)
    print("\n[Schema Formatted for LLM]\n", schema_str)  # <-- Print formatted schema
    # Save to state for use in prompt
    state.schema_metadata = schema_str
    return state