from typing import List
from models.domain import Resource, Finding
from core.config import settings
import json
# import openai

class AIReviewer:
    def __init__(self):
        # We would initialize openai client here using settings
        # openai.api_key = settings.AZURE_OPENAI_API_KEY
        # openai.api_base = settings.AZURE_OPENAI_ENDPOINT
        pass

    async def analyze(self, resources: List[Resource]) -> List[Finding]:
        # In a real implementation, we would stringify the resources and send to Azure OpenAI
        # For now, we mock some AI findings for demonstration
        findings = []
        
        # Mock AI finding based on resources
        for res in resources:
            if res.resource_type == "azurerm_virtual_machine" or res.resource_type == "azurerm_linux_virtual_machine":
                findings.append(Finding(
                    resource_type=res.resource_type,
                    resource_name=res.name,
                    issue="Oversized VM SKU potentially used",
                    risk_level="Medium",
                    category="Cost",
                    recommendation="Review VM usage and consider downscaling to a smaller SKU if CPU/Memory utilization is low.",
                    business_impact="Reduces unnecessary cloud spend.",
                    code_example='size = "Standard_B2s"'
                ))
        return findings
