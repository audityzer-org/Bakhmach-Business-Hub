# Kubernetes Deployment Guide - Bakhmach Business Hub

## Overview
This guide provides complete Kubernetes (K8s) deployment configurations for the Bakhmach Business Hub production environment.

## Prerequisites
- Kubernetes cluster 1.24+
- kubectl CLI configured
- Helm 3.0+
- Container registry access (Docker Hub / GCR / ECR)

## Architecture

### Cluster Setup
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: bakhmach-prod
  labels:
    environment: production
```

### Deployment Configuration
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: bakhmach-api
  namespace: bakhmach-prod
spec:
  replicas: 3
  selector:
    matchLabels:
      app: bakhmach-api
  template:
    metadata:
      labels:
        app: bakhmach-api
    spec:
      containers:
      - name: api
        image: romanchaa997/bakhmach-business-hub:latest
        ports:
        - containerPort: 3000
        env:
        - name: NODE_ENV
          value: "production"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
```

### Service Configuration
```yaml
apiVersion: v1
kind: Service
metadata:
  name: bakhmach-api-service
  namespace: bakhmach-prod
spec:
  type: LoadBalancer
  selector:
    app: bakhmach-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 3000
```

### ConfigMap & Secrets
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: bakhmach-config
  namespace: bakhmach-prod
data:
  DATABASE_HOST: "postgres.bakhmach-prod.svc.cluster.local"
  CACHE_HOST: "redis.bakhmach-prod.svc.cluster.local"
  LOG_LEVEL: "info"
---
apiVersion: v1
kind: Secret
metadata:
  name: bakhmach-secrets
  namespace: bakhmach-prod
type: Opaque
stringData:
  DATABASE_PASSWORD: "${DB_PASS}"
  API_KEY: "${API_KEY}"
```

## Deployment Steps

### 1. Create Namespace
```bash
kubectl create namespace bakhmach-prod
```

### 2. Apply ConfigMaps and Secrets
```bash
kubectl apply -f configmap.yaml
kubectl apply -f secrets.yaml
```

### 3. Deploy Application
```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

### 4. Verify Deployment
```bash
kubectl get pods -n bakhmach-prod
kubectl get svc -n bakhmach-prod
kubectl logs -f deployment/bakhmach-api -n bakhmach-prod
```

## Scaling

### Manual Scaling
```bash
kubectl scale deployment bakhmach-api --replicas=5 -n bakhmach-prod
```

### Horizontal Pod Autoscaler
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: bakhmach-hpa
  namespace: bakhmach-prod
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: bakhmach-api
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

## Monitoring & Logging

### Prometheus Metrics
```yaml
apiVersion: v1
kind: Service
metadata:
  name: bakhmach-metrics
  namespace: bakhmach-prod
spec:
  ports:
  - name: metrics
    port: 9090
  selector:
    app: bakhmach-api
```

### ELK Stack Integration
- Elasticsearch for log storage
- Logstash for log processing
- Kibana for visualization

## Security Best Practices

1. **RBAC Configuration**
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: bakhmach-role
  namespace: bakhmach-prod
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list"]
```

2. **Network Policies**
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: bakhmach-network-policy
  namespace: bakhmach-prod
spec:
  podSelector:
    matchLabels:
      app: bakhmach-api
  policyTypes:
  - Ingress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: bakhmach-prod
```

## Disaster Recovery

### Backup Strategy
- Daily backup of PostgreSQL database
- PVC snapshots every 6 hours
- Configuration versioning in Git

### Recovery Procedures
1. Restore from latest backup
2. Verify data integrity
3. Run migrations if needed
4. Deploy fresh cluster

## Performance Optimization

- CPU/Memory requests: 250m / 256Mi
- Pod Disruption Budget for high availability
- Node affinity for optimal placement
- Image caching strategies

## Troubleshooting

```bash
# Check pod status
kubectl describe pod <pod-name> -n bakhmach-prod

# View logs
kubectl logs <pod-name> -n bakhmach-prod

# Access pod shell
kubectl exec -it <pod-name> -n bakhmach-prod -- /bin/bash

# Check service connectivity
kubectl get endpoints -n bakhmach-prod
```

## Helm Chart

For simplified deployment, use the Bakhmach Helm chart:

```bash
helm repo add bakhmach https://charts.bakhmach.dev
helm install bakhmach bakhmach/bakhmach-business-hub \
  --namespace bakhmach-prod \
  --values values.yaml
```

## Support & Documentation

- Full Kubernetes docs: https://kubernetes.io/docs
- Bakhmach GitHub: https://github.com/romanchaa997/Bakhmach-Business-Hub
- Issue tracker: https://github.com/romanchaa997/Bakhmach-Business-Hub/issues

---
**Last Updated**: January 2026
**Owner**: @romanchaa997
**Status**: Production Ready ✅
