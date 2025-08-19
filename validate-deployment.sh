#!/bin/bash

# Pharmaceutical Order Management System - Deployment Validation Script
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔍 Validating Pharmaceutical Order Management System Deployment${NC}"

# Get Terraform outputs
cd terraform

if [ ! -f "terraform.tfstate" ]; then
    echo -e "${RED}❌ Terraform state not found. Please run deployment first.${NC}"
    exit 1
fi

APPLICATION_URL=$(terraform output -raw application_url 2>/dev/null || echo "")
BACKEND_API_URL=$(terraform output -raw backend_api_url 2>/dev/null || echo "")
BACKEND_DOCS_URL=$(terraform output -raw backend_docs_url 2>/dev/null || echo "")
ECS_CLUSTER=$(terraform output -raw ecs_cluster_name 2>/dev/null || echo "")
AWS_REGION=$(terraform output -raw aws_region 2>/dev/null || echo "us-east-1")

if [ -z "$APPLICATION_URL" ]; then
    echo -e "${RED}❌ Could not retrieve application URL from Terraform outputs${NC}"
    exit 1
fi

echo -e "${BLUE}📋 Deployment Information:${NC}"
echo -e "${YELLOW}Application URL: ${APPLICATION_URL}${NC}"
echo -e "${YELLOW}Backend API URL: ${BACKEND_API_URL}${NC}"
echo -e "${YELLOW}API Documentation: ${BACKEND_DOCS_URL}${NC}"
echo -e "${YELLOW}ECS Cluster: ${ECS_CLUSTER}${NC}"
echo ""

# Test 1: Check ECS Services
echo -e "${YELLOW}🔍 Test 1: Checking ECS Services Status...${NC}"

BACKEND_SERVICE_STATUS=$(aws ecs describe-services \
    --cluster $ECS_CLUSTER \
    --services pharma-order-mgmt-backend \
    --region $AWS_REGION \
    --query 'services[0].status' \
    --output text 2>/dev/null || echo "UNKNOWN")

FRONTEND_SERVICE_STATUS=$(aws ecs describe-services \
    --cluster $ECS_CLUSTER \
    --services pharma-order-mgmt-frontend \
    --region $AWS_REGION \
    --query 'services[0].status' \
    --output text 2>/dev/null || echo "UNKNOWN")

if [ "$BACKEND_SERVICE_STATUS" = "ACTIVE" ]; then
    echo -e "${GREEN}✅ Backend service is ACTIVE${NC}"
else
    echo -e "${RED}❌ Backend service status: $BACKEND_SERVICE_STATUS${NC}"
fi

if [ "$FRONTEND_SERVICE_STATUS" = "ACTIVE" ]; then
    echo -e "${GREEN}✅ Frontend service is ACTIVE${NC}"
else
    echo -e "${RED}❌ Frontend service status: $FRONTEND_SERVICE_STATUS${NC}"
fi

# Test 2: Check Running Tasks
echo -e "${YELLOW}🔍 Test 2: Checking Running Tasks...${NC}"

BACKEND_RUNNING_COUNT=$(aws ecs describe-services \
    --cluster $ECS_CLUSTER \
    --services pharma-order-mgmt-backend \
    --region $AWS_REGION \
    --query 'services[0].runningCount' \
    --output text 2>/dev/null || echo "0")

FRONTEND_RUNNING_COUNT=$(aws ecs describe-services \
    --cluster $ECS_CLUSTER \
    --services pharma-order-mgmt-frontend \
    --region $AWS_REGION \
    --query 'services[0].runningCount' \
    --output text 2>/dev/null || echo "0")

if [ "$BACKEND_RUNNING_COUNT" -gt "0" ]; then
    echo -e "${GREEN}✅ Backend has $BACKEND_RUNNING_COUNT running task(s)${NC}"
else
    echo -e "${RED}❌ Backend has no running tasks${NC}"
fi

if [ "$FRONTEND_RUNNING_COUNT" -gt "0" ]; then
    echo -e "${GREEN}✅ Frontend has $FRONTEND_RUNNING_COUNT running task(s)${NC}"
else
    echo -e "${RED}❌ Frontend has no running tasks${NC}"
fi

# Test 3: Check Load Balancer Target Health
echo -e "${YELLOW}🔍 Test 3: Checking Load Balancer Target Health...${NC}"

