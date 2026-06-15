output "resource_group_name" {
  description = "Resource group name."
  value       = module.resource_group.name
}

output "front_door_endpoint_hostname" {
  description = "Azure Front Door endpoint hostname."
  value       = module.edge.front_door_endpoint_hostname
}

output "application_gateway_public_fqdn" {
  description = "Application Gateway public FQDN used as the Front Door origin."
  value       = module.edge.application_gateway_public_fqdn
}

output "app_service_name" {
  description = "App Service name."
  value       = module.app_service.name
}

output "app_service_default_hostname" {
  description = "App Service default hostname. This resolves privately from the VNet after private endpoint DNS is linked."
  value       = module.app_service.default_hostname
}

output "postgresql_server_fqdn" {
  description = "Private PostgreSQL Flexible Server FQDN."
  value       = module.database.server_fqdn
}

output "key_vault_uri" {
  description = "Key Vault URI."
  value       = module.backend_services.key_vault_uri
}

output "servicebus_namespace_name" {
  description = "Service Bus namespace name."
  value       = module.backend_services.servicebus_namespace_name
}

output "storage_account_name" {
  description = "Storage account name."
  value       = module.backend_services.storage_account_name
}

output "ai_service_endpoint" {
  description = "Azure AI/Cognitive Service endpoint."
  value       = module.backend_services.ai_service_endpoint
}

output "log_analytics_workspace_id" {
  description = "Log Analytics Workspace resource ID."
  value       = module.monitoring.log_analytics_workspace_id
}
