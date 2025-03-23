terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "fiap-terraform-state"
    key            = "db-infra/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "fiap-terraform-locks"
    encrypt        = true
  }

  required_version = ">= 1.0.0"
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Environment = var.environment
      Project     = "FIAP-Tech-Challenge"
      ManagedBy   = "Terraform"
    }
  }
} 