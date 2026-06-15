resource "azurerm_service_plan" "asp" {
  name                = var.app_service_plan_name
  resource_group_name = var.resource_group_name
  location            = var.location
  os_type             = "Linux"
  sku_name            = "P1v2"
  tags                = var.tags
}

resource "azurerm_linux_web_app" "app" {
  name                = var.web_app_name
  resource_group_name = var.resource_group_name
  location            = var.location
  service_plan_id     = azurerm_service_plan.asp.id

  site_config {
    always_on = true
  }

  tags = var.tags
}

variable "app_service_plan_name" {}
variable "web_app_name" {}
variable "location" {}
variable "resource_group_name" {}
variable "tags" {}
