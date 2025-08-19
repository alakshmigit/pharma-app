#!/bin/bash

# Pharmaceutical Order Management System - AWS Deployment Script
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="pharma-order-mgmt"
AWS_REGION="us-east-1"

echo -e "${BLUE}🚀 Starting deployment of Pharmaceutical Order Management System${NC}"

# Check prerequisites
echo -e "${YELLOW}📋 Checking prerequisites...${NC}"

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo -e "${RED}❌ AWS CLI is not installed. Please install it first.${NC}"
    exit 1
fi

# Check if Terraform is installed
if ! command -v terraform &> /dev/null; then
    echo -e "${RED}❌ Terraform is not installed. Please install it first.${NC}"
    exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed. Please install it first.${NC}"
    exit 1
fi

# Check AWS credentials
if ! aws sts get-caller-identity &> /dev/null; then
    echo -e "${RED}❌ AWS credentials not configured. Please run 'aws configure' first.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ All prerequisites met${NC}"

# Step 1: Initialize and apply Terraform
echo -e "${YELLOW}🏗️  Step 1: Deploying infrastructure with Terraform...${NC}"
cd terraform

# Copy example tfvars if it doesn't exist
if [ ! -f "terraform.tfvars" ]; then
    echo -e "${YELLOW}📝 Creating terraform.tfvars from example...${NC}"
    cp terraform.tfvars.example terraform.tfvars
    echo -e "${YELLOW}⚠️  Please edit terraform.tfvars with your desired configuration before continuing.${NC}"
    read -p "Press Enter to continue after editing terraform.tfvars..."
fi

# Initialize Terraform
terraform init

# Plan the deployment
echo -e "${YELLOW}📋 Planning Terraform deployment...${NC}"
terraform plan

# Apply the infrastructure
echo -e "${YELLOW}🚀 Applying Terraform configuration...${NC}"
terraform apply -auto-approve

# Get outputs
ECR_BACKEND_REPO=$(terraform output -raw ecr_backend_repository_url)
ECR_FRONTEND_REPO=$(terraform output -raw ecr_frontend_repository_url)
ECS_CLUSTER=$(terraform output -raw ecs_cluster_name)

echo -e "${GREEN}✅ Infrastructure deployed successfully${NC}"
echo -e "${BLUE}📊 ECR Backend Repository: ${ECR_BACKEND_REPO}${NC}"
echo -e "${BLUE}📊 ECR Frontend Repository: ${ECR_FRONTEND_REPO}${NC}"

cd ..

# Step 2: Build and push Docker images
echo -e "${YELLOW}🐳 Step 2: Building and pushing Docker images...${NC}"

# Login to ECR
echo -e "${YELLOW}🔐 Logging into ECR...${NC}"
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_BACKEND_REPO

# Build and push backend image
echo -e "${YELLOW}🔨 Building backend Docker image...${NC}"
cd backend
docker build -t $PROJECT_NAME-backend .
docker tag $PROJECT_NAME-backend:latest $ECR_BACKEND_REPO:latest
echo -e "${YELLOW}📤 Pushing backend image to ECR...${NC}"
docker push $ECR_BACKEND_REPO:latest
cd ..

# Build and push frontend image
echo -e "${YELLOW}🔨 Building frontend Docker image...${NC}"
cd frontend
docker build -t $PROJECT_NAME-frontend .
docker tag $PROJECT_NAME-frontend:latest $ECR_FRONTEND_REPO:latest
echo -e "${YELLOW}📤 Pushing frontend image to ECR...${NC}"
docker push $ECR_FRONTEND_REPO:latest
cd ..

echo -e "${GREEN}✅ Docker images built and pushed successfully${NC}"

# Step 3: Update ECS services
echo -e "${YELLOW}🔄 Step 3: Updating ECS services...${NC}"

# Force new deployment of backend service
aws ecs update-service \
    --cluster $ECS_CLUSTER \
    --service $PROJECT_NAME-backend \
    --force-new-deployment \
    --region $AWS_REGION

# Force new deployment of frontend service
aws ecs update-service \
    --cluster $ECS_CLUSTER \
    --service $PROJECT_NAME-frontend \
    --force-new-deployment \
    --region $AWS_REGION

echo -e "${GREEN}✅ ECS services updated successfully${NC}"

# Step 4: Wait for services to be stable
echo -e "${YELLOW}⏳ Step 4: Waiting for services to stabilize...${NC}"

aws ecs wait services-stable \
    --cluster $ECS_CLUSTER \
    --services $PROJECT_NAME-backend \
    --region $AWS_REGION

aws ecs wait services-stable \
    --cluster $ECS_CLUSTER \
    --services $PROJECT_NAME-frontend \
    --region $AWS_REGION

echo -e "${GREEN}✅ Services are stable and running${NC}"

# Step 5: Display final information
echo -e "${YELLOW}📋 Step 5: Deployment Summary${NC}"
cd terraform

APPLICATION_URL=$(terraform output -raw application_url)
BACKEND_API_URL=$(terraform output -raw backend_api_url)
BACKEND_DOCS_URL=$(terraform output -raw backend_docs_url)

echo -e "${GREEN}🎉 Deployment completed successfully!${NC}"
echo -e "${BLUE}📱 Application URL: ${APPLICATION_URL}${NC}"
echo -e "${BLUE}🔗 Backend API URL: ${BACKEND_API_URL}${NC}"
echo -e "${BLUE}📚 API Documentation: ${BACKEND_DOCS_URL}${NC}"
echo ""
echo -e "${YELLOW}⚠️  Note: It may take a few minutes for the application to be fully available.${NC}"
echo -e "${YELLOW}💡 You can monitor the deployment in the AWS ECS console.${NC}"

cd ..

echo -e "${GREEN}✨ Pharmaceutical Order Management System deployed successfully! ✨${NC}"