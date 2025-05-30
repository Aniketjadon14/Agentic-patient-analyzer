from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END
from graphviz import Digraph
from nodes.user_input import UserInputNode
from nodes.query_db import QueryDBNode
from nodes.check_abnormal import CheckAbnormalNode
from nodes.summarize import SummarizeNode
from nodes.alert import AlertNode
from nodes.generate_sql import GenerateSQLNode
from nodes.SuggestQuestion import SuggestQuestionsNode

class PatientVisitState(TypedDict):
    input: str
    query: str
    result: str
    abnormal: bool
    summary: Optional[str]
    alert1: Optional[str]
    suggested_questions: Optional[list]  # List of suggested follow-up questions

builder = StateGraph(PatientVisitState)

# Instantiate classes
user_input_node = UserInputNode()
query_db_node = QueryDBNode()
suggest_questions_node = SuggestQuestionsNode()
check_abnormal_node = CheckAbnormalNode()
summarize_node = SummarizeNode()
alert_node = AlertNode()
generate_sql_node = GenerateSQLNode()

# Add nodes
builder.add_node("user_input", user_input_node)
builder.add_node("generate_sql", generate_sql_node)
builder.add_node("Suggest_Questions", suggest_questions_node)
builder.add_node("query_db", query_db_node)
builder.add_node("check_abnormal", check_abnormal_node)
builder.add_node("summarize", summarize_node)
builder.add_node("alert", alert_node)

# Add edges (NO Suggest_Questions -> user_input in backend!)
builder.set_entry_point("user_input")
builder.add_edge("user_input", "generate_sql")
builder.add_edge("generate_sql", "query_db")
builder.add_edge("query_db", "check_abnormal")
builder.add_edge("check_abnormal", "summarize")
builder.add_edge("summarize", "alert")
builder.add_edge("alert", END)

builder.add_conditional_edges(
    "check_abnormal",
    lambda state: "alert" if state["abnormal"] else "summarize",
    {
        "alert": "alert",
        "summarize": "summarize"
    }
)

builder.add_edge("summarize", "Suggest_Questions")
builder.add_edge("Suggest_Questions", END)
builder.add_edge("alert", END)

# Compile graph
patient_graph = builder.compile()

def visualize_graph(builder):
    dot = Digraph()
    for node in builder.nodes:
        dot.node(node)
    for src, tgt in builder.edges:
        dot.edge(src, tgt)
    # Visualization only: show Suggest_Questions -> user_input as a dashed edge
    dot.edge("Suggest_Questions", "user_input", style="dashed", label="on suggestion click")
    dot.render('stategraph', view=True)

if __name__ == "__main__":
    visualize_graph(builder)