variable "subscription_id" {
  description = "Azure subscription ID"
  type        = string
  sensitive   = true
}

variable "tenant_id" {
  description = "Azure tenant ID"
  type        = string
  sensitive   = true
}

variable "client_id" {
  description = "Service Principal Client ID"
  type        = string
  sensitive   = true
  default     = "" # Leave empty for user account
}

variable "client_secret" {
  description = "Service Principal Client Secret"
  type        = string
  sensitive   = true
  default     = "" # Leave empty for user account
}

variable "resource_group_name" {
  description = "Resource group name"
  type        = string
  default     = "rg-aiops-dev"
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "francecentral"
}

variable "aks_cluster_name" {
  description = "Name of the AKS cluster"
  type        = string
  default     = "aks-aiops-dev"

  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{0,44}$", var.aks_cluster_name))
    error_message = "AKS name must be 1-45 chars, start with letter, contain only lowercase letters, numbers, and hyphens."
  }
}

variable "aks_node_count" {
  description = "Number of AKS worker nodes (1 for dev, 3+ for prod)"
  type        = number
  default     = 1

  validation {
    condition     = var.aks_node_count >= 1 && var.aks_node_count <= 10
    error_message = "Node count must be between 1 and 10 for cost control."
  }
}

variable "aks_vm_size" {
  description = "VM size for AKS nodes"
  type        = string
  default     = "Standard_B2s"

  validation {
    condition = contains([
      "Standard_B2s",    # Cheap dev
      "Standard_D2s_v3", # General purpose
      "Standard_F2s_v2"  # Compute optimized
    ], var.aks_vm_size)
    error_message = "VM size must be one of: Standard_B2s, Standard_D2s_v3, Standard_F2s_v2."
  }
}

variable "aks_dns_prefix" {
  description = "DNS prefix for AKS cluster"
  type        = string
  default     = "aiops-dev"

  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{0,8}$", var.aks_dns_prefix))
    error_message = "DNS prefix must be 1-9 chars, start with letter, contain only lowercase letters, numbers, and hyphens."
  }
}

variable "acr_name" {
  description = "Name for Azure Container Registry"
  type        = string
  default     = "acraioopsdev"

  validation {
    condition     = can(regex("^[a-z0-9]{5,50}$", var.acr_name))
    error_message = "ACR name must be 5-50 chars, lowercase letters and numbers only."
  }
}