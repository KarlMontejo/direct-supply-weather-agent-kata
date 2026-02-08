from pydantic import BaseModel
from typing import List

class Violation(BaseModel):
    product_id: int
    reason: str

class ComplianceAssessment(BaseModel):
    violations: List[Violation]
    is_compliant: bool