# Get target group ARNs
BACKEND_TG_ARN=$(aws elbv2 describe-target-groups \
    --names pharma-order-mgmt-backend-tg \
    --region $AWS_REGION \
    --query 'TargetGroups[0].TargetGroupArn' \
    --output text 2>/dev/null || echo "")

FRONTEND_TG_ARN=$(aws elbv2 describe-target-groups \
    --names pharma-order-mgmt-frontend-tg \
    --region $AWS_REGION \
    --query 'TargetGroups[0].TargetGroupArn' \
    --output text 2>/dev/null || echo "")

if [ -n "$BACKEND_TG_ARN" ] && [ "$BACKEND_TG_ARN" != "None" ]; then
    BACKEND_HEALTHY_COUNT=$(aws elbv2 describe-target-health \
        --target-group-arn $BACKEND_TG_ARN \
        --region $AWS_REGION \
        --query 'length(TargetHealthDescriptions[?TargetHealth.State==`healthy`])' \
        --output text 2>/dev/null || echo "0")
    
    if [ "$BACKEND_HEALTHY_COUNT" -gt "0" ]; then
        echo -e "${GREEN}✅ Backend has $BACKEND_HEALTHY_COUNT healthy target(s)${NC}"
    else
        echo -e "${RED}❌ Backend has no healthy targets${NC}"
    fi
else
    echo -e "${YELLOW}⚠️ Could not find backend target group${NC}"
fi

if [ -n "$FRONTEND_TG_ARN" ] && [ "$FRONTEND_TG_ARN" != "None" ]; then
    FRONTEND_HEALTHY_COUNT=$(aws elbv2 describe-target-health \
        --target-group-arn $FRONTEND_TG_ARN \
        --region $AWS_REGION \
        --query 'length(TargetHealthDescriptions[?TargetHealth.State==`healthy`])' \
        --output text 2>/dev/null || echo "0")
    
    if [ "$FRONTEND_HEALTHY_COUNT" -gt "0" ]; then
        echo -e "${GREEN}✅ Frontend has $FRONTEND_HEALTHY_COUNT healthy target(s)${NC}"
    else
        echo -e "${RED}❌ Frontend has no healthy targets${NC}"
    fi
else
    echo -e "${YELLOW}⚠️ Could not find frontend target group${NC}"
fi

# Test 4: HTTP Connectivity Tests
echo -e "${YELLOW}🔍 Test 4: Testing HTTP Connectivity...${NC}"

# Test frontend
echo -e "${BLUE}Testing frontend accessibility...${NC}"
FRONTEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 30 "$APPLICATION_URL" || echo "000")

if [ "$FRONTEND_STATUS" = "200" ]; then
    echo -e "${GREEN}✅ Frontend is accessible (HTTP $FRONTEND_STATUS)${NC}"
elif [ "$FRONTEND_STATUS" = "000" ]; then
    echo -e "${RED}❌ Frontend is not accessible (Connection failed)${NC}"
else
    echo -e "${YELLOW}⚠️ Frontend returned HTTP $FRONTEND_STATUS${NC}"
fi

# Test backend API
echo -e "${BLUE}Testing backend API accessibility...${NC}"
BACKEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 30 "$BACKEND_API_URL/" || echo "000")

if [ "$BACKEND_STATUS" = "200" ]; then
    echo -e "${GREEN}✅ Backend API is accessible (HTTP $BACKEND_STATUS)${NC}"
elif [ "$BACKEND_STATUS" = "000" ]; then
    echo -e "${RED}❌ Backend API is not accessible (Connection failed)${NC}"
else
    echo -e "${YELLOW}⚠️ Backend API returned HTTP $BACKEND_STATUS${NC}"
fi

# Test API documentation
echo -e "${BLUE}Testing API documentation...${NC}"
DOCS_STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 30 "$BACKEND_DOCS_URL" || echo "000")

if [ "$DOCS_STATUS" = "200" ]; then
    echo -e "${GREEN}✅ API documentation is accessible (HTTP $DOCS_STATUS)${NC}"
elif [ "$DOCS_STATUS" = "000" ]; then
    echo -e "${RED}❌ API documentation is not accessible (Connection failed)${NC}"
