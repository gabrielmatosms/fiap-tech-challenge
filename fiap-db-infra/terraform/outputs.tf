output "db_instance_id" {
  description = "The ID of the RDS instance"
  value       = aws_db_instance.db_instance.id
}

output "db_instance_address" {
  description = "The hostname of the RDS instance"
  value       = aws_db_instance.db_instance.address
}

output "db_instance_endpoint" {
  description = "The connection endpoint of the RDS instance"
  value       = aws_db_instance.db_instance.endpoint
}

output "db_instance_name" {
  description = "The database name"
  value       = aws_db_instance.db_instance.db_name
}

output "db_secret_arn" {
  description = "The ARN of the secret storing the database credentials"
  value       = aws_secretsmanager_secret.db_credentials.arn
}

output "db_security_group_id" {
  description = "The ID of the security group for the RDS instance"
  value       = aws_security_group.db_security_group.id
}

output "db_subnet_group_id" {
  description = "The ID of the DB subnet group"
  value       = aws_db_subnet_group.db_subnet_group.id
}

output "db_parameter_group_id" {
  description = "The ID of the DB parameter group"
  value       = aws_db_parameter_group.db_parameter_group.id
} 