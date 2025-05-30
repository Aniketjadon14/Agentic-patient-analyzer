from dotenv import load_dotenv
from graph import patient_graph
from dotenv import load_dotenv
load_dotenv()

load_dotenv()

if __name__ == "__main__":
    input_text = "give me the count of patients at  riskLevel High Risk"
    result = patient_graph.invoke({"input": input_text})
    print("=== FINAL RESULT ===")
    print(result)
