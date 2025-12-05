ARCHITECTURE.md  # Bakhmach Business Hub - Technical Architecture

**Version**: 0.2.0  
**Status**: MVP Planning Phase  
**Last Updated**: December 5, 2024

---

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (Next.js 14)                    │
│  React Components | TypeScript | Tailwind CSS | Zustand     │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTPS/REST
                           ↓
┌─────────────────────────────────────────────────────────────┐
│               API Gateway (Express.js)                       │
│  Auth | Rate Limiting | Request Validation | Error Handling │
└──────────────────────────┬──────────────────────────────────┘
                           │
          ┌────────────────┼────────────────┐
          ↓                ↓                ↓
     ┌─────────┐   ┌─────────────┐   ┌──────────┐
     │ Business│   │ Auth        │   │ Integration
     │ Logic   │   │ Service     │   │ Service
     │ Service │   │             │   │
     │         │   │ - JWT       │   │ - GitHub
     │ - Users │   │ - Sessions  │   │ - Slack
     │ - Goals │   │ - MFA       │   │ - Calendar
     │ - Tasks │   │             │   │
     └────┬────┘   └────┬────────┘   └──────┬─────┘
          │             │                   │
          └─────────────┼───────────────────┘
                        │
          ┌─────────────┼─────────────┐
          ↓             ↓             ↓
      ┌────────┐  ┌──────────┐  ┌────────┐
      │PostgreSQL│ │  Redis   │  │  S3    │
      │ (Data)  │  │ (Cache)  │  │(Files) │
      │         │  │          │  │        │
      │ Users   │  │ Sessions │  │ Avatars│
      │ Goals   │  │ Tokens   │  │ Exports│
      │ Tasks   │  │ API Keys │  │Reports │
      └────────┘  └──────────┘  └────────┘
```

---

## 🗂️ Directory Structure

### Frontend (`/frontend`)

```
frontend/
├── src/
│   ├── pages/           # Next.js pages
│   ├── components/      # Reusable React components
│   ├── hooks/          # Custom React hooks
│   ├── services/       # API client services
│   ├── store/          # Zustand state management
│   ├── types/          # TypeScript types
│   ├── utils/          # Helper functions
│   ├── styles/         # Global styles
│   └── app.tsx         # Root component
├── public/             # Static assets
├── next.config.js      # Next.js config
├── tsconfig.json       # TypeScript config
└── package.json        # Dependencies
```

### Backend (`/backend`)

```
backend/
├── src/
│   ├── routes/         # API endpoint handlers
│   ├── controllers/     # Business logic
│   ├── models/         # Database models
│   ├── middleware/     # Express middleware
│   ├── services/       # Business logic
│   ├── utils/          # Helper functions
│   ├── config/         # Configuration
│   └── index.ts        # Entry point
├── migrations/         # Database migrations
├── tests/             # Unit & integration tests
├── .env.example        # Environment variables
├── docker-compose.yml  # Local development
└── package.json        # Dependencies
```

---

## 🔌 API Endpoints (MVP Phase)

### Authentication
```
POST   /api/auth/signup           # Register new user
POST   /api/auth/login             # Login with email/password
POST   /api/auth/github            # OAuth with GitHub
POST   /api/auth/refresh           # Refresh JWT token
POST   /api/auth/logout            # Logout & invalidate token
GET    /api/auth/me                # Get current user
```

### Users
```
GET    /api/users/:id              # Get user profile
PUT    /api/users/:id              # Update user profile
DELETE /api/users/:id              # Delete user account
GET    /api/users/:id/settings     # Get user settings
PUT    /api/users/:id/settings     # Update user settings
```

### Personal Development Plans
```
POST   /api/pdps                   # Create new PDP
GET    /api/pdps                   # List user PDPs
GET    /api/pdps/:id               # Get PDP details
PUT    /api/pdps/:id               # Update PDP
DELETE /api/pdps/:id               # Delete PDP
GET    /api/pdps/:id/report        # Generate PDP report
```

### Goals
```
POST   /api/goals                  # Create goal
GET    /api/goals                  # List user goals
GET    /api/goals/:id              # Get goal details
PUT    /api/goals/:id              # Update goal
DELETE /api/goals/:id              # Delete goal
POST   /api/goals/:id/progress     # Log progress
```

### Tasks
```
POST   /api/tasks                  # Create task
GET    /api/tasks                  # List tasks (with filtering)
GET    /api/tasks/:id              # Get task details
PUT    /api/tasks/:id              # Update task
DELETE /api/tasks/:id              # Delete task
POST   /api/tasks/:id/complete     # Mark task complete
```

### Analytics
```
GET    /api/analytics/summary      # Dashboard summary
GET    /api/analytics/goals        # Goal progress analytics
GET    /api/analytics/productivity # Productivity scores
GET    /api/analytics/export       # Export data (PDF/CSV)
```

---

## 💾 Database Schema (PostgreSQL)

### Users Table
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  username VARCHAR(100) UNIQUE,
  password_hash VARCHAR(255),
  avatar_url VARCHAR(255),
  github_id INTEGER,
  github_access_token VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  deleted_at TIMESTAMP
);
```

