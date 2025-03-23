provider "aws" {
  region = var.region
  
  default_tags {
    tags = {
      Project     = "fiap-tech-challenge"
      Environment = var.environment
      ManagedBy   = "terraform"
    }
  }
}

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.16"
    }
  }
  
  backend "s3" {
    bucket         = "fiap-terraform-state"
    key            = "k8s-infra/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-lock"
  }
} 