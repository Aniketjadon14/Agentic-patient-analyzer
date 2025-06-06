from pydantic import BaseModel
from typing_extensions import Optional


class PatientVisitState(BaseModel):
    input: Optional[str] = None
    query: Optional[str] = None
    result: Optional[str] = None
    summary: Optional[str] = None
    validation: Optional[str] = None
    schema_metadata: Optional[str] = None
    retry_count: int = 0  # <-- Add this
    db_error: Optional[str] = None
