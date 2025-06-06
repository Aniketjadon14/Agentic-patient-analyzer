# from langchain_core.tools import tool
from state import PatientVisitState

# @tool(args_schema=PatientVisitState)
def user_input_tool(state: PatientVisitState) -> PatientVisitState:
    """Take user question as 'input'"""
    return state