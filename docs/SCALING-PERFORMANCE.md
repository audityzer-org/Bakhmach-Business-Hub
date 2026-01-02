# Performance & Scaling Guide

## Overview

Guide for optimizing performance and scaling Bakhmach Business Hub to handle enterprise-level loads.

## Performance Optimization

### Database Optimization

#### Connection Pooling

```python
from sqlalchemy.pool import QueuePool

engine = create_engine(
    'postgresql://user:password@host/db',
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True,
    pool_recycle=3600
)
```

#### Query Optimization

```python
# Use SELECT * only when necessary
query = db.session.query(SyncRecord.id, SyncRecord.status)

# Use eager loading to prevent N+1 queries
from sqlalchemy.orm import joinedload
records = db.session.query(SyncRecord).options(
    joinedload(SyncRecord.source)
).all()

# Use batch operations
db.session.bulk_insert_mappings(SyncRecord, records_list)
db.session.bulk_update_mappings(SyncRecord, updates_list)
```

#### Indexing Strategy

```sql
-- Sync records table
CREATE INDEX idx_sync_source_target ON sync_records(source, target);
CREATE INDEX idx_sync_status ON sync_records(status);
CREATE INDEX idx_sync_created_at ON sync_records(created_at DESC);
CREATE INDEX idx_sync_partial ON sync_records(source) WHERE status='pending';

-- User sessions table
CREATE INDEX idx_user_session_token ON user_sessions(token);
CREATE INDEX idx_user_session_user_id ON user_sessions(user_id);

-- Webhook deliveries table
CREATE INDEX idx_webhook_delivery_status ON webhook_deliveries(status);
CREATE INDEX idx_webhook_delivery_created ON webhook_deliveries(created_at DESC);
```

#### Caching Strategy

```python
from functools import wraps
from redis import Redis
import hashlib
import json

redis_client = Redis(host='localhost', port=6379, db=0)

def cache_result(ttl=3600):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{hashlib.md5(str(args)+str(kwargs)).hexdigest()}"
            result = redis_client.get(cache_key)
            
            if result:
                return json.loads(result)
            
            result = func(*args, **kwargs)
            redis_client.setex(cache_key, ttl, json.dumps(result))
            return result
        return wrapper
    return decorator

@cache_result(ttl=3600)
def get_user_profile(user_id):
    return db.session.query(User).get(user_id).to_dict()
```

### API Optimization

#### Response Compression

```python
from flask_compress import Compress

app = Flask(__name__)
Compress(app)  # Enables gzip compression
```

#### Pagination

```python
@app.route('/api/syncs', methods=['GET'])
def get_syncs():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)
    
    paginated = db.session.query(SyncRecord).paginate(
        page=page,
        per_page=per_page
    )
    
    return jsonify({
        'items': [sync.to_dict() for sync in paginated.items],
        'total': paginated.total,
        'pages': paginated.pages,
        'current_page': page
    })
```

#### Async Processing

```python
from celery import Celery
from celery.schedules import crontab

celery = Celery(app.name, broker='redis://localhost:6379')
celery.conf.update(app.config)

@celery.task
def sync_github_async():
    # Long-running task
    return orchestrator.sync_github()

@app.route('/api/sync', methods=['POST'])
def trigger_sync():
    task = sync_github_async.delay()
    return jsonify({'task_id': task.id}), 202

# Scheduled tasks
celery.conf.beat_schedule = {
    'sync-github-every-5-minutes': {
        'task': 'tasks.sync_github_async',
        'schedule': crontab(minute='*/5'),
    },
}
```

### Frontend Optimization

```javascript
// Code splitting with dynamic imports
const SyncDashboard = React.lazy(() => import('./SyncDashboard'));

// Suspense component for loading state
<Suspense fallback={<Loading />}>
  <SyncDashboard />
</Suspense>

// Memoization to prevent unnecessary re-renders
const SyncCard = React.memo(({ sync }) => {
  return <div>{sync.id}: {sync.status}</div>;
});

// Virtual scrolling for large lists
import { FixedSizeList } from 'react-window';

const ItemList = ({ items }) => (
  <FixedSizeList
    height={600}
    itemCount={items.length}
    itemSize={35}
    width='100%'
  >
    {({ index, style }) => (
      <div style={style}>
        {items[index].name}
      </div>
    )}
  </FixedSizeList>
);
```

