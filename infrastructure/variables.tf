variable "location" { default = "East US" }
variable "resource_group_name" { default = "rg-terraform-review-assistant" }
variable "key_vault_name" { default = "kv-tfa-assistant" }
variable "tenant_id" {}
variable "storage_account_name" { default = "sttfaassistant" }
variable "sql_server_name" { default = "sql-tfa-assistant" }
variable "database_name" { default = "sqldb-tfa-assistant" }
variable "admin_username" { default = "sqladmin" }
variable "admin_password" {}
variable "app_service_plan_name" { default = "asp-tfa-assistant" }
variable "web_app_name" { default = "app-tfa-assistant" }
variable "tags" {
  type = map(string)
  default = {
    Environment = "Production"
    Project     = "AI Review Assistant"
  }
}
