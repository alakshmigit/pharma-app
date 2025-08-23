# AWS Deployment Guide - Pharmaceutical Order Management System

This guide provides comprehensive instructions for deploying your pharmaceutical order management system to AWS using Terraform, Docker, and ECS Fargate.

## 🏗️ AWS Architecture

The deployment creates a production-ready infrastructure with:

- **ECS Fargate**: Serverless container hosting for backend and frontend
- **RDS PostgreSQL**: Managed database with automated backups
- **Application Load Balancer**: High availability with health checks
- **VPC**: Secure networking with public/private subnets
- **ECR**: Container registry for Docker images
- **CloudWatch**: Centralized logging and monitoring

## 📋 Prerequisites

Before deploying, ensure you have:

### 1. AWS CLI Installed and Configured
```bash
# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Configure AWS credentials
aws configure
```

### 2. Terraform Installed
```bash
# macOS
brew install terraform

# Ubuntu/Debian
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform
```

### 3. Docker Installed
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# macOS
brew install docker
```

### 4. AWS Permissions
Your AWS user/role needs permissions for:
- ECS (Elastic Container Service)
- RDS (Relational Database Service)
- ECR (Elastic Container Registry)
- VPC, Subnets, Security Groups
- Application Load Balancer
- IAM Roles and Policies
- CloudWatch Logs

## 🚀 Quick Deployment (Automated)

### Step 1: Configure Deployment
```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
```

Edit `terraform.tfvars` with your configuration:
```hcl
# AWS Configuration
aws_region = "us-east-1"

# Project Configuration
project_name = "pharma-order-mgmt"
environment  = "prod"

# Database Configuration
db_instance_class = "db.t3.micro"
db_name          = "pharma_orders"
db_username      = "admin"
db_password      = "YourSecurePassword123!"

# ECS Configuration
backend_cpu     = 256
backend_memory  = 512
frontend_cpu    = 256
frontend_memory = 512
```

### Step 2: Run Automated Deployment
```bash
./deploy.sh
```

The script will:
1. ✅ Validate prerequisites
2. 🏗️ Deploy AWS infrastructure
3. 🐳 Build and push Docker images
4. 🚀 Deploy applications to ECS
5. ⏳ Wait for services to stabilize
6. 📋 Display access URLs

## 🔧 Manual Deployment (Step-by-Step)

### Step 1: Deploy Infrastructure
```bash
cd terraform

# Initialize Terraform
terraform init

# Review the deployment plan
terraform plan

# Deploy infrastructure
terraform apply
```

### Step 2: Build and Push Docker Images
```bash
# Get ECR repository URLs from Terraform output
ECR_BACKEND=$(terraform output -raw ecr_backend_repository_url)
ECR_FRONTEND=$(terraform output -raw ecr_frontend_repository_url)
AWS_REGION=$(terraform output -raw aws_region || echo "us-east-1")

# Login to ECR
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_BACKEND

# Build and push backend image
cd ../backend
docker build -t pharma-backend .
docker tag pharma-backend:latest $ECR_BACKEND:latest
docker push $ECR_BACKEND:latest

# Build and push frontend image
cd ../frontend
docker build -t pharma-frontend .
docker tag pharma-frontend:latest $ECR_FRONTEND:latest
docker push $ECR_FRONTEND:latest
```

### Step 3: Deploy to ECS
```bash
# Get cluster name
ECS_CLUSTER=$(terraform output -raw ecs_cluster_name)

# Update backend service
aws ecs update-service \
    --cluster $ECS_CLUSTER \
    --service pharma-order-mgmt-backend \
    --force-new-deployment \
    --region $AWS_REGION

# Update frontend service
aws ecs update-service \
    --cluster $ECS_CLUSTER \
    --service pharma-order-mgmt-frontend \
    --force-new-deployment \
    --region $AWS_REGION
```

### Step 4: Wait for Deployment
```bash
# Wait for services to stabilize
aws ecs wait services-stable \
    --cluster $ECS_CLUSTER \
    --services pharma-order-mgmt-backend \
    --region $AWS_REGION

aws ecs wait services-stable \
    --cluster $ECS_CLUSTER \
    --services pharma-order-mgmt-frontend \
    --region $AWS_REGION
