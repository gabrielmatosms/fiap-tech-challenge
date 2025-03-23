# FIAP Database Infrastructure

This repository contains the Terraform configuration for provisioning the database infrastructure for the FIAP Tech Challenge project.

## Architecture

The infrastructure consists of:

1. Amazon RDS PostgreSQL database
2. Security groups to control access to the database
3. Database subnets and subnet groups
4. Database parameter group for PostgreSQL configuration
5. IAM roles and policies for database monitoring
6. Secrets Manager for secure credential storage

## Prerequisites

- AWS CLI configured with appropriate credentials
- Terraform 1.0.0 or later
- PostgreSQL client (psql) for migrations

## Getting Started

### Initialize Terraform

```bash
cd terraform
terraform init
```

### Plan and Apply

```bash
# Preview the changes
terraform plan -var="db_password=<your-secure-password>"

# Apply the changes
terraform apply -var="db_password=<your-secure-password>"
```

### Database Migrations

To apply database migrations:

```bash
cd scripts
./migrate.sh <db-host> <db-port> <db-name> <db-user> <db-password>
```

## CI/CD

This repository is configured with GitHub Actions workflows for continuous integration and deployment:

1. **Terraform Plan**: Runs on pull requests to validate changes
2. **Terraform Apply**: Runs on push to main to apply changes to infrastructure

## Folder Structure

- `terraform/`: Terraform configuration files
  - `provider.tf`: AWS provider configuration
  - `variables.tf`: Input variables
  - `outputs.tf`: Output values
  - `database.tf`: RDS database configuration
- `migrations/`: Database migration files
  - `V1__initial_schema.sql`: Initial database schema
  - `V2__seed_data.sql`: Seed data for development
- `scripts/`: Utility scripts
  - `migrate.sh`: Script to apply database migrations

## Remote State

The Terraform state is stored in an S3 bucket with DynamoDB for state locking. The backend configuration is in `provider.tf`.

## Variables

Key variables to configure:

- `db_name`: Name of the RDS database
- `db_username`: Username for the database
- `db_password`: Password for the database (should be kept secret)
- `db_instance_class`: Instance class for the database
- `multi_az`: Whether to enable Multi-AZ deployment

## Security Considerations

- The database is deployed in a private subnet and is not publicly accessible
- The security group allows only the application servers to connect to the database
- Database credentials are stored in AWS Secrets Manager
- Storage is encrypted at rest

## Contributing

1. Create a feature branch
2. Make your changes
3. Create a pull request for review
4. The Terraform Plan workflow will validate your changes

## License

[MIT License](LICENSE) 