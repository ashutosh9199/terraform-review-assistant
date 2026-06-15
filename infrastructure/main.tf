provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "main" {
  name     = var.resource_group_name
  location = var.location
  tags     = var.tags
}

module "key_vault" {
  source              = "./modules/key_vault"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  kv_name             = var.key_vault_name
  tenant_id           = var.tenant_id
  tags                = var.tags
}

module "storage" {
  source              = "./modules/storage"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  storage_account_name= var.storage_account_name
  tags                = var.tags
}

module "database" {
  source              = "./modules/database"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  sql_server_name     = var.sql_server_name
  database_name       = var.database_name
  admin_username      = var.admin_username
  admin_password      = var.admin_password
  tags                = var.tags
}

module "app_service" {
  source              = "./modules/app_service"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  app_service_plan_name = var.app_service_plan_name
  web_app_name        = var.web_app_name
  tags                = var.tags
}
