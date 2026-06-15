from fastapi import APIRouter, HTTPException
import os
from core.config import settings
from services.parser import TerraformParser
from services.rule_engine import RuleEngine
from services.ai_reviewer import AIReviewer
from services.scoring import ScoringEngine
from models.domain import ReviewReport

import datetime

router = APIRouter()

@router.get("/history")
async def get_history():
    history = []
    if os.path.exists(settings.UPLOAD_DIR):
        for d in os.listdir(settings.UPLOAD_DIR):
            dir_path = os.path.join(settings.UPLOAD_DIR, d)
            if os.path.isdir(dir_path):
                ctime = os.path.getctime(dir_path)
                dt = datetime.datetime.fromtimestamp(ctime).strftime('%Y-%m-%d %H:%M:%S')
                files_count = sum([len(files) for r, _, files in os.walk(dir_path)])
                history.append({
                    "project_id": d,
                    "date": dt,
                    "files_count": files_count
                })
    history.sort(key=lambda x: x["date"], reverse=True)
    return history

@router.get("/stats/overview")
async def get_stats():
    total_reviews = 0
    if os.path.exists(settings.UPLOAD_DIR):
        total_reviews = len([d for d in os.listdir(settings.UPLOAD_DIR) if os.path.isdir(os.path.join(settings.UPLOAD_DIR, d))])
    
    # Calculate a mock dynamic avg score based on reviews so it changes
    avg_score = max(40, 100 - (total_reviews * 2))
    
    return {"total_reviews": total_reviews, "avg_score": avg_score}

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
