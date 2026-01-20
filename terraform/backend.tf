terraform {
  required_version = ">= 1.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }

  backend "azurerm" {
    resource_group_name  = "rg-aiops-dev"
    storage_account_name = "staiopsterraform"
    container_name       = "tfstate"
    key                  = "aiops-dev.tfstate"
  }
}