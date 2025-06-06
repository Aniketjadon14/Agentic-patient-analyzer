# from langchain_core.tools import tool
from state import PatientVisitState
from langchain_openai import ChatOpenAI


llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# @tool(args_schema=PatientVisitState)
def generate_sql_tool(state: PatientVisitState) -> PatientVisitState:
    """Generates SQL query from user input."""
    user_question = state.input

    system_prompt = f"""
    You are a medical SQL expert. Here is the database schema:
    {state.schema_metadata or ""}
    Given a user's question, convert it to a SQL query.
    You are a medical SQL expert. Given a user's question, convert it to a SQL query.
    Return ONLY the raw SQL query — do NOT include markdown formatting or sql blocks.
    Do not include any explanations, comments, or markdown syntax.
    Your job is to convert user questions into SQL queries that can extract relevant data.
    Always put table name, column name inside double quote.
    riskLevel has possible values as `High Risk`,`Moderate Risk`, `Very High Risk` and `Low Risk`.
    """


    prompt = f"{system_prompt}\n\nUser: {user_question}\nSQL:"
    response = llm.invoke(prompt)
    sql = response.content.strip()
    print(f"\n[Generate SQL] {sql}\n")
    # sql = 'SELECT "Doctorname" FROM "PatientHistory" WHERE "patientId" = 402;'  # Use single quotes outside
    state.query = sql
    return state