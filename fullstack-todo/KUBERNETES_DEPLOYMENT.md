# Kubernetes Deployment Guide - Fullstack Todo App

This guide will help you containerize and deploy your fullstack todo application to Kubernetes.

## 📋 Prerequisites

Before you begin, ensure you have:
- Docker installed and running
- Kubernetes cluster (minikube, Docker Desktop, or cloud provider)
- kubectl CLI installed
- Docker Hub account (or another container registry)

## 🚀 Step-by-Step Deployment Guide

### Step 1: Install Prerequisites (if not already installed)

#### Install Docker
```bash
# macOS (using Homebrew)
brew install --cask docker

# Or download from: https://www.docker.com/products/docker-desktop
```

#### Install kubectl
```bash
# macOS
brew install kubectl
```

#### Install Minikube (for local Kubernetes cluster)
```bash
# macOS
brew install minikube

# Start minikube
minikube start
```

### Step 2: Build Docker Images

Navigate to the project root directory and build both images:

#### Build Backend Image
```bash
cd backend
docker build -t YOUR_DOCKERHUB_USERNAME/todo-backend:latest .
cd ..
```

#### Build Frontend Image
```bash
cd frontend
docker build -t YOUR_DOCKERHUB_USERNAME/todo-frontend:latest .
cd ..
```

**Replace `YOUR_DOCKERHUB_USERNAME` with your actual Docker Hub username!**

### Step 3: Test Images Locally (Optional but Recommended)

#### Test Backend
```bash
docker run -d -p 8000:8000 --name test-backend YOUR_DOCKERHUB_USERNAME/todo-backend:latest

# Check if it's working
curl http://localhost:8000/health

# Stop and remove
docker stop test-backend && docker rm test-backend
```

#### Test Frontend
```bash
docker run -d -p 8080:80 --name test-frontend YOUR_DOCKERHUB_USERNAME/todo-frontend:latest

# Visit http://localhost:8080 in your browser

# Stop and remove
docker stop test-frontend && docker rm test-frontend
```

### Step 4: Push Images to Docker Hub

Login to Docker Hub:
```bash
docker login
# Enter your Docker Hub username and password
```

Push the images:
```bash
docker push YOUR_DOCKERHUB_USERNAME/todo-backend:latest
docker push YOUR_DOCKERHUB_USERNAME/todo-frontend:latest
```

### Step 5: Update Kubernetes Manifests

Edit the Kubernetes deployment files to use your Docker Hub username:

1. Open `k8s/complete-deployment.yaml`
2. Replace `your-dockerhub-username` with your actual username in both places:
   - Line with `image: your-dockerhub-username/todo-backend:latest`
   - Line with `image: your-dockerhub-username/todo-frontend:latest`

### Step 6: Deploy to Kubernetes

#### Apply all resources at once:
```bash
kubectl apply -f k8s/complete-deployment.yaml
```

#### Or deploy individually:
```bash
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/frontend-deployment.yaml
```

### Step 7: Verify Deployment

Check if pods are running:
```bash
# List all pods in the todo-app namespace
kubectl get pods -n todo-app

# You should see 2 backend pods and 2 frontend pods running
```

Check services:
```bash
kubectl get services -n todo-app
```

Get detailed status:
```bash
# Watch pods until they're all running
kubectl get pods -n todo-app -w

# Check pod logs if there are issues
kubectl logs -n todo-app <pod-name>
```

### Step 8: Access Your Application

#### If using Minikube:
```bash
# Get the Minikube IP
minikube ip

# Get the NodePort
kubectl get service frontend-service -n todo-app

# Access at: http://<minikube-ip>:30080
minikube service frontend-service -n todo-app
```

#### If using Docker Desktop Kubernetes:
```bash
# Access at: http://localhost:30080
open http://localhost:30080
```

#### If using cloud provider (AWS, GCP, Azure):
```bash
# Get the LoadBalancer IP
kubectl get service frontend-service -n todo-app

# Wait for EXTERNAL-IP to be assigned (may take a few minutes)
# Then access: http://<EXTERNAL-IP>
```

## 🔄 Sharing with Your Team

### Option 1: Share Docker Images (Recommended)

Your team members can pull the images directly from Docker Hub:

```bash
# They just need to run:
docker pull YOUR_DOCKERHUB_USERNAME/todo-backend:latest
docker pull YOUR_DOCKERHUB_USERNAME/todo-frontend:latest

# Then deploy to their Kubernetes cluster:
kubectl apply -f k8s/complete-deployment.yaml
```

### Option 2: Share Source Code + Dockerfiles

Share the entire project repository. Team members can:
1. Build images themselves
2. Push to their own registry
3. Deploy to Kubernetes

### Option 3: Export/Import Docker Images (No Docker Hub needed)

If you can't use Docker Hub, export images to files:

