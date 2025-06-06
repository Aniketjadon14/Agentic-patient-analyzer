import streamlit as st
from graph import patient_graph
from nodes.SuggestQuestion import SuggestQuestionsNode
from langchain_openai import ChatOpenAI
from nodes.suggestion_click_agent import SuggestionClickAgent


st.title("Anginx Patient Analyser")

if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "run_analyze" not in st.session_state:
    st.session_state.run_analyze = False
if "suggest_node" not in st.session_state:
    st.session_state.suggest_node = SuggestQuestionsNode()
if "suggestion_click_agent" not in st.session_state:
    st.session_state.suggestion_click_agent = SuggestionClickAgent(patient_graph)

user_input = st.text_input("Enter your medical query:", value=st.session_state.user_input)

def format_db_result(db_result):
    if isinstance(db_result, dict):
        return "\n".join(f"**{k}:** {v}" for k, v in db_result.items())
    elif isinstance(db_result, (list, tuple)):
        return "\n".join(str(item) for item in db_result)
    else:
        return str(db_result)

def format_human_readable(result):
    user_q = result.get("input", "")
    query = result.get("query", "")
    db_result = result.get("result", "")
    abnormal = result.get("abnormal", False)
    summary = result.get("summary", "")
    alert = result.get("alert1", "")

    lines = [
        f"**User Query:** {user_q}",
        f"**Generated SQL:** `{query}`",
        f"**Database Result:**\n{format_db_result(db_result)}",
        f"**Abnormal:** {'Yes' if abnormal else 'No'}"
    ]
    if alert:
        lines.append(f"**Alert:** {alert}")
    if summary:
        lines.append(f"**Summary:** {summary}")
    return "\n\n".join(lines)

# Analyze button logic
if st.button("Analyze"):
    st.session_state.user_input = user_input
    st.session_state.run_analyze = True
    st.rerun()

# Main analysis logic
if st.session_state.run_analyze and st.session_state.user_input.strip():
    result = patient_graph.invoke({"input": st.session_state.user_input})
    st.subheader("Result")
    st.markdown(format_human_readable(result), unsafe_allow_html=True)

    # Show question suggestions (NO clickable buttons now)
    suggest_node = st.session_state.suggest_node
    suggestions = suggest_node({"input": st.session_state.user_input})["suggested_questions"]
    st.markdown("**You may also ask:**")
    for i, s in enumerate(suggestions):
        if  st.button(s, key=f"suggestion_{i}"):
            st.session_state.user_input = s
            st.session_state.run_analyze = True
            st.rerun()

elif st.session_state.run_analyze:
    st.warning("Please enter a query.")
    st.session_state.run_analyze = False