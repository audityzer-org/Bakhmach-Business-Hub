# Goals + Tasks Microservice

A TypeScript/Express microservice for managing personal and project goals with task tracking. Part of the Bakhmach Business Hub platform.

## Quick Start

### Install & Build
```bash
npm install
npm run build
```

### Environment Setup
Copy `.env.example` to `.env` and configure:
```bash
DATABASE_URL=postgres://user:password@localhost:5432/bakhmach_integration
NODE_ENV=development
PORT=4002
```

### Database Migration
```bash
psql -h localhost -U postgres -d bakhmach_integration \\
  -f ../../db/migrations/001_create_goals_tasks.sql
```

### Run Locally
```bash
npm run dev
curl http://localhost:4002/health
```

## Documentation

| Document | Purpose |
|----------|----------|
| **[IMPLEMENTATION_GUIDE.md](../GOALS_TASKS_IMPLEMENTATION_GUIDE.md)** | Complete code for all layers |
| **[DEVSECOPS_GUIDE.md](../GOALS_TASKS_DEVSECOPS_INFRA_GUIDE.md)** | Infrastructure & security configs |
| **[DEPLOYMENT_SUMMARY.md](../GOALS_TASKS_DEPLOYMENT_SUMMARY.md)** | Deployment checklist & guide |
| **[PRODUCTION_READY.md](../GOALS_TASKS_READY_FOR_PRODUCTION.md)** | Production readiness & status |

## Architecture

**Layers:**
- **Controllers** (`src/controllers/`) - HTTP request handling
- **Services** (`src/services/`) - Business logic
- **Repositories** (`src/repositories/`) - Database access (no ORM)
- **Routes** (`src/routes/`) - Express route definitions

**Stack:**
- Framework: Express.js
- Language: TypeScript (strict mode)
- Database: PostgreSQL (parameterized queries)
- Testing: Jest
- Linting: ESLint + Prettier
- Security: Helmet, CORS, zod validation

## API Endpoints

### Goals
```
POST   /api/v1/goals              Create goal
GET    /api/v1/goals              List goals (filter by status, pdpId)
GET    /api/v1/goals/:goalId      Get goal with progress
PATCH  /api/v1/goals/:goalId      Update goal
POST   /api/v1/goals/:goalId/tasks Create task for goal
```

### Tasks
```
GET    /api/v1/tasks              List tasks (filter by status, due date)
GET    /api/v1/tasks/:taskId      Get task
PATCH  /api/v1/tasks/:taskId      Update task (including completion)
```

### Health
```
GET    /health                    Health check (200 OK)
GET    /metrics                   Prometheus metrics (optional)
```

## Development

### Commands
```bash
npm run dev              # Start in development with ts-node
npm run build            # Compile TypeScript to dist/
npm start                # Run compiled JavaScript
npm test                 # Run Jest tests
npm run test:watch       # Run tests in watch mode
npm run test:coverage    # Generate coverage report
npm run lint             # Run ESLint
npm run lint:fix         # Fix linting errors
npm run format           # Format with Prettier
npm run type-check       # Check TypeScript types
```

### Testing
Create test files alongside source files:
```
src/
  services/
    goalsService.ts
    goalsService.test.ts
```

Run with:
```bash
npm test -- --coverage
```

Target: **80%+ code coverage**

## Deployment

### Docker
```bash
docker build -t bakhmach/goals-tasks:latest .
docker run -e DATABASE_URL="..." -p 4002:4002 bakhmach/goals-tasks:latest
```

### Kubernetes
```bash
kubectl apply -f ../../k8s/goals-tasks-deployment.yaml
kubectl get pods -l app=goals-tasks
kubectl logs -f deployment/goals-tasks
```

## Security

- ✅ No hardcoded secrets (environment variables)
- ✅ SQL injection protected (parameterized queries)
- ✅ Input validation (zod schemas)
- ✅ CORS restrictive (middleware)
- ✅ Security headers (helmet)
- ✅ Dependency scanning (npm audit, Snyk)
- ✅ Container scanning (Trivy in CI)
- ✅ Pod security policies (Kubernetes)

## Monitoring

**Logs:** Winston/Pino structured logging  
**Metrics:** Prometheus endpoint at `/metrics`  
**Health:** `/health` endpoint for uptime checks  
**Tracing:** Jaeger/OpenTelemetry ready  

## Troubleshooting

### Database Connection Error
```bash
psql -h localhost -U postgres -c "CREATE DATABASE bakhmach_integration;"
```

### Port Already in Use
```bash
kill $(lsof -t -i:4002)
```

### TypeScript Errors
```bash
npm run type-check
```

## CI/CD

GitHub Actions workflow automatically:
1. Lints code
2. Checks types
3. Runs tests with coverage
4. Scans dependencies
5. Builds Docker image
6. Deploys to staging

See `.github/workflows/goals-tasks.yml`

## Architecture Integration

Part of 7-microservice model:
- **Goals Service** ← YOU ARE HERE
- **Tasks Service** ← Integrated
- Auth Microservice (JWT validation)
- PDP Microservice (linked goals)
- Analytics Microservice (event consumption)
- Consciousness Microservice (metrics feed)
- Coordinator Microservice (orchestration)

## Next Steps

1. Copy code from `GOALS_TASKS_IMPLEMENTATION_GUIDE.md`
2. Run `npm install && npm run build`
3. Execute database migration
4. Start service locally: `npm start`
5. Run tests: `npm test`
6. Deploy with `docker build && kubectl apply`

For detailed deployment procedures, see `GOALS_TASKS_READY_FOR_PRODUCTION.md`

## Support

Documentation: See root-level guides  
Issues: Create GitHub issue with `[goals-tasks]` prefix  
Questions: Check implementation guides or contact backend team  

---

**Status**: 🟢 Production-Ready  
**Last Updated**: January 3, 2026  
**Version**: 1.0.0