### Personal Development Plans
```sql
CREATE TABLE pdps (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  title VARCHAR(255) NOT NULL,
  description TEXT,
  start_date DATE,
  end_date DATE,
  vision TEXT,
  data JSONB,  -- Stores all PDP data
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### Goals
```sql
CREATE TABLE goals (
  id UUID PRIMARY KEY,
  pdp_id UUID REFERENCES pdps(id),
  user_id UUID REFERENCES users(id),
  title VARCHAR(255) NOT NULL,
  domain VARCHAR(50),  -- career, finance, health, etc.
  target_date DATE,
  status VARCHAR(50),  -- active, completed, on_hold
  progress INT,        -- 0-100
  data JSONB,          -- Stores goal details
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### Tasks
```sql
CREATE TABLE tasks (
  id UUID PRIMARY KEY,
  goal_id UUID REFERENCES goals(id),
  user_id UUID REFERENCES users(id),
  title VARCHAR(255) NOT NULL,
  description TEXT,
  priority INT,        -- 1-5
  due_date DATE,
  completed_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🔐 Security Architecture

### Authentication Flow
1. User signs up with email/password or GitHub OAuth
2. Backend validates and creates user account
3. JWT token generated (access + refresh tokens)
4. Frontend stores tokens (httpOnly cookies for refresh)
5. Requests include Authorization header with JWT
6. Backend validates JWT on each request

### Password Security
- Bcrypt hashing (10 rounds)
- No passwords stored in plain text
- Password reset via email verification
- Session invalidation on password change

### Data Protection
- HTTPS only
- CORS configured for frontend domain
- Rate limiting on auth endpoints
- Input validation on all endpoints
- SQL injection prevention (parameterized queries)
- XSS protection (Content Security Policy)

---

## ⚡ Performance Optimization

### Caching Strategy
- Redis for session storage
- User profile caching (5 min TTL)
- Goal/task list caching (2 min TTL)
- Analytics caching (10 min TTL)

### Database Optimization
- Indexes on frequently queried columns
- Connection pooling (10 connections)
- Query optimization for list endpoints
- Pagination (20 items per page)

### Frontend Optimization
- Code splitting
- Image optimization
- Lazy loading
- Service worker for offline support
- CDN for static assets

---

## 🧪 Testing Strategy

### Unit Tests
- Controllers: >80% coverage
- Services: >80% coverage
- Utils: >90% coverage
- Frontend components: >70% coverage

### Integration Tests
- API endpoint tests
- Database transaction tests
- Auth flow tests
- Payment processing (Stripe) tests

### E2E Tests
- User signup flow
- Goal creation & tracking
- Report generation
- Export functionality

---

## 📊 Monitoring & Logging

### Logging
- Winston logger (error, warn, info, debug levels)
- Request logging middleware
- Error tracking (Sentry)
- Performance monitoring (New Relic)

### Metrics
- Request latency (p50, p95, p99)
- Error rate
- API response times
- Database query performance
- User engagement metrics

---

## 🚀 Deployment Architecture

### Frontend (Vercel)
- Automatic deployments on push to main
- Preview deployments for PRs
- Edge function support
- CDN for global distribution

### Backend (Railway/Render)
- Docker containerization
- CI/CD via GitHub Actions
- Environment variable management
- Database backups

### Database (PostgreSQL)
- Managed service (Heroku Postgres / Supabase)
- Automated backups (daily)
- Replication for high availability
- SSL connections required

---

## 📈 Scalability Roadmap

### Phase 1 (MVP - 1000 users)
- Single backend instance
- Shared database
- Redis caching
- CDN for frontend

### Phase 2 (Growth - 10K users)
- Horizontal scaling (load balancer)
- Read replicas for database
- Distributed caching
- Message queue (Bull/BullMQ)

### Phase 3 (Scale - 100K+ users)
- Microservices architecture
- Kubernetes orchestration
- Event-driven workflows
- GraphQL for complex queries

---

**Next**: Start with Backend Foundation (Auth, DB Setup)
**Timeline**: Weeks 1-3 of MVP development
