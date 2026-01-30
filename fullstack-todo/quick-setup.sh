#!/bin/bash

# Quick Setup Script - Run this first!
# This script sets up everything you need to deploy to Kubernetes

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Todo App - Quick Setup${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Get Docker Hub username
echo -e "${YELLOW}What is your Docker Hub username?${NC}"
read DOCKERHUB_USERNAME

if [ -z "$DOCKERHUB_USERNAME" ]; then
    echo -e "${RED}Error: Docker Hub username is required${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}Starting deployment process...${NC}"
echo ""

# Step 1: Build images
echo -e "${YELLOW}[1/4] Building Docker images...${NC}"
cd backend
docker build -t ${DOCKERHUB_USERNAME}/todo-backend:latest .
cd ../frontend
docker build -t ${DOCKERHUB_USERNAME}/todo-frontend:latest .
cd ..
echo -e "${GREEN}✓ Images built${NC}"
echo ""

# Step 2: Login and push
echo -e "${YELLOW}[2/4] Pushing to Docker Hub...${NC}"
echo "Please log in to Docker Hub:"
docker login
docker push ${DOCKERHUB_USERNAME}/todo-backend:latest
docker push ${DOCKERHUB_USERNAME}/todo-frontend:latest
echo -e "${GREEN}✓ Images pushed${NC}"
echo ""

# Step 3: Update manifests
echo -e "${YELLOW}[3/4] Updating Kubernetes manifests...${NC}"
sed "s/your-dockerhub-username/${DOCKERHUB_USERNAME}/g" k8s/complete-deployment.yaml > k8s/complete-deployment.yaml.tmp
mv k8s/complete-deployment.yaml.tmp k8s/complete-deployment.yaml
echo -e "${GREEN}✓ Manifests updated${NC}"
echo ""

# Step 4: Deploy
echo -e "${YELLOW}[4/4] Deploying to Kubernetes...${NC}"
kubectl apply -f k8s/complete-deployment.yaml
echo ""
echo -e "${YELLOW}Waiting for pods to be ready (this may take a minute)...${NC}"
kubectl wait --for=condition=ready pod -l app=todo-backend -n todo-app --timeout=180s || true
kubectl wait --for=condition=ready pod -l app=todo-frontend -n todo-app --timeout=180s || true
echo -e "${GREEN}✓ Deployed${NC}"

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}Setup Complete! 🎉${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Show how to access
echo -e "${YELLOW}Your app is now running on Kubernetes!${NC}"
echo ""
kubectl get pods -n todo-app
echo ""
kubectl get services -n todo-app
echo ""

if command -v minikube &> /dev/null && minikube status &> /dev/null; then
    MINIKUBE_IP=$(minikube ip)
    echo -e "${GREEN}Access your app at: http://${MINIKUBE_IP}:30080${NC}"
    echo ""
    echo "Or run: minikube service frontend-service -n todo-app"
else
    echo -e "${GREEN}Access your app at: http://localhost:30080${NC}"
fi

echo ""
echo -e "${YELLOW}Share with your team:${NC}"
echo "1. Tell them your Docker Hub username: ${DOCKERHUB_USERNAME}"
echo "2. They can pull images: docker pull ${DOCKERHUB_USERNAME}/todo-backend:latest"
echo "3. They can deploy: kubectl apply -f k8s/complete-deployment.yaml"
echo ""
