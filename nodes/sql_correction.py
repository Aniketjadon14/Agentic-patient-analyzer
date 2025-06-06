from langchain_openai import ChatOpenAI
from state import PatientVisitState

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

def sql_correction_tool(state: PatientVisitState) -> PatientVisitState:
    """
    Attempts to correct a failed SQL query using the original prompt, the failed query, and the DB error.
    """
    prompt = f"""
    The following SQL query failed with a database error.
    User prompt: {state.input}
    SQL query: {state.query}
    Database error: {state.db_error}
    Please generate a corrected SQL query for the user's request, considering the schema:
    {state.schema_metadata or ""}
    Return ONLY the raw SQL query, no explanations.
    """
    response = llm.invoke(prompt)
    corrected_sql = response.content.strip()
    print(f"\n[SQL Correction] {corrected_sql}\n")
    state.query = corrected_sql
    return state