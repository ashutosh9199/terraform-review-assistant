provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "bad_rg" {
  name     = "rg-vulnerable"
  location = "East US"
  # Missing Tags!
}

resource "azurerm_storage_account" "bad_sa" {
  name                     = "badsastorage"
  resource_group_name      = azurerm_resource_group.bad_rg.name
  location                 = azurerm_resource_group.bad_rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  
  # VULNERABILITY: Public network access is enabled
  public_network_access_enabled = true
  
  # VULNERABILITY: Allow public blob access
  allow_blob_public_access = true
}

resource "azurerm_kubernetes_cluster" "bad_aks" {
  name                = "aks-vulnerable"
  location            = azurerm_resource_group.bad_rg.location
  resource_group_name = azurerm_resource_group.bad_rg.name
  dns_prefix          = "badaks"

  default_node_pool {
    name       = "default"
    node_count = 1
    vm_size    = "Standard_D2_v2"
  }

  identity {
    type = "SystemAssigned"
  }

  # VULNERABILITY: RBAC is explicitly disabled
  role_based_access_control_enabled = false
}

resource "azurerm_virtual_machine" "bad_vm" {
  name                  = "vm-oversized"
  location              = azurerm_resource_group.bad_rg.location
  resource_group_name   = azurerm_resource_group.bad_rg.name
  network_interface_ids = []
  vm_size               = "Standard_DS4_v2" # COST ISSUE: Very large VM SKU

  storage_os_disk {
    name              = "myosdisk1"
    caching           = "ReadWrite"
    create_option     = "FromImage"
    managed_disk_type = "Standard_LRS"
  }
}
