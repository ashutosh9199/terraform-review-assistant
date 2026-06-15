from typing import List
from models.domain import Resource, Finding

class RuleEngine:
    def __init__(self):
        pass

    def analyze(self, resources: List[Resource]) -> List[Finding]:
        findings = []
        for res in resources:
            if res.resource_type == "azurerm_storage_account":
                findings.extend(self._check_storage_account(res))
            elif res.resource_type == "azurerm_kubernetes_cluster":
                findings.extend(self._check_aks(res))
            # add more checks here
        return findings

    def _check_storage_account(self, res: Resource) -> List[Finding]:
        findings = []
        # Check public access
        # In HCL, boolean values are parsed as Python bools.
        public_access = res.properties.get("public_network_access_enabled", True)
        blob_public_access = res.properties.get("allow_blob_public_access", True)
        
        if public_access is True or blob_public_access is True:
            findings.append(Finding(
                resource_type=res.resource_type,
                resource_name=res.name,
                issue="Storage account allows public access",
                risk_level="High",
                category="Security",
                recommendation="Disable public network access and use private endpoints.",
                business_impact="Reduces risk of unauthorized data exposure.",
                code_example='public_network_access_enabled = false\nallow_blob_public_access = false'
            ))
        return findings
        
    def _check_aks(self, res: Resource) -> List[Finding]:
        findings = []
        # basic check
        if "role_based_access_control_enabled" not in res.properties or res.properties.get("role_based_access_control_enabled") != True:
            findings.append(Finding(
                resource_type=res.resource_type,
                resource_name=res.name,
                issue="AKS RBAC Disabled",
                risk_level="High",
                category="Security",
                recommendation="Enable RBAC for AKS cluster.",
                business_impact="Ensures least privilege access to the Kubernetes API.",
                code_example='role_based_access_control_enabled = true'
            ))
        return findings
