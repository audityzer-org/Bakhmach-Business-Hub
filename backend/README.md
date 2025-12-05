# Bakhmach Business Hub - Backend API

Node.js/Express.js backend API for the Bakhmach Business Hub platform - a cooperative platform for personal development planning and achievement tracking.

## Quick Start

### Prerequisites
- Node.js 18+
- PostgreSQL 13+
- npm or yarn

### Installation

1. Clone the repository:
```bash
git clone https://github.com/romanchaa997/Bakhmach-Business-Hub.git
cd Bakhmach-Business-Hub/backend
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment:
```bash
cp env.template .env
# Edit .env with your configuration
```

4. Initialize database:
```bash
psql -U postgres -d bakhmach_hub -f schema.sql
```

5. Start development server:
```bash
npm run dev
```

Server will be running at `http://localhost:3001`

## Available Scripts

- `npm run dev` - Start development server with hot-reload
- `npm run build` - Compile TypeScript to JavaScript
- `npm start` - Run production build
- `npm test` - Run tests with coverage
- `npm run lint` - Run ESLint

## Project Structure

```
backend/
├── app.ts              # Express app configuration
├── config.ts           # Configuration management
├── auth.ts             # JWT authentication middleware
├── routes.ts           # API route definitions
├── authService.ts      # Authentication business logic
├── user.ts             # User model class
├── schema.sql          # PostgreSQL database schema
├── env.template        # Environment configuration template
├── package.json        # Dependencies and scripts
├── tsconfig.json       # TypeScript configuration
└── README.md           # This file
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Create new user account
- `POST /api/v1/auth/login` - Authenticate user
- `GET /api/v1/auth/profile` - Get user profile (requires token)

### PDPs (Personal Development Plans)
- `POST /api/v1/pdps/create` - Create new PDP
- `GET /api/v1/pdps` - List all PDPs
- `GET /api/v1/pdps/{id}` - Get PDP details
- `PUT /api/v1/pdps/{id}` - Update PDP

### Goals
- `POST /api/v1/goals/create` - Create goal
- `GET /api/v1/goals` - List all goals
- `GET /api/v1/goals/{id}` - Get goal details
- `PUT /api/v1/goals/{id}` - Update goal

### Tasks
- `POST /api/v1/tasks/create` - Create task
- `GET /api/v1/tasks` - List all tasks
- `GET /api/v1/tasks/{id}` - Get task details
- `PUT /api/v1/tasks/{id}` - Update task

### Analytics
- `GET /api/v1/analytics/summary` - Get user analytics summary

## Configuration

Environment variables (see `env.template`):

- `NODE_ENV` - Development or production
- `PORT` - Server port (default: 3001)
- `DB_HOST` - PostgreSQL host
- `DB_PORT` - PostgreSQL port
- `DB_NAME` - Database name
- `DB_USER` - Database user
- `DB_PASSWORD` - Database password
- `JWT_SECRET` - JWT signing secret
- `CORS_ORIGIN` - CORS allowed origins

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:

```bash
Authorization: Bearer <your_jwt_token>
```

## Error Handling

API returns standardized error responses:

```json
{
  "error": "ERROR_CODE",
  "message": "Human-readable error message",
  "timestamp": "2025-12-05T21:00:00Z"
}
```

## Contributing

See main [CONTRIBUTING.md](../CONTRIBUTING.md) for contribution guidelines.

## License

GPL-3.0 - See [LICENSE](../LICENSE) for details.
