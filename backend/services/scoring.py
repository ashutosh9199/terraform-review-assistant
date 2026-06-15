from typing import List
from models.domain import Finding, ReviewReport, ScoreCategory

class ScoringEngine:
    def __init__(self):
        pass

    def calculate_scores(self, findings: List[Finding]) -> ReviewReport:
        # Base scores
        scores = {
            "Security": 100,
            "Cost": 100,
            "Governance": 100,
            "Operations": 100
        }
        counts = {
            "Security": 0,
            "Cost": 0,
            "Governance": 0,
            "Operations": 0
        }
        
        # Deduct points based on risk
        deductions = {
            "High": 15,
            "Medium": 5,
            "Low": 2
        }
        
        for finding in findings:
            cat = finding.category
            if cat in scores:
                scores[cat] -= deductions.get(finding.risk_level, 0)
                counts[cat] += 1
                
        # Floor at 0
        for cat in scores:
            scores[cat] = max(0, scores[cat])
            
        overall = sum(scores.values()) // 4
        
        return ReviewReport(
            overall_score=overall,
            security=ScoreCategory(score=scores["Security"], findings_count=counts["Security"]),
            cost=ScoreCategory(score=scores["Cost"], findings_count=counts["Cost"]),
            governance=ScoreCategory(score=scores["Governance"], findings_count=counts["Governance"]),
            operations=ScoreCategory(score=scores["Operations"], findings_count=counts["Operations"]),
            findings=findings
        )
