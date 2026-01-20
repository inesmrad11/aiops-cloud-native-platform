# ------------------------------------------------------------
# Outputs
# ------------------------------------------------------------

output "aks_name" {
  description = "AKS cluster name"
  value       = azurerm_kubernetes_cluster.main.name
}

output "aks_resource_group" {
  description = "AKS resource group"
  value       = azurerm_kubernetes_cluster.main.resource_group_name
}

output "acr_login_server" {
  description = "ACR login server"
  value       = azurerm_container_registry.main.login_server
}

output "kubeconfig_raw" {
  description = "Raw kubeconfig (DEV ONLY)"
  value       = azurerm_kubernetes_cluster.main.kube_config_raw
  sensitive   = true
}