```

## 🔗 Access Your Application

After successful deployment:

```bash
cd terraform
APPLICATION_URL=$(terraform output -raw application_url)
echo "🎉 Application URL: $APPLICATION_URL"
```

- **Main Application**: `http://your-alb-url/`
- **Backend API**: `http://your-alb-url/api/`
- **API Documentation**: `http://your-alb-url/docs`

## 📊 Infrastructure Components

### Networking
- **VPC**: 10.0.0.0/16 with DNS support
- **Public Subnets**: 2 subnets across AZs for ALB
- **Private Subnets**: 2 subnets across AZs for ECS/RDS
- **NAT Gateway**: Outbound internet access for private subnets
- **Internet Gateway**: Inbound access for public subnets

### Security Groups
- **ALB Security Group**: HTTP/HTTPS from internet
- **ECS Security Group**: Backend (8001) and Frontend (8501) from ALB
- **RDS Security Group**: PostgreSQL (5432) from ECS tasks only

### Database
- **Engine**: PostgreSQL 15.4
- **Instance**: db.t3.micro (burstable performance)
- **Storage**: 20GB GP2 with auto-scaling to 100GB
- **Backup**: 7-day retention with automated backups
- **Monitoring**: Enhanced monitoring enabled

### Container Services
- **ECS Cluster**: Fargate launch type
- **Backend Task**: 0.25 vCPU, 512MB memory
- **Frontend Task**: 0.25 vCPU, 512MB memory
- **Auto Scaling**: Manual scaling (can be automated)

## 💰 Cost Estimation

**Monthly AWS costs (US East 1)**:

| Service | Configuration | Estimated Cost |
|---------|---------------|----------------|
| ECS Fargate | 2 tasks × 0.25 vCPU × 512MB | $15-25 |
| RDS PostgreSQL | db.t3.micro | $15-20 |
| Application Load Balancer | Standard ALB | $20-25 |
| NAT Gateway | Single NAT | $45-50 |
| Data Transfer | Moderate usage | $5-10 |
| CloudWatch Logs | 7-day retention | $2-5 |
| **Total** | | **$102-135/month** |

### Cost Optimization Tips:
1. **Remove NAT Gateway**: Use public subnets for ECS (less secure)
2. **Use Spot Instances**: Not available for Fargate
3. **Optimize Log Retention**: Reduce CloudWatch retention period
4. **Right-size Resources**: Monitor and adjust CPU/memory

## 🔧 Configuration Options

### Terraform Variables

| Variable | Description | Default | Options |
|----------|-------------|---------|---------|
| `aws_region` | AWS deployment region | us-east-1 | Any AWS region |
| `project_name` | Project identifier | pharma-order-mgmt | Alphanumeric + hyphens |
| `environment` | Environment name | prod | dev, staging, prod |
| `db_instance_class` | RDS instance type | db.t3.micro | db.t3.micro, db.t3.small |
| `backend_cpu` | Backend CPU units | 256 | 256, 512, 1024 |
| `backend_memory` | Backend memory (MB) | 512 | 512, 1024, 2048 |

### Environment Variables

**Backend Container**:
```bash
DATABASE_URL=postgresql://user:pass@host/db
DB_HOST=rds-endpoint
DB_PORT=5432
DB_NAME=pharma_orders
DB_USER=admin
DB_PASSWORD=secure-password
```

**Frontend Container**:
```bash
BACKEND_URL=http://alb-dns/api
```

## 🚨 Troubleshooting

### Common Issues

#### 1. ECS Tasks Not Starting
**Symptoms**: Tasks keep stopping, health checks failing

**Solutions**:
```bash
# Check CloudWatch logs
aws logs describe-log-groups --log-group-name-prefix "/ecs/pharma"

# View recent logs
aws logs tail /ecs/pharma-order-mgmt-backend --follow

# Check task definition
aws ecs describe-task-definition --task-definition pharma-order-mgmt-backend
```

#### 2. Database Connection Issues
**Symptoms**: Backend can't connect to RDS

**Solutions**:
```bash
# Verify RDS endpoint
aws rds describe-db-instances --db-instance-identifier pharma-order-mgmt-postgres

# Check security groups
aws ec2 describe-security-groups --group-names pharma-order-mgmt-rds-*

# Test connectivity from ECS task
aws ecs execute-command --cluster pharma-order-mgmt-cluster \
    --task TASK_ID --container backend \
    --command "psql -h RDS_ENDPOINT -U admin -d pharma_orders"
```

