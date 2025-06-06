from dotenv import load_dotenv
from graph import patient_graph
from state import PatientVisitState

load_dotenv()
  
if __name__ == "__main__":
    input_text =  "give me the address   for  patientId 402?"
    

    state: PatientVisitState = PatientVisitState(
        input=input_text
    )
    
    result = patient_graph.invoke(state)
    print("=== FINAL RESULT ===")
    print(result)
