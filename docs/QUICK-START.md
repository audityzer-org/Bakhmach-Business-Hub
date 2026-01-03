# Bakhmach Business Hub - Quick Start Guide

**Get up and running with Bakhmach Business Hub in 15 minutes!**

## 📋 Prerequisites

- Node.js 18+ ([Download](https://nodejs.org/))
- npm or yarn
- PostgreSQL 13+ ([Download](https://www.postgresql.org/))
- Git

## 🚀 Step 1: Clone the Repository

```bash
git clone https://github.com/romanchaa997/Bakhmach-Business-Hub.git
cd Bakhmach-Business-Hub
```

## 🏗️ Step 2: Set Up the Backend

```bash
cd backend
npm install
cp env.template .env
```

Edit `.env` with your configuration:

```env
NODE_ENV=development
PORT=3001
DB_HOST=localhost
DB_PORT=5432
DB_NAME=bakhmach_hub
DB_USER=postgres
DB_PASSWORD=your_password
JWT_SECRET=your_secret_key
CORS_ORIGIN=http://localhost:3000
```

## 💾 Step 3: Initialize Database

```bash
# Create database
psql -U postgres -c "CREATE DATABASE bakhmach_hub;"

# Run schema
psql -U postgres -d bakhmach_hub -f schema.sql
```

## ▶️ Step 4: Start Backend Server

```bash
npm run dev
```

Server running at: `http://localhost:3001`

## 🎨 Step 5: Set Up Frontend (Optional)

```bash
cd ../frontend  # if it exists
npm install
npm start
```

Frontend running at: `http://localhost:3000`

## 📱 Step 6: Test the API

### Health Check

```bash
curl http://localhost:3001/api/v1/health
```

### Register User

```bash
curl -X POST http://localhost:3001/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword",
    "name": "User Name"
  }'
```

### Login

```bash
curl -X POST http://localhost:3001/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword"
  }'
```

## 🔍 Step 7: Explore the Architecture

1. **View Architecture Model:**
   - Open `docs/ARCHITECTURE.json` for complete system design

2. **Interactive Visualizer:**
   - Open `docs/ARCHITECTURE-VISUALIZER.html` in your browser

3. **API Endpoints:**
   - Check `backend/routes.ts` for all available endpoints

## 📚 Available Commands

### Backend

```bash
# Development (with hot reload)
npm run dev

# Build TypeScript
npm run build

# Production
npm start

# Tests
npm test

# Linting
npm run lint
```

## 🐛 Troubleshooting

### Database Connection Failed

```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Or check if port 5432 is in use
lsof -i :5432
```

### Port Already in Use

```bash
# Change PORT in .env file
PORT=3002  # Use different port

# Or kill process on port 3001
lsof -i :3001 | grep LISTEN | awk '{print $2}' | xargs kill -9
```

### Module Not Found

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

## 📖 Next Steps

1. **Read Documentation:**
   - `docs/README.md` - Documentation hub
   - `docs/DEV-REVIEW.md` - Technical review
   - `docs/ARCHITECTURE.json` - System design

2. **Create Your First PDP:**
   ```bash
   curl -X POST http://localhost:3001/api/v1/pdps/create \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "My Development Plan",
       "description": "Learning backend development",
       "startDate": "2026-01-02",
       "endDate": "2026-12-31"
     }'
   ```

3. **Explore Features:**
   - Goals Management
   - Task Tracking
   - Analytics
   - Consciousness Metrics

## 🤝 Contributing

See `CONTRIBUTING.md` for guidelines.

## 💬 Support

- **Issues:** [GitHub Issues](https://github.com/romanchaa997/Bakhmach-Business-Hub/issues)
- **Email:** roman@bakhmach-hub.com
- **Documentation:** See `/docs` directory

## 📝 Project Structure

```
Bakhmach-Business-Hub/
├── backend/                    # Node.js/Express API
├── frontend/                   # React web app (if exists)
├── services/                   # Microservices
├── docs/                       # Documentation
│   ├── README.md              # Doc hub
│   ├── QUICK-START.md         # This file
│   ├── ARCHITECTURE.json      # System design
│   ├── DEV-REVIEW.md          # Technical review
│   └── ...
├── package.json
└── README.md
```

## ⚡ Quick Reference

| Command | Purpose |
|---------|----------|
| `npm run dev` | Start development server |
| `npm test` | Run tests |
| `npm run build` | Build for production |
| `npm run lint` | Check code quality |

## 🎯 Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register user |
| POST | `/api/v1/auth/login` | Login |
| GET | `/api/v1/auth/profile` | Get profile |
| POST | `/api/v1/pdps/create` | Create PDP |
| GET | `/api/v1/pdps` | List PDPs |
| POST | `/api/v1/goals/create` | Create goal |
| GET | `/api/v1/goals` | List goals |
| POST | `/api/v1/tasks/create` | Create task |
| GET | `/api/v1/tasks` | List tasks |

---

**Ready to build? Happy coding!** 🚀

*Last Updated: January 2, 2026*
*Version: 1.0*

## 🚀 Automated Startup Script

For quick setup and initialization, use the provided startup script:

```bash
#!/bin/bash
# Bakhmach Business Hub - Integration Service Startup Script
# Version: 1.0
# Date: January 2, 2026

set -e

echo ""
echo "========================================"
echo "🚀 BAKHMACH BUSINESS HUB STARTUP"
echo "========================================"
echo ""

# Step 1: Check Python installation
echo "[1/10] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.10+"
    exit 1
fi
echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Step 2: Create virtual environment
echo "[2/10] Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi
source venv/bin/activate
echo ""

# Step 3: Install dependencies
echo "[3/10] Installing dependencies..."
pip install -q -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Step 4: Set up environment variables
echo "[4/10] Configuring environment variables..."
if [ ! -f ".env" ]; then
    cat > .env << 'EOF'
# GitHub Configuration
GITHUB_TOKEN=your_github_token_here
GITHUB_WEBHOOK_SECRET=your_webhook_secret_here
GITHUB_REPO=romanchaa997/Bakhmach-Business-Hub

# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=bakhmach_integration
DB_USER=postgres
DB_PASSWORD=your_db_password_here

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379

# Application Configuration
APP_ENV=development
APP_DEBUG=true
LOG_LEVEL=INFO
EOF
    echo "✅ .env file created (⚠️  Update with real credentials)"
else
    echo "✅ .env file already exists"
fi
echo ""

# Step 5: Check database connectivity
echo "[5/10] Checking PostgreSQL connectivity..."
if command -v psql &> /dev/null; then
    psql -h localhost -U postgres -d template1 -c "SELECT 1" > /dev/null 2>&1 && \
    echo "✅ PostgreSQL is accessible" || \
    echo "⚠️  PostgreSQL not fully accessible (will attempt to continue)"
else
    echo "⚠️  psql not installed (skipping PostgreSQL check)"
fi
echo ""

# Step 6: Check Redis connectivity
echo "[6/10] Checking Redis connectivity..."
if command -v redis-cli &> /dev/null; then
    redis-cli ping > /dev/null 2>&1 && \
    echo "✅ Redis is accessible" || \
    echo "⚠️  Redis not fully accessible (will attempt to continue)"
else
    echo "⚠️  redis-cli not installed (skipping Redis check)"
fi
echo ""

# Step 7-10: Display startup summary
echo "[7/10] Setup complete!"
echo ""
echo "========================================"
echo "✅ BAKHMACH BUSINESS HUB IS READY"
echo "========================================"
echo ""
echo "🎯 Quick Start Guide:"
echo "   1. Update .env with real credentials"
echo "   2. Ensure PostgreSQL is running"
echo "   3. Ensure Redis is running"
echo "   4. Run: python3 -m uvicorn services.integration.main:app --reload"
echo ""
echo "📚 Documentation:"
echo "   - Architecture: docs/ARCHITECTURE_INTEGRATION.md"
echo "   - Roadmap: docs/NEXT_STEPS_STRATEGIC_ROADMAP.md"
echo "   - Q1 Plan: docs/PRODUCT_ROADMAP_Q1_2026.md"
echo ""
echo "🚀 Next Steps:"
echo "   1. Complete the sync_orchestrator TODO methods"
echo "   2. Set up OAuth 2.0 credentials"
echo "   3. Initialize webhook receiver"
echo "   4. Run integration tests"
echo "   5. Deploy to production (Jan 9, 2026)"
echo ""
echo "Setup complete! Ready for development. 🎉"
echo ""
```

### Running the Startup Script

1. **Save the script** to your project root as `startup.sh`
2. **Make it executable**:
   ```bash
   chmod +x startup.sh
   ```
3. **Run the script**:
   ```bash
   ./startup.sh
   ```

### What the Script Does

- ✅ Checks Python 3.10+ installation
- ✅ Creates and activates virtual environment
- ✅ Installs all project dependencies
- ✅ Sets up `.env` configuration file
- ✅ Verifies PostgreSQL connectivity
- ✅ Verifies Redis connectivity
- ✅ Displays next steps and documentation links

### Troubleshooting

If you encounter issues:

1. **Python not found**: Install Python 3.10+ from [python.org](https://www.python.org)
2. **PostgreSQL connection failed**: Ensure PostgreSQL is running on `localhost:5432`
3. **Redis connection failed**: Ensure Redis is running on `localhost:6379`
4. **Permission denied**: Run `chmod +x startup.sh` before executing

---

*Last Updated: January 3, 2026*
*Status: ACTIVE - Implementation Phase*
