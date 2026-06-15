from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class Resource(BaseModel):
    resource_type: str
    name: str
    properties: Dict[str, Any]
    file_path: Optional[str] = None
    line_number: Optional[int] = None

class Finding(BaseModel):
    resource_type: str
    resource_name: str
    issue: str
    risk_level: str # High, Medium, Low
    category: str # Security, Cost, Governance, Operational
    recommendation: str
    business_impact: str
    code_example: Optional[str] = None

class ScoreCategory(BaseModel):
    score: int
    findings_count: int

class ReviewReport(BaseModel):
    overall_score: int
    security: ScoreCategory
    cost: ScoreCategory
    governance: ScoreCategory
    operations: ScoreCategory
    findings: List[Finding]
