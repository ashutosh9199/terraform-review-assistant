from fastapi import APIRouter, HTTPException
import os
from core.config import settings
from services.parser import TerraformParser
from services.rule_engine import RuleEngine
from services.ai_reviewer import AIReviewer
from services.scoring import ScoringEngine
from models.domain import ReviewReport

router = APIRouter()

@router.post("/{project_id}", response_model=ReviewReport)
async def analyze_project(project_id: str):
    project_dir = os.path.join(settings.UPLOAD_DIR, project_id)
    if not os.path.exists(project_dir):
        raise HTTPException(status_code=404, detail="Project not found.")
    
    try:
        # 1. Parse Terraform files
        parser = TerraformParser(project_dir)
        resources = parser.parse()
        
        # 2. Rule Engine (Static Analysis)
        rule_engine = RuleEngine()
        static_findings = rule_engine.analyze(resources)
        
        # 3. AI Review
        ai_reviewer = AIReviewer()
        ai_findings = await ai_reviewer.analyze(resources)
        
        # Combine findings
        all_findings = static_findings + ai_findings
        
        # 4. Scoring Engine
        scoring = ScoringEngine()
        report = scoring.calculate_scores(all_findings)
        
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
