# FIAP Kubernetes Infrastructure

This repository contains the Terraform configuration for provisioning the Kubernetes infrastructure for the FIAP Tech Challenge project.

## Architecture

The infrastructure consists of:

1. Amazon EKS (Elastic Kubernetes Service) cluster
2. VPC with public and private subnets across multiple availability zones
3. Security groups for node groups and control plane
4. IAM roles and policies for EKS

## Prerequisites

- AWS CLI configured with appropriate credentials
- Terraform 1.0.0 or later
- kubectl
- AWS IAM Authenticator

## Getting Started

### Initialize Terraform

```bash
cd terraform
terraform init
```

### Plan and Apply

```bash
# Preview the changes
terraform plan

# Apply the changes
terraform apply
```

### Connect to the Cluster

After the cluster is created, you can connect to it using:

```bash
aws eks update-kubeconfig --name <cluster-name> --region <region>
```

Replace `<cluster-name>` and `<region>` with the output values from Terraform.

### Deploy the Application

To deploy the application to the cluster:

```bash
cd scripts
./deploy.sh <environment> <ecr-repository-url>
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
  - `network.tf`: VPC and network configuration
  - `eks.tf`: EKS cluster configuration
  - `iam.tf`: IAM roles and policies
- `kubernetes/`: Kubernetes manifest files
  - `deployments/`: Deployment configurations
  - `services/`: Service configurations
  - `ingress/`: Ingress configurations
- `scripts/`: Utility scripts
  - `deploy.sh`: Script to deploy the application to the cluster

## Remote State

The Terraform state is stored in an S3 bucket with DynamoDB for state locking. The backend configuration is in `provider.tf`.

## Variables

Key variables to configure:

- `cluster_name`: Name of the EKS cluster
- `region`: AWS region to deploy resources
- `environment`: Environment name (dev, qa, production)
- Node group configuration: instance types, sizes, etc.

## Security Considerations

- The EKS cluster has both private and public endpoint access
- Node groups run in private subnets with outbound internet access via NAT Gateway
- Security groups are configured to allow only necessary communication

## Contributing

1. Create a feature branch
2. Make your changes
3. Create a pull request for review
4. The Terraform Plan workflow will validate your changes

## License

[MIT License](LICENSE) 