else
    echo -e "${YELLOW}⚠️ API documentation returned HTTP $DOCS_STATUS${NC}"
fi

# Test 5: Database Connectivity (via API)
echo -e "${YELLOW}🔍 Test 5: Testing Database Connectivity...${NC}"

DB_TEST_STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 30 "$BACKEND_API_URL/orders/" || echo "000")

if [ "$DB_TEST_STATUS" = "200" ]; then
    echo -e "${GREEN}✅ Database connectivity is working (HTTP $DB_TEST_STATUS)${NC}"
elif [ "$DB_TEST_STATUS" = "000" ]; then
    echo -e "${RED}❌ Database connectivity test failed (Connection failed)${NC}"
else
    echo -e "${YELLOW}⚠️ Database connectivity test returned HTTP $DB_TEST_STATUS${NC}"
fi

# Test 6: Check Recent Logs for Errors
echo -e "${YELLOW}🔍 Test 6: Checking Recent Application Logs...${NC}"

echo -e "${BLUE}Checking backend logs for errors...${NC}"
BACKEND_ERRORS=$(aws logs filter-log-events \
    --log-group-name "/ecs/pharma-order-mgmt-backend" \
    --start-time $(date -d '5 minutes ago' +%s)000 \
    --filter-pattern "ERROR" \
    --region $AWS_REGION \
    --query 'length(events)' \
    --output text 2>/dev/null || echo "0")

if [ "$BACKEND_ERRORS" = "0" ]; then
    echo -e "${GREEN}✅ No recent errors in backend logs${NC}"
else
    echo -e "${YELLOW}⚠️ Found $BACKEND_ERRORS recent error(s) in backend logs${NC}"
fi

echo -e "${BLUE}Checking frontend logs for errors...${NC}"
FRONTEND_ERRORS=$(aws logs filter-log-events \
    --log-group-name "/ecs/pharma-order-mgmt-frontend" \
    --start-time $(date -d '5 minutes ago' +%s)000 \
    --filter-pattern "ERROR" \
    --region $AWS_REGION \
    --query 'length(events)' \
    --output text 2>/dev/null || echo "0")

if [ "$FRONTEND_ERRORS" = "0" ]; then
    echo -e "${GREEN}✅ No recent errors in frontend logs${NC}"
else
    echo -e "${YELLOW}⚠️ Found $FRONTEND_ERRORS recent error(s) in frontend logs${NC}"
fi

# Summary
echo ""
echo -e "${BLUE}📊 Validation Summary${NC}"
echo -e "${GREEN}✅ Services Status: Backend ($BACKEND_SERVICE_STATUS), Frontend ($FRONTEND_SERVICE_STATUS)${NC}"
echo -e "${GREEN}✅ Running Tasks: Backend ($BACKEND_RUNNING_COUNT), Frontend ($FRONTEND_RUNNING_COUNT)${NC}"
echo -e "${GREEN}✅ HTTP Status: Frontend ($FRONTEND_STATUS), Backend ($BACKEND_STATUS), Docs ($DOCS_STATUS)${NC}"
echo -e "${GREEN}✅ Database Test: HTTP $DB_TEST_STATUS${NC}"
echo -e "${GREEN}✅ Recent Errors: Backend ($BACKEND_ERRORS), Frontend ($FRONTEND_ERRORS)${NC}"

echo ""
echo -e "${BLUE}🔗 Access URLs:${NC}"
echo -e "${GREEN}🌐 Application: ${APPLICATION_URL}${NC}"
echo -e "${GREEN}🔌 Backend API: ${BACKEND_API_URL}${NC}"
echo -e "${GREEN}📚 API Docs: ${BACKEND_DOCS_URL}${NC}"

echo ""
if [ "$FRONTEND_STATUS" = "200" ] && [ "$BACKEND_STATUS" = "200" ]; then
    echo -e "${GREEN}🎉 Deployment validation completed successfully!${NC}"
    echo -e "${GREEN}✨ Your pharmaceutical order management system is ready for use!${NC}"
else
    echo -e "${YELLOW}⚠️ Deployment validation completed with warnings.${NC}"
    echo -e "${YELLOW}💡 Some services may still be starting up. Wait a few minutes and try again.${NC}"
fi

cd ..