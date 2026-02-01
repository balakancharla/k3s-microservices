#!/bin/bash
set -e

echo "🚀 Starting WSL microservices validation checklist..."

# Paths
BACKEND_DIR="./backend"
FRONTEND_DIR="./frontend"
K8S_DIR="./k8s"

# Ports
BACKEND_PORT=8081
FRONTEND_PORT=8082

# Docker images
BACKEND_IMAGE="mybackendimage:latest"
FRONTEND_IMAGE="myfrontendimage:latest"

# Function to check if port is free
function check_port() {
    PORT=$1
    if lsof -i:$PORT > /dev/null; then
        echo "⚠️ Port $PORT is already in use. Please free it and rerun."
        exit 1
    fi
}

echo "1️⃣ Checking ports..."
check_port $BACKEND_PORT
check_port $FRONTEND_PORT

echo "2️⃣ Starting backend Flask server..."
# Run backend in background
python3 $BACKEND_DIR/app.py &
BACKEND_PID=$!
sleep 3

echo "3️⃣ Starting frontend static server..."
# Serve frontend (static files) in background
cd $FRONTEND_DIR
python3 -m http.server $FRONTEND_PORT &
FRONTEND_PID=$!
cd -

sleep 2

echo "4️⃣ Building Docker images..."
#docker build -t $BACKEND_IMAGE $BACKEND_DIR
#docker build -t $FRONTEND_IMAGE $FRONTEND_DIR

echo "5️⃣ Applying Kubernetes manifests..."
kubectl apply -f $K8S_DIR/namespace.yaml
kubectl apply -f $K8S_DIR/backend.yaml
kubectl apply -f $K8S_DIR/frontend.yaml

echo "6️⃣ Waiting for pods to be ready..."
sleep 5
kubectl wait --for=condition=Ready pods --all -n billpay --timeout=60s

echo "7️⃣ Listing pods and services..."
kubectl get pods -n billpay
kubectl get svc -n billpay

echo "8️⃣ Running curl tests..."

echo "🔹 Backend health check"
curl -s http://127.0.0.1:$BACKEND_PORT/api/health | jq

echo "🔹 Login test"
curl -s -X POST http://127.0.0.1:$BACKEND_PORT/api/login \
-H "Content-Type: application/json" \
-d '{"username":"admin","password":"password"}' | jq

echo "🔹 Pay bill test"
curl -s -X POST http://127.0.0.1:$BACKEND_PORT/api/pay-bill \
-H "Content-Type: application/json" \
-d '{}' | jq

echo "✅ Validation completed successfully!"

echo "🛑 Cleaning up backend/frontend processes..."
kill $BACKEND_PID
kill $FRONTEND_PID

echo "🎉 All done!"

