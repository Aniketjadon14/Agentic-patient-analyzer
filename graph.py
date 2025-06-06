from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from nodes.user_input import user_input_tool
from nodes.generate_sql import generate_sql_tool
from nodes.query_db import query_db_tool
from nodes.summarize import summarize_tool
# from nodes.validate_sql import validate_sql_tool
from nodes.sql_correction import sql_correction_tool  # <-- Add this import
from state import PatientVisitState
from nodes.schema_understanding import schema_understanding_tool
import networkx as nx



def validation_no_handler(state: PatientVisitState):
    state.result = "The generated SQL query is invalid for the schema. Please rephrase your question."
    return state

def retry_limit_handler(state: PatientVisitState):
    state.result = "Unable to resolve your request due to repeated database errors."
    return state

def increment_retry(state: PatientVisitState):
    state.retry_count += 1
    return state

builder = StateGraph(PatientVisitState)

builder.add_node("user_input", user_input_tool)
builder.add_node("schema_understanding", schema_understanding_tool)
builder.add_node("generate_sql", generate_sql_tool)
# builder.add_node("validate_sql", validate_sql_tool)
builder.add_node("query_db", query_db_tool)
builder.add_node("sql_correction", sql_correction_tool)  # <-- Add this node
builder.add_node("increment_retry", RunnableLambda(increment_retry))
builder.add_node("summarize", summarize_tool)
builder.add_node("validation_no", RunnableLambda(validation_no_handler))
builder.add_node("retry_limit", RunnableLambda(retry_limit_handler))  # <-- Add this node

builder.set_entry_point("user_input")
builder.add_edge("user_input", "schema_understanding")
builder.add_edge("schema_understanding", "generate_sql")
builder.add_edge("generate_sql", "query_db")

# def validation_condition(state: PatientVisitState):
#     return state.validation == "YES"

# builder.add_conditional_edges(
#     "validate_sql",
#     lambda state: "query_db" if validation_condition(state) else "validation_no",
#     {
#         "query_db": "query_db",
#         "validation_no": "validation_no"
#     }
# )

# Retry logic after query_db
def db_error_condition(state: PatientVisitState):
    # If db_error is set, and retry_count < 3, go to correction; else, fallback
    if state.db_error and state.retry_count < 3:
        return "sql_correction"
    elif state.db_error and state.retry_count >= 3:
        return "retry_limit"
    else:
        return "summarize"

builder.add_conditional_edges(
    "query_db",
    db_error_condition,
    {
        "sql_correction": "sql_correction",
        "retry_limit": "retry_limit",
        "summarize": "summarize"
    }
)

# After correction, increment retry_count, validate, and try again


builder.add_edge("sql_correction", "increment_retry")
builder.add_edge("increment_retry", "query_db")

builder.add_edge("validation_no", "summarize")
builder.add_edge("retry_limit", "summarize")
builder.add_edge("summarize", END)

patient_graph = builder.compile()

if __name__ == "__main__":

    # Manually reconstruct the graph for visualization
    G = nx.DiGraph()
    G.add_nodes_from([
        "user_input",
        "schema_understanding",
        "generate_sql",
        "query_db",
        "sql_correction",
        "increment_retry",
        "summarize",
        "validation_no",
        "retry_limit",
        "END"
    ])
    G.add_edge("user_input", "schema_understanding")
    G.add_edge("schema_understanding", "generate_sql")
    G.add_edge("generate_sql", "query_db")
    G.add_edge("query_db", "sql_correction")
    G.add_edge("query_db", "retry_limit")
    G.add_edge("query_db", "summarize")
    G.add_edge("sql_correction", "increment_retry")
    G.add_edge("increment_retry", "query_db")
    G.add_edge("validation_no", "summarize")
    G.add_edge("retry_limit", "summarize")
    G.add_edge("summarize", "END")

    nx.drawing.nx_pydot.write_dot(G, "pipeline_graph.dot")
    print("DOT file saved as pipeline_graph.dot")