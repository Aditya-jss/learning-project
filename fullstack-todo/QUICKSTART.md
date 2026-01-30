# 🎯 QUICK START - Deploy to Kubernetes in 5 Minutes!

## The Fastest Way (Recommended for First Time)

Run this ONE command and follow the prompts:

```bash
./quick-setup.sh
```

That's it! The script will:
- Build Docker images
- Push to Docker Hub
- Deploy to Kubernetes
- Show you the URL to access your app

---

## Manual Step-by-Step (If you want more control)

### 1️⃣ Build and Push Images

```bash
./build-and-push.sh
```
Enter your Docker Hub username when prompted.

### 2️⃣ Deploy to Kubernetes

```bash
./deploy.sh
```
Enter your Docker Hub username when prompted (or skip if already updated).

### 3️⃣ Access Your App

- **With Minikube**: `minikube service frontend-service -n todo-app`
- **With Docker Desktop**: `http://localhost:30080`

---

## 📤 Share with Your Team

### Option 1: Share Docker Images (Easiest)
Tell your team:
1. Your Docker Hub username
2. Run: `kubectl apply -f k8s/complete-deployment.yaml` (after updating with your username)

### Option 2: Share Everything
Share this entire folder. They run:
```bash
./quick-setup.sh
```

---

## 🛠️ Useful Commands

```bash
# View running pods
kubectl get pods -n todo-app

# View logs
kubectl logs -f <pod-name> -n todo-app

# Scale up
kubectl scale deployment backend-deployment -n todo-app --replicas=3

# Delete everything
kubectl delete namespace todo-app
```

---

## 📚 Need More Details?

Read [KUBERNETES_DEPLOYMENT.md](KUBERNETES_DEPLOYMENT.md) for:
- Detailed explanations
- Troubleshooting guide
- Architecture diagrams
- Production considerations

---

## ✅ Prerequisites

- Docker installed and running
- Kubernetes cluster (minikube, Docker Desktop, or cloud)
- kubectl installed
- Docker Hub account

---

## 🎉 That's It!

Your fullstack todo app is now running on Kubernetes and can be shared with your team!
