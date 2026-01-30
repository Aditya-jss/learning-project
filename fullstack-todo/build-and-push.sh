#!/bin/bash

# Build and Push Script for Fullstack Todo App
# This script builds both Docker images and pushes them to Docker Hub

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get Docker Hub username
echo -e "${YELLOW}Enter your Docker Hub username:${NC}"
read DOCKERHUB_USERNAME

if [ -z "$DOCKERHUB_USERNAME" ]; then
    echo -e "${RED}Error: Docker Hub username is required${NC}"
    exit 1
fi

echo -e "${GREEN}Building Docker images...${NC}"

# Build backend
echo -e "${YELLOW}Building backend image...${NC}"
cd backend
docker build -t ${DOCKERHUB_USERNAME}/todo-backend:latest .
echo -e "${GREEN}✓ Backend image built successfully${NC}"
cd ..

# Build frontend
echo -e "${YELLOW}Building frontend image...${NC}"
cd frontend
docker build -t ${DOCKERHUB_USERNAME}/todo-frontend:latest .
echo -e "${GREEN}✓ Frontend image built successfully${NC}"
cd ..

# Login to Docker Hub
echo -e "${YELLOW}Logging in to Docker Hub...${NC}"
docker login

# Push images
echo -e "${YELLOW}Pushing backend image...${NC}"
docker push ${DOCKERHUB_USERNAME}/todo-backend:latest
echo -e "${GREEN}✓ Backend image pushed successfully${NC}"

echo -e "${YELLOW}Pushing frontend image...${NC}"
docker push ${DOCKERHUB_USERNAME}/todo-frontend:latest
echo -e "${GREEN}✓ Frontend image pushed successfully${NC}"

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}All images built and pushed successfully!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${YELLOW}Images available at:${NC}"
echo "  - ${DOCKERHUB_USERNAME}/todo-backend:latest"
echo "  - ${DOCKERHUB_USERNAME}/todo-frontend:latest"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Update k8s/complete-deployment.yaml with your Docker Hub username"
echo "2. Run: ./deploy.sh"
echo ""
