from typing import List
from models.domain import Resource, Finding
from core.config import settings
import json
from openai import AsyncAzureOpenAI
import os

class AIReviewer:
    def __init__(self):
        self.client = None
        if settings.AZURE_OPENAI_API_KEY and settings.AZURE_OPENAI_API_KEY != "your-azure-openai-key":
            self.client = AsyncAzureOpenAI(
                api_key=settings.AZURE_OPENAI_API_KEY,
                api_version="2023-05-15",
                azure_endpoint=settings.AZURE_OPENAI_ENDPOINT
            )

    async def analyze(self, resources: List[Resource]) -> List[Finding]:
        findings = []
        if not resources:
            return findings

        # Fallback to warning if API key is not configured yet
        if not self.client:
            findings.append(Finding(
                resource_type="system",
                resource_name="AI_Engine",
                issue="Azure OpenAI is not configured",
                risk_level="Low",
                category="Operations",
                recommendation="Please add your AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT to the backend/.env file to enable deep semantic AI scanning.",
                business_impact="Advanced AI threat detection is disabled. Falling back to static scanning only.",
                code_example=""
            ))
            return findings

        # Serialize resources for prompt
        resource_data = [{"type": r.resource_type, "name": r.name, "properties": r.properties} for r in resources]
        prompt = f"""
        You are an expert Cloud Security Architect. Review the following Terraform resources for security vulnerabilities, cost inefficiencies, and missing governance best practices.
        Return ONLY a JSON array of findings with the exact keys: 'resource_type', 'resource_name', 'issue', 'risk_level' (High/Medium/Low), 'category' (Security/Cost/Governance/Operations), 'recommendation', 'business_impact', 'code_example'.
        
        Terraform Resources:
        {json.dumps(resource_data, indent=2)}
        """

        try:
            response = await self.client.chat.completions.create(
                model=settings.AZURE_OPENAI_DEPLOYMENT_NAME or "gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a Terraform security expert. Only output raw JSON arrays."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )
            
            content = response.choices[0].message.content.strip()
            if content.startswith("```json"):
                content = content[7:-3]
            elif content.startswith("```"):
                content = content[3:-3]
            
            ai_results = json.loads(content)
            for res in ai_results:
                findings.append(Finding(
                    resource_type=res.get("resource_type", "unknown"),
                    resource_name=res.get("resource_name", "unknown"),
                    issue=res.get("issue", "Unknown AI finding"),
                    risk_level=res.get("risk_level", "Medium"),
                    category=res.get("category", "Security"),
                    recommendation=res.get("recommendation", "Review architecture"),
                    business_impact=res.get("business_impact", "Unknown"),
                    code_example=res.get("code_example", "")
                ))
        except Exception as e:
            print(f"AI Analysis Failed: {str(e)}")
            findings.append(Finding(
                resource_type="system",
                resource_name="AI_Engine",
                issue=f"AI Request Failed: {str(e)}",
                risk_level="Low",
                category="Operations",
                recommendation="Verify your Azure OpenAI credentials and deployment name in the .env file.",
                business_impact="Advanced AI threat detection could not complete.",
                code_example=""
            ))
            
        return findings
