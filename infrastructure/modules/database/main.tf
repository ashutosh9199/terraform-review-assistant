resource "azurerm_mssql_server" "sql" {
  name                         = var.sql_server_name
  resource_group_name          = var.resource_group_name
  location                     = var.location
  version                      = "12.0"
  administrator_login          = var.admin_username
  administrator_login_password = var.admin_password
  tags                         = var.tags
}

resource "azurerm_mssql_database" "db" {
  name      = var.database_name
  server_id = azurerm_mssql_server.sql.id
  tags      = var.tags
}

variable "sql_server_name" {}
variable "database_name" {}
variable "admin_username" {}
variable "admin_password" {}
variable "location" {}
variable "resource_group_name" {}
variable "tags" {}