## Horizontal Scaling

### Load Balancing

#### Nginx Configuration

```nginx
upstream bakhmach_backend {
    least_conn;
    server app1.bakhmach.local:8000 weight=5;
    server app2.bakhmach.local:8000 weight=5;
    server app3.bakhmach.local:8000 weight=3;
    
    keepalive 64;
}

server {
    listen 80;
    server_name api.bakhmach.com;
    
    location / {
        proxy_pass http://bakhmach_backend;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        
        # Buffering
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 24 4k;
    }
}
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: bakhmach-api
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
        image: bakhmach/api:latest
        ports:
        - containerPort: 8000
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
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
        env:
        - name: REDIS_URL
          value: redis://redis:6379
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: url
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: bakhmach-api-hpa
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
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### Database Replication

```sql
-- Primary database configuration
wal_level = replica
max_wal_senders = 3
max_replication_slots = 3

-- Replication slot creation
SELECT * FROM pg_create_physical_replication_slot('replica_slot');

-- Replica configuration
primary_conninfo = 'host=primary.bakhmach.local port=5432 user=repuser password=reppass'
replication = on
replication_slot_name = 'replica_slot'
```

## Vertical Scaling

### Resource Allocation

```python
# Database connection settings for larger deployments
DATABASE_POOL_SIZE = 50  # Production
DATABASE_MAX_OVERFLOW = 100
DATABASE_POOL_TIMEOUT = 30

# Redis cluster for caching
REDIS_CLUSTER_NODES = [
    'redis1:6379',
    'redis2:6379',
    'redis3:6379',
]
```

## Performance Benchmarks

### Target Metrics

```
API Endpoints:
- P50 Latency: < 50ms
- P95 Latency: < 200ms
- P99 Latency: < 500ms
- Throughput: > 1000 req/s
- Error Rate: < 0.1%

Database:
- Query Latency: < 10ms (p95)
- Connection Pool Utilization: < 80%
- Replication Lag: < 100ms

SyncOperations:
- Sync Duration: < 5s (p95)
- Throughput: > 100 syncs/minute
- Success Rate: > 99.5%
```

## Load Testing

```python
from locust import HttpUser, task, between

class APIUser(HttpUser):
    wait_time = between(1, 3)
    
    @task(3)
    def get_syncs(self):
        self.client.get("/api/syncs?page=1&per_page=20")
    
    @task(1)
    def trigger_sync(self):
        self.client.post("/api/sync", json={})

# Run with:
# locust -f locustfile.py --host=http://localhost:8000
```

## Monitoring Performance

### Key Metrics

1. **CPU Usage**: Target < 70%
2. **Memory Usage**: Target < 80%
3. **Disk I/O**: Monitor latency < 10ms
4. **Network**: Monitor bandwidth utilization
5. **Database Connections**: Keep < 80% pool capacity

### SLA Targets

```
UptimeSLA: 99.9%
LatencySLA: p95 < 200ms
ErrorSLA: < 0.1%
ThroughputSLA: > 1000 req/s
```

## Optimization Checklist

- [ ] Enable database query caching
- [ ] Configure Redis for session storage
- [ ] Enable response compression
- [ ] Implement connection pooling
- [ ] Set up CDN for static assets
- [ ] Configure load balancer
- [ ] Enable async task processing
- [ ] Implement database replication
- [ ] Configure autoscaling
- [ ] Set up monitoring and alerting
- [ ] Run load tests
- [ ] Review and optimize slow queries
- [ ] Implement rate limiting
- [ ] Configure caching headers
- [ ] Monitor and optimize resource usage

## Contact

For performance questions: @romanchaa997
