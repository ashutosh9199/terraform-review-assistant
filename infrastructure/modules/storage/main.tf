resource "azurerm_storage_account" "sa" {
  name                     = var.storage_account_name
  resource_group_name      = var.resource_group_name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  public_network_access_enabled = false
  tags                     = var.tags
}

variable "storage_account_name" {}
variable "location" {}
variable "resource_group_name" {}
variable "tags" {}
