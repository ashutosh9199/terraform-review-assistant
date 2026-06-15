from typing import List
from models.domain import Resource, Finding

class RuleEngine:
    def __init__(self):
        pass

    def analyze(self, resources: List[Resource]) -> List[Finding]:
        findings = []
        
        if len(resources) == 0:
            findings.append(Finding(
                resource_type="file",
                resource_name="upload",
                issue="No actionable Terraform resources or modules found",
                risk_level="Low",
                category="Operations",
                recommendation="Upload a file containing standard 'resource' or 'module' blocks. Files with only outputs or variables cannot be analyzed for infrastructure security.",
                business_impact="Engine bypassed due to lack of scanable infrastructure blocks.",
                code_example='resource "azurerm_resource_group" "rg" {}'
            ))
            return findings

        for res in resources:
            if res.resource_type == "azurerm_storage_account":
                findings.extend(self._check_storage_account(res))
            elif res.resource_type == "azurerm_kubernetes_cluster":
                findings.extend(self._check_aks(res))
            elif res.resource_type == "azurerm_public_ip":
                findings.append(Finding(
                    resource_type=res.resource_type,
                    resource_name=res.name,
                    issue="Public IP addresses expose resources directly to the internet",
                    risk_level="High",
                    category="Security",
                    recommendation="Remove Public IP and route traffic through a Load Balancer, App Gateway, or Azure Firewall.",
                    business_impact="Significantly increases the attack surface.",
                    code_example="# Remove this resource"
                ))
            elif res.resource_type == "azurerm_linux_virtual_machine":
                if "tags" not in res.properties:
                    findings.append(Finding(
                        resource_type=res.resource_type,
                        resource_name=res.name,
                        issue="Virtual Machine is missing tags",
                        risk_level="Low",
                        category="Governance",
                        recommendation="Add required tags (Environment, Project, Owner) to the VM.",
                        business_impact="Reduces cost visibility and operational governance.",
                        code_example='tags = {\n  Environment = "Production"\n}'
                    ))
            elif res.resource_type == "azurerm_key_vault_secret":
                findings.append(Finding(
                    resource_type=res.resource_type,
                    resource_name=res.name,
                    issue="Hardcoded Secret Value in Terraform",
                    risk_level="High",
                    category="Security",
                    recommendation="Avoid passing secret values directly in Terraform state. Use Azure Key Vault references or environment variables.",
                    business_impact="Secrets can be exposed in plaintext within the tfstate file.",
                    code_example='value = "@Microsoft.KeyVault(SecretUri=...)"'
                ))
            elif res.resource_type == "module":
                findings.append(Finding(
                    resource_type=res.resource_type,
                    resource_name=res.name,
                    issue="Module version not pinned",
                    risk_level="Medium",
                    category="Operations",
                    recommendation="Always pin Terraform modules to a specific version or git commit hash.",
                    business_impact="Upstream module changes could break infrastructure unexpectedly.",
                    code_example='source = "git::https://...v1.0.0"'
                ))
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