#### 3. Load Balancer Health Checks Failing
**Symptoms**: Targets showing unhealthy

**Solutions**:
```bash
# Check target group health
aws elbv2 describe-target-health --target-group-arn TARGET_GROUP_ARN

# Verify health check configuration
aws elbv2 describe-target-groups --target-group-arns TARGET_GROUP_ARN

# Test health endpoints directly
curl http://TASK_IP:8001/  # Backend
curl http://TASK_IP:8501/_stcore/health  # Frontend
```

#### 4. Docker Build Issues
**Symptoms**: Image build failures, push errors

**Solutions**:
```bash
# Check Docker daemon
docker info

# Verify ECR login
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ECR_URI

# Build with verbose output
docker build --no-cache --progress=plain -t image-name .

# Check image size
docker images | grep pharma
```

### Monitoring and Debugging

#### CloudWatch Logs
```bash
# List log groups
aws logs describe-log-groups --log-group-name-prefix "/ecs/pharma"

# Stream logs in real-time
aws logs tail /ecs/pharma-order-mgmt-backend --follow

# Search for errors
aws logs filter-log-events \
    --log-group-name "/ecs/pharma-order-mgmt-backend" \
    --filter-pattern "ERROR"
```

#### ECS Service Status
```bash
# Check service status
aws ecs describe-services \
    --cluster pharma-order-mgmt-cluster \
    --services pharma-order-mgmt-backend pharma-order-mgmt-frontend

# List running tasks
aws ecs list-tasks --cluster pharma-order-mgmt-cluster

# Describe specific task
aws ecs describe-tasks --cluster pharma-order-mgmt-cluster --tasks TASK_ARN
```

## 🔄 Updates and Maintenance

### Application Updates
```bash
# Method 1: Use deployment script
./deploy.sh

# Method 2: Manual update
cd terraform
terraform apply  # If infrastructure changes
# Then rebuild and push images
# Then update ECS services
```

### Database Migrations
```bash
# Connect to RDS instance
psql -h $(terraform output -raw database_endpoint) -U admin -d pharma_orders

# Run migration scripts
psql -h RDS_ENDPOINT -U admin -d pharma_orders < migration.sql
```

### Scaling
```bash
# Update desired count in terraform.tfvars
backend_desired_count = 2
frontend_desired_count = 2

# Apply changes
terraform apply

# Or scale directly via AWS CLI
aws ecs update-service \
    --cluster pharma-order-mgmt-cluster \
    --service pharma-order-mgmt-backend \
    --desired-count 2
```

## 🔒 Security Best Practices

### 1. Database Security
- ✅ RDS in private subnets
- ✅ Security groups restrict access
- ✅ Encrypted storage
- ✅ Automated backups
- ⚠️ Consider: Parameter Store for passwords

### 2. Network Security
- ✅ VPC with private subnets
- ✅ Security groups (least privilege)
- ✅ ALB with security groups
- ⚠️ Consider: WAF for additional protection

### 3. Container Security
- ✅ Non-root user in containers
- ✅ Minimal base images
- ✅ Health checks
- ⚠️ Consider: Image scanning, secrets management

### 4. Access Control
- ✅ IAM roles for ECS tasks
- ✅ Least privilege permissions
- ⚠️ Consider: VPC endpoints, private ECR

## 🧹 Cleanup

To destroy all AWS resources:

```bash
cd terraform

# Destroy infrastructure
terraform destroy

# Confirm destruction
# Type 'yes' when prompted
```

**Warning**: This will permanently delete:
- All ECS services and tasks
- RDS database (including data)
- Load balancer and networking
- ECR repositories and images

## 📞 Support

For deployment issues:

1. **Check Prerequisites**: Ensure all tools are installed and configured
2. **Review Logs**: Check CloudWatch logs for detailed error messages
3. **Validate Configuration**: Verify terraform.tfvars settings
4. **Test Connectivity**: Ensure AWS credentials and network access
5. **Monitor Resources**: Use AWS Console to check resource status

---

**🎉 Your pharmaceutical order management system is now ready for production on AWS!**

The deployment provides a scalable, secure, and maintainable infrastructure that can handle your pharmaceutical order management needs with high availability and automated backups.