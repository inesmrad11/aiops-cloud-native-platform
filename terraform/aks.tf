# ------------------------------------------------------------
# Log Analytics (AKS Monitoring)
# ------------------------------------------------------------

resource "azurerm_log_analytics_workspace" "main" {
  name                = "log-aiops-dev"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  sku                 = "PerGB2018"
  retention_in_days   = 30

  tags = {
    project     = "aiops"
    environment = "dev"
    managed-by  = "terraform"
  }
}

# ------------------------------------------------------------
# Azure Kubernetes Service (AKS)
# ------------------------------------------------------------

resource "azurerm_kubernetes_cluster" "main" {
  name                = var.aks_cluster_name
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  dns_prefix          = var.aks_dns_prefix

  default_node_pool {
    name           = "system"
    node_count     = var.aks_node_count
    vm_size        = var.aks_vm_size
    vnet_subnet_id = azurerm_subnet.aks.id
  }

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin    = "azure"
    network_policy    = "calico"
    load_balancer_sku = "standard"

    service_cidr = "10.1.0.0/16"       # <-- Choisir une plage libre
    dns_service_ip = "10.1.0.10"       # <-- Doit être dans service_cidr
    docker_bridge_cidr = "172.17.0.1/16" # optionnel
}

  oms_agent {
    log_analytics_workspace_id = azurerm_log_analytics_workspace.main.id
  }

  role_based_access_control_enabled = true

  tags = {
    project     = "aiops"
    environment = "dev"
    managed-by  = "terraform"
  }
}