import json
from models.domain import ReviewReport

class ReportingService:
    def __init__(self):
        pass

    def generate_json_report(self, report: ReviewReport, filepath: str):
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report.model_dump_json(indent=4))

    def generate_markdown_report(self, report: ReviewReport) -> str:
        md = f"# AI-Powered Terraform Review Assessment\n\n"
        md += f"## Overall Infrastructure Score: {report.overall_score}/100\n\n"
        md += f"- **Security**: {report.security.score}/100 ({report.security.findings_count} findings)\n"
        md += f"- **Cost**: {report.cost.score}/100 ({report.cost.findings_count} findings)\n"
        md += f"- **Governance**: {report.governance.score}/100 ({report.governance.findings_count} findings)\n"
        md += f"- **Operations**: {report.operations.score}/100 ({report.operations.findings_count} findings)\n\n"
        
        md += "## Detailed Findings\n"
        for idx, finding in enumerate(report.findings):
            md += f"### {idx+1}. {finding.issue} ({finding.risk_level} Risk - {finding.category})\n"
            md += f"- **Resource**: {finding.resource_type} ({finding.resource_name})\n"
            md += f"- **Impact**: {finding.business_impact}\n"
            md += f"- **Recommendation**: {finding.recommendation}\n"
            if finding.code_example:
                md += f"```hcl\n{finding.code_example}\n```\n"
            md += "\n"
        return md
