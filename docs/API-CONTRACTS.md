# API Contracts & Schemas

Comprehensive OpenAPI 3.0, GraphQL, and gRPC specifications for all Bakhmach services.

## Services Overview

| Service | Type | Port | Protocol |
|---------|------|------|----------|
| API Gateway | Central | 8000 | REST/GraphQL |
| Auth Service | Security | 8001 | REST |
| ML Pipeline | Processing | 8002 | REST/gRPC |
| Finance Sync | Integration | 8003 | REST |
| Payments | Commerce | 8004 | REST |
| Orchestrator | Management | 8005 | gRPC |

## API Gateway

### Base URL
- **Dev:** `http://localhost:8000/api/v1`
- **Prod:** `https://api.bakhmach-hub.dev/api/v1`

### Authentication
```
Header: Authorization: Bearer {jwt_token}
Expiry: 24 hours
Refresh: POST /auth/refresh
```

### Endpoints

#### GET /architecture
Retrieve system architecture graph
```json
{
  "nodes": [{"id": "service-1", "name": "API Gateway", "health": 98}],
  "edges": [{"source": "service-1", "target": "service-2", "latency": 45}],
  "timestamp": "2026-01-02T19:00:00Z"
}
```

#### GET /health
System health check
```json
{
  "status": "healthy",
  "services": {"auth": "up", "ml": "up", "payments": "up"},
  "uptime": 99.87
}
```

#### POST /query
GraphQL query endpoint
```graphql
query GetArchitecture {
  architecture {
    nodes { id name health readiness }
    edges { source target latency }
  }
  metrics {
    avgLatency
    requestsPerSecond
    errorRate
  }
}
```

## Auth Service

### Endpoints

#### POST /auth/login
Authenticate user
```json
Request:
{ "email": "user@example.com", "password": "secure_pass" }

Response:
{ "token": "jwt_token", "expires_in": 86400 }
```

#### POST /auth/refresh
Refresh JWT token
```json
Response:
{ "token": "new_jwt_token", "expires_in": 86400 }
```

#### GET /auth/verify
Verify token validity
```json
Response:
{ "valid": true, "user_id": "uuid", "expires_at": "2026-01-03T19:00:00Z" }
```

## ML Pipeline Service

### Endpoints

#### POST /predict
Generate predictions (gRPC recommended)
```json
Request:
{
  "model": "architecture_optimizer",
  "input_data": { "metric": "latency", "value": 250 },
  "confidence_threshold": 0.8
}

Response:
{
  "prediction": 0.92,
  "confidence": 0.87,
  "recommendation": "scale_service",
  "processing_time_ms": 1250
}
```

#### GET /models
List available models
```json
Response:
{
  "models": [
    {"name": "architecture_optimizer", "version": "1.2.3", "accuracy": 0.94},
    {"name": "performance_predictor", "version": "2.0.0", "accuracy": 0.91}
  ]
}
```

## Payments Service

### Endpoints

#### POST /payments/process
Process payment (PCI DSS compliance required)
```json
Request:
{
  "amount": 9900,
  "currency": "USD",
  "provider": "stripe",
  "idempotency_key": "uuid"
}

Response:
{
  "transaction_id": "txn_123abc",
  "status": "succeeded",
  "timestamp": "2026-01-02T19:00:00Z"
}
```

#### GET /payments/{transaction_id}
Retrieve payment details
```json
Response:
{
  "id": "txn_123abc",
  "amount": 9900,
  "status": "succeeded",
  "created_at": "2026-01-02T19:00:00Z"
}
```

## Finance Sync Service

### Endpoints

#### POST /sync/monobank
Sync Monobank transactions
```json
Request:
{
  "account_id": "monobank_uuid",
  "from_timestamp": "2026-01-01T00:00:00Z",
  "to_timestamp": "2026-01-02T23:59:59Z"
}

Response:
{
  "synced_transactions": 42,
  "total_amount": 5000000,
  "last_sync": "2026-01-02T19:00:00Z"
}
```

## Error Responses

All services follow consistent error format:
```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Description of what went wrong",
    "status": 400,
    "trace_id": "uuid-for-debugging"
  }
}
```

### Common Status Codes
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `429` - Rate Limited (100 req/min per IP)
- `500` - Internal Server Error
- `503` - Service Unavailable

## Rate Limiting

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1704181200
```

## Versioning Strategy

- Current: `v1` (stable)
- Beta: `v2-beta` (testing)
- Deprecated versions supported for 12 months
- Breaking changes require major version bump

## GraphQL Schema

```graphql
type Query {
  architecture: Architecture!
  health: HealthStatus!
  metrics(service: String!): ServiceMetrics!
  user(id: ID!): User!
}

type Mutation {
  deployService(name: String!, version: String!): DeploymentResult!
  configureCache(ttl: Int!): CacheConfig!
  triggerOptimization: OptimizationResult!
}

type Subscription {
  systemMetrics: Metrics!
  deploymentStatus: DeploymentEvent!
  alertEvents: Alert!
}
```

## gRPC Services

### Orchestrator Service
```protobuf
service Orchestrator {
  rpc DeployService(DeployRequest) returns (DeployResponse);
  rpc GetStatus(StatusRequest) returns (StatusResponse);
  rpc ScaleService(ScaleRequest) returns (ScaleResponse);
}
```

## Testing

### API Testing Tools
- **Postman:** `/docs/postman-collection.json`
- **Swagger UI:** `http://localhost:8000/docs`
- **GraphQL Playground:** `http://localhost:8000/graphql`
- **gRPC UI:** `http://localhost:8005/grpc`

### Test Coverage
- Unit tests: 85%+ coverage
- Integration tests: All endpoints
- Load tests: See `docs/LOAD-TESTS.md`
- Security tests: OWASP Top 10

## Documentation

- **OpenAPI Spec:** `services/api/openapi.yaml`
- **GraphQL Schema:** `services/api/schema.graphql`
- **gRPC Definitions:** `services/api/protos/`
- **API Guides:** `docs/API-GUIDES/`

---

**Last Updated:** January 2, 2026  
**Version:** 1.0.0  
**Owner:** @romanchaa997
