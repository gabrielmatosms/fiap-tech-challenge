#!/bin/bash
set -e

# Variables
ENVIRONMENT=${1:-dev}
ECR_REPOSITORY_URL=${2}

# Check required variables
if [ -z "$ECR_REPOSITORY_URL" ]; then
  echo "ERROR: ECR_REPOSITORY_URL is required"
  echo "Usage: $0 <environment> <ecr_repository_url>"
  exit 1
fi

# Set AWS region
AWS_REGION=$(aws configure get region)
if [ -z "$AWS_REGION" ]; then
  AWS_REGION="us-east-1"
fi

# Get EKS cluster name from Terraform state
CLUSTER_NAME=$(terraform -chdir=../terraform output -raw cluster_name)

# Update kubeconfig
echo "Updating kubeconfig for cluster $CLUSTER_NAME in region $AWS_REGION"
aws eks update-kubeconfig --name $CLUSTER_NAME --region $AWS_REGION

# Process templates
echo "Processing Kubernetes templates for environment: $ENVIRONMENT"
mkdir -p ../kubernetes/processed

# Process deployment template
cat ../kubernetes/deployments/app-deployment.yaml | \
  sed "s|\${ECR_REPOSITORY_URL}|$ECR_REPOSITORY_URL|g" | \
  sed "s|\${ENVIRONMENT}|$ENVIRONMENT|g" \
  > ../kubernetes/processed/app-deployment.yaml

# Copy other templates
cp ../kubernetes/services/app-service.yaml ../kubernetes/processed/
cp ../kubernetes/ingress/app-ingress.yaml ../kubernetes/processed/

# Apply Kubernetes resources
echo "Applying Kubernetes resources"
kubectl apply -f ../kubernetes/processed/

# Wait for deployment to complete
echo "Waiting for deployment to complete..."
kubectl rollout status deployment/fiap-app

echo "Deployment completed successfully!" 