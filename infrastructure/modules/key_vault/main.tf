resource "azurerm_key_vault" "kv" {
  name                        = var.kv_name
  location                    = var.location
  resource_group_name         = var.resource_group_name
  tenant_id                   = var.tenant_id
  sku_name                    = "standard"
  purge_protection_enabled    = true
  tags                        = var.tags
}

variable "kv_name" {}
variable "location" {}
variable "resource_group_name" {}
variable "tenant_id" {}
variable "tags" {}
