# from state import PatientVisitState
# from langchain_openai import ChatOpenAI

# llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# def validate_sql_tool(state: PatientVisitState) -> PatientVisitState:
#     """Validates the generated SQL query against the schema."""
#     schema = f"""
#     You are a medical SQL expert. Here is the database schema:
#     {state.schema_metadata or ""}

#     Given a user's question, convert it to a SQL query.
#     You are a medical SQL expert. Given a user's question, convert it to a SQL query.
#     Return ONLY the raw SQL query — do NOT include markdown formatting or sql blocks.
#     Do not include any explanations, comments, or markdown syntax.
#     Your job is to convert user questions into SQL queries that can extract relevant data.
#     Always put table name, column name inside double quote.
#     riskLevel has possible values as `High Risk`,`Moderate Risk`, `Very High Risk` and `Low Risk`.
#     """
#     print("\n[Validate SQL] Checking the following query against schema:")
#     print(f"SQL Query: {state.query}\n")
#     prompt = f"""
#     Given the following table schema:
#     {schema}

#     Is this SQL query valid for the schema? Only answer YES or NO.

#     SQL Query:
#     {state.query}
#     """
#     response = llm.invoke(prompt)
#     answer = response.content.strip().upper()
#     print(f"\n[answer] {answer}\n")
#     state.validation = answer
#     return state