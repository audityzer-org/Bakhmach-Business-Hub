# Load Testing & Performance Benchmarking

## Overview
Comprehensive load testing strategy using k6 for Bakhmach Business Hub, covering spike tests, stress tests, and capacity planning.

## K6 Load Testing Scripts

### Basic Load Test
```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  stages: [
    { duration: '30s', target: 100 },   // Ramp-up
    { duration: '1m', target: 500 },    // Stay at peak
    { duration: '30s', target: 0 },     // Ramp-down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500', 'p(99)<1000'],
    http_req_failed: ['rate<0.1'],
  },
};

export default function() {
  let res = http.get('https://api.bakhmach.com/health');
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  sleep(1);
}
```

### Spike Test
```javascript
export let options = {
  stages: [
    { duration: '10s', target: 100 },
    { duration: '1m', target: 1000 },   // Sudden spike
    { duration: '10s', target: 100 },
  ],
};
```

### Stress Test
```javascript
export let options = {
  stages: [
    { duration: '2m', target: 100 },
    { duration: '5m', target: 500 },
    { duration: '10m', target: 1000 }, // Sustained load
    { duration: '2m', target: 0 },
  ],
};
```

## Performance Targets

| Metric | Target | Threshold |
|--------|--------|----------|
| p50 Latency | 100ms | < 200ms |
| p95 Latency | 300ms | < 500ms |
| p99 Latency | 500ms | < 1000ms |
| Error Rate | < 0.1% | < 1% |
| Throughput | 1000 RPS | Min 500 RPS |

## Running Load Tests

```bash
# Local test
k6 run load-test.js

# Cloud test (with metrics)
k6 cloud load-test.js

# Generate HTML report
k6 run --out json=results.json load-test.js
k6 convert results.json > report.html
```

## Database Query Performance

### Query Optimization Checklist
- [ ] Proper indexing on frequently queried columns
- [ ] Query execution time < 100ms
- [ ] Connection pooling configured
- [ ] Slow query log monitoring enabled
- [ ] Query cache implemented where applicable

### Benchmark Example
```sql
EXPLAIN ANALYZE
SELECT u.id, u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at > NOW() - INTERVAL '30 days'
GROUP BY u.id, u.name
ORDER BY order_count DESC;
```

## Endpoint Performance Benchmarks

| Endpoint | p50 | p95 | p99 | RPS |
|----------|-----|-----|-----|-----|
| GET /api/products | 50ms | 150ms | 300ms | 2000 |
| POST /api/orders | 100ms | 350ms | 600ms | 500 |
| GET /api/users/:id | 30ms | 100ms | 200ms | 3000 |
| GET /health | 10ms | 20ms | 50ms | 10000 |

## Capacity Planning

### Resource Allocation
- CPU: 4 vCPU min, 8 vCPU recommended
- Memory: 8GB min, 16GB recommended
- Database: SSD storage, 50GB initial
- Network: 100Mbps min

### Scaling Strategy
- Horizontal: Add container replicas
- Vertical: Increase instance size
- Database: Read replicas for high read volume

## Monitoring During Load Tests

### Key Metrics
- Response time distribution
- Error rate trends
- CPU/Memory usage
- Database connection count
- Cache hit ratio

## Best Practices

1. Test during off-peak times
2. Gradually increase load
3. Monitor infrastructure metrics
4. Document baseline performance
5. Test failure scenarios
6. Verify recovery mechanisms
7. Repeat tests regularly
