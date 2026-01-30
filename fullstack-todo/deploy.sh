#!/bin/bash

# Deploy Script for Fullstack Todo App to Kubernetes
# This script deploys the application to your Kubernetes cluster

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Fullstack Todo App - Kubernetes Deploy${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}Error: kubectl is not installed${NC}"
    echo "Please install kubectl: https://kubernetes.io/docs/tasks/tools/"
    exit 1
fi

# Check if cluster is accessible
echo -e "${YELLOW}Checking Kubernetes cluster connection...${NC}"
if ! kubectl cluster-info &> /dev/null; then
    echo -e "${RED}Error: Cannot connect to Kubernetes cluster${NC}"
    echo "Please ensure your cluster is running (minikube start, or check your cloud provider)"
    exit 1
fi
echo -e "${GREEN}✓ Connected to Kubernetes cluster${NC}"
echo ""

# Ask for Docker Hub username to update manifests
echo -e "${YELLOW}Enter your Docker Hub username (or press Enter to skip if already updated):${NC}"
read DOCKERHUB_USERNAME

if [ ! -z "$DOCKERHUB_USERNAME" ]; then
    echo -e "${YELLOW}Updating Kubernetes manifests...${NC}"
    
    # Create a temporary file
    sed "s/your-dockerhub-username/${DOCKERHUB_USERNAME}/g" k8s/complete-deployment.yaml > k8s/complete-deployment.yaml.tmp
    mv k8s/complete-deployment.yaml.tmp k8s/complete-deployment.yaml
    
    echo -e "${GREEN}✓ Manifests updated${NC}"
fi

# Deploy to Kubernetes
echo ""
echo -e "${YELLOW}Deploying to Kubernetes...${NC}"
kubectl apply -f k8s/complete-deployment.yaml
echo -e "${GREEN}✓ Resources deployed${NC}"

# Wait for pods to be ready
echo ""
echo -e "${YELLOW}Waiting for pods to be ready...${NC}"
kubectl wait --for=condition=ready pod -l app=todo-backend -n todo-app --timeout=120s
kubectl wait --for=condition=ready pod -l app=todo-frontend -n todo-app --timeout=120s
echo -e "${GREEN}✓ All pods are ready${NC}"

# Get status
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Deployment Status${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

echo -e "${YELLOW}Pods:${NC}"
kubectl get pods -n todo-app

echo ""
echo -e "${YELLOW}Services:${NC}"
kubectl get services -n todo-app

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}Deployment Complete!${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Get access URL
echo -e "${YELLOW}Access your application:${NC}"
if command -v minikube &> /dev/null && minikube status &> /dev/null; then
    MINIKUBE_IP=$(minikube ip)
    echo "  URL: http://${MINIKUBE_IP}:30080"
    echo ""
    echo "Or run: minikube service frontend-service -n todo-app"
else
    echo "  URL: http://localhost:30080"
    echo "  (if using Docker Desktop Kubernetes)"
fi

echo ""
echo -e "${YELLOW}Useful commands:${NC}"
echo "  View logs:     kubectl logs -f <pod-name> -n todo-app"
echo "  Shell access:  kubectl exec -it <pod-name> -n todo-app -- /bin/sh"
echo "  Scale app:     kubectl scale deployment backend-deployment -n todo-app --replicas=3"
echo "  Delete app:    kubectl delete namespace todo-app"
echo ""