```bash
# Export images
docker save YOUR_DOCKERHUB_USERNAME/todo-backend:latest > todo-backend.tar
docker save YOUR_DOCKERHUB_USERNAME/todo-frontend:latest > todo-frontend.tar

# Share these .tar files with your team

# Team members import them:
docker load < todo-backend.tar
docker load < todo-frontend.tar
```

## 🛠️ Useful Commands

### Scaling
```bash
# Scale backend to 3 replicas
kubectl scale deployment backend-deployment -n todo-app --replicas=3

# Scale frontend to 3 replicas
kubectl scale deployment frontend-deployment -n todo-app --replicas=3
```

### Updates
```bash
# After building a new image with a new tag
docker build -t YOUR_DOCKERHUB_USERNAME/todo-backend:v2 backend/
docker push YOUR_DOCKERHUB_USERNAME/todo-backend:v2

# Update deployment
kubectl set image deployment/backend-deployment -n todo-app backend=YOUR_DOCKERHUB_USERNAME/todo-backend:v2
```

### Debugging
```bash
# Get pod details
kubectl describe pod <pod-name> -n todo-app

# View logs
kubectl logs -f <pod-name> -n todo-app

# Execute commands in a pod
kubectl exec -it <pod-name> -n todo-app -- /bin/sh

# Port forward for testing
kubectl port-forward -n todo-app service/backend-service 8000:8000
kubectl port-forward -n todo-app service/frontend-service 8080:80
```

### Cleanup
```bash
# Delete all resources
kubectl delete -f k8s/complete-deployment.yaml

# Or delete namespace (removes everything)
kubectl delete namespace todo-app
```

## 📊 Architecture

```
┌─────────────────────────────────────────┐
│         Kubernetes Cluster              │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │   Namespace: todo-app           │   │
│  │                                 │   │
│  │  ┌──────────────────────────┐  │   │
│  │  │  Frontend Service        │  │   │
│  │  │  (NodePort: 30080)       │  │   │
│  │  └────────┬─────────────────┘  │   │
│  │           │                     │   │
│  │  ┌────────▼─────────────────┐  │   │
│  │  │  Frontend Pods (x2)      │  │   │
│  │  │  (Nginx + React)         │  │   │
│  │  └────────┬─────────────────┘  │   │
│  │           │ /api, /health       │   │
│  │  ┌────────▼─────────────────┐  │   │
│  │  │  Backend Service         │  │   │
│  │  │  (ClusterIP: 8000)       │  │   │
│  │  └────────┬─────────────────┘  │   │
│  │           │                     │   │
│  │  ┌────────▼─────────────────┐  │   │
│  │  │  Backend Pods (x2)       │  │   │
│  │  │  (FastAPI + SQLite)      │  │   │
│  │  └──────────────────────────┘  │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

## 🎯 Quick Reference

| Component | Image Tag | Service Name | Port |
|-----------|-----------|--------------|------|
| Backend | `YOUR_DOCKERHUB_USERNAME/todo-backend:latest` | backend-service | 8000 |
| Frontend | `YOUR_DOCKERHUB_USERNAME/todo-frontend:latest` | frontend-service | 80 → 30080 |

## ⚠️ Important Notes

1. **SQLite in Production**: The current setup uses SQLite, which is stored in the container. Data will be lost when pods restart. For production, consider using:
   - PostgreSQL or MySQL with persistent volumes
   - Cloud database service (AWS RDS, Google Cloud SQL, etc.)

2. **Environment Variables**: Update CORS origins and other configs as needed

3. **Security**: In production, consider:
   - Using private container registry
   - Implementing HTTPS/TLS
   - Adding authentication/authorization
   - Using Kubernetes secrets for sensitive data

4. **Resource Limits**: Adjust CPU and memory limits based on your needs

## 🤝 Team Collaboration Workflow

**For the person deploying first (you):**
1. Build images
2. Push to Docker Hub
3. Deploy to Kubernetes
4. Share the Docker Hub repository name with team

**For team members:**
1. Get the Docker Hub repository name
2. Update `k8s/complete-deployment.yaml` with correct image names
3. Run `kubectl apply -f k8s/complete-deployment.yaml`
4. Access the application

## 🎉 Success!

If everything works:
- Backend health check: `http://<your-ip>:30080/health`
- Frontend UI: `http://<your-ip>:30080`
- You can create, read, update, and delete todos!

## 📞 Troubleshooting

If pods aren't starting:
```bash
# Check pod status
kubectl get pods -n todo-app

# View pod logs
kubectl logs -n todo-app <pod-name>

# Describe pod for events
kubectl describe pod -n todo-app <pod-name>
```

Common issues:
- **ImagePullBackOff**: Wrong image name or not pushed to Docker Hub
- **CrashLoopBackOff**: Application error, check logs
- **Pending**: Resource constraints, check node capacity

---

Need help? Check the Kubernetes documentation: https://kubernetes.io/docs/
