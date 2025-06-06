# from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from state import PatientVisitState

# Instantiate the LLM at module level
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.6)

# @tool(args_schema=PatientVisitState)
def summarize_tool(state: PatientVisitState) -> PatientVisitState:
    """Summarizes SQL query results."""
    response = llm.invoke(f"Summarize the following medical findings:\n{state.result}")
    summary = response.content.strip()
    print(f"\n[Summary] {summary}\n")
    state.summary = summary
    return state