# ------------------------------------------------------------
# Azure Container Registry (DEV)
# ------------------------------------------------------------

resource "random_integer" "acr_suffix" {
  min = 100
  max = 999
}

resource "azurerm_container_registry" "main" {
  name                = "${var.acr_name}${random_integer.acr_suffix.result}"
  resource_group_name = data.azurerm_resource_group.main.name
  location            = data.azurerm_resource_group.main.location
  sku                 = "Basic"

  admin_enabled = true # DEV ONLY — disable in production

  # retention_policy {
  #   days    = 7
  #   enabled = true
  # }

  tags = {
    project     = "aiops"
    environment = "dev"
    managed-by  = "terraform"
    purpose     = "container-images"
  }
}