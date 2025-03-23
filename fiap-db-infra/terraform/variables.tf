variable "aws_region" {
  description = "The AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "The deployment environment (dev, qa, prod)"
  type        = string
  default     = "dev"
}

variable "db_name" {
  description = "The name of the RDS database"
  type        = string
  default     = "fiapdb"
}

variable "db_username" {
  description = "The username for the RDS database"
  type        = string
  default     = "fiapuser"
  sensitive   = true
}

variable "db_password" {
  description = "The password for the RDS database"
  type        = string
  sensitive   = true
}

variable "db_instance_class" {
  description = "The instance class for the RDS database"
  type        = string
  default     = "db.t3.micro"
}

variable "db_allocated_storage" {
  description = "The allocated storage for the RDS database in GB"
  type        = number
  default     = 20
}

variable "db_max_allocated_storage" {
  description = "The maximum allocated storage for the RDS database in GB"
  type        = number
  default     = 100
}

variable "multi_az" {
  description = "Whether to deploy the RDS database in multiple availability zones"
  type        = bool
  default     = false
}

variable "vpc_id" {
  description = "The ID of the VPC to deploy the RDS database in"
  type        = string
}

variable "private_subnet_ids" {
  description = "The IDs of the private subnets to deploy the RDS database in"
  type        = list(string)
}

variable "app_security_group_id" {
  description = "The ID of the security group for the application server"
  type        = string
}

variable "backup_retention_period" {
  description = "The backup retention period in days"
  type        = number
  default     = 7
}

variable "deletion_protection" {
  description = "Whether to enable deletion protection for the RDS database"
  type        = bool
  default     = true
} 