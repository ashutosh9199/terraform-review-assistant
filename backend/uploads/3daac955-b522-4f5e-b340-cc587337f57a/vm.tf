terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "4.71.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# ------------------------
# RESOURCE GROUP
# ------------------------
resource "azurerm_resource_group" "rg" {
  name     = "ashutosh-resources"
  location = "Central India"
}

# ------------------------
# VNET
# ------------------------
resource "azurerm_virtual_network" "vnet" {
  name                = "ashutosh-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
}

# ------------------------
# SUBNETS
# ------------------------

# Public Subnet
resource "azurerm_subnet" "public_subnet" {
  name                 = "public-subnet"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.1.0/24"]
}

# Private Subnet
resource "azurerm_subnet" "private_subnet" {
  name                 = "private-subnet"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.2.0/24"]
}

# ------------------------
# PUBLIC VM (DIRECT INTERNET ACCESS)
# ------------------------

resource "azurerm_public_ip" "public_vm_ip" {
  name                = "public-vm-ip"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  allocation_method   = "Static"
}

resource "azurerm_network_interface" "public_nic" {
  name                = "public-nic"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  ip_configuration {
    name                          = "public-ipconfig"
    subnet_id                     = azurerm_subnet.public_subnet.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.public_vm_ip.id
  }
}

resource "azurerm_linux_virtual_machine" "public_vm" {
  name                = "public-vm"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  size                = "Standard_B2ats_v2"
  admin_username      = "ashutosh"
  admin_password      = "7319@Ashutosh"
  disable_password_authentication = false

  network_interface_ids = [
    azurerm_network_interface.public_nic.id
  ]

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts"
    version   = "latest"
  }
}

# ------------------------
# PRIVATE VM (NO PUBLIC IP)
# ------------------------

resource "azurerm_network_interface" "private_nic" {
  name                = "private-nic"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  ip_configuration {
    name                          = "private-ipconfig"
    subnet_id                     = azurerm_subnet.private_subnet.id
    private_ip_address_allocation = "Dynamic"
  }
}

resource "azurerm_linux_virtual_machine" "private_vm" {
  name                = "private-vm"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  size                = "Standard_B2ats_v2"
  admin_username      = "ashutosh"
  admin_password      = "7319@Ashutosh"
  disable_password_authentication = false

  network_interface_ids = [
    azurerm_network_interface.private_nic.id
  ]

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts"
    version   = "latest"
  }
}

# ------------------------
# NAT GATEWAY (OUTBOUND ONLY)
# ------------------------

resource "azurerm_public_ip" "nat_ip" {
  name                = "nat-ip"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  allocation_method   = "Static"
  sku                 = "Standard"
}

resource "azurerm_nat_gateway" "nat" {
  name                = "nat-gateway"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku_name            = "Standard"
}

resource "azurerm_nat_gateway_public_ip_association" "nat_assoc" {
  nat_gateway_id       = azurerm_nat_gateway.nat.id
  public_ip_address_id = azurerm_public_ip.nat_ip.id
}

resource "azurerm_subnet_nat_gateway_association" "nat_attach" {
  subnet_id      = azurerm_subnet.private_subnet.id
  nat_gateway_id = azurerm_nat_gateway.nat.id
}

# ------------------------
# LOAD BALANCER (INBOUND TO PRIVATE VM)
# ------------------------

resource "azurerm_public_ip" "lb_ip" {
  name                = "lb-ip"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  allocation_method   = "Static"
  sku                 = "Standard"
}

resource "azurerm_lb" "lb" {
  name                = "public-lb"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku                 = "Standard"

  frontend_ip_configuration {
    name                 = "frontend"
    public_ip_address_id = azurerm_public_ip.lb_ip.id
  }
}

resource "azurerm_lb_backend_address_pool" "backend" {
  loadbalancer_id = azurerm_lb.lb.id
  name            = "backend-pool"
}

resource "azurerm_network_interface_backend_address_pool_association" "assoc" {
  network_interface_id    = azurerm_network_interface.private_nic.id
  ip_configuration_name   = "private-ipconfig"
  backend_address_pool_id = azurerm_lb_backend_address_pool.backend.id
}

resource "azurerm_lb_probe" "probe" {
  loadbalancer_id = azurerm_lb.lb.id
  name            = "http-probe"
  port            = 80
}

resource "azurerm_lb_rule" "rule" {
  loadbalancer_id                = azurerm_lb.lb.id
  name                           = "http-rule"
  protocol                       = "Tcp"
  frontend_port                  = 80
  backend_port                   = 80
  frontend_ip_configuration_name = "frontend"
  backend_address_pool_ids       = [azurerm_lb_backend_address_pool.backend.id]
  probe_id                       = azurerm_lb_probe.probe.id
}
