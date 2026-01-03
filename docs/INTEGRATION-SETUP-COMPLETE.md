# 🔗 Complete Integration Setup Guide - Bakhmach Business Hub

## All 7 Integrations Ready for Production

This guide covers setup, configuration, testing, and deployment of all integrations:
1. Gmail (Email)
2. GitHub (Repository Management)
3. Slack (Team Messaging)
4. Google Calendar (Event Management)
5. Zapier (Workflow Automation)
6. Telegram Bot (Chat Interface)
7. Monobank (Financial Transactions)

---

## INTEGRATION 1: GMAIL SETUP

### Configuration
```env
GOOGLE_CLIENT_ID=your_client_id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_client_secret
GOOGLE_CALLBACK_URL=https://yourdomain.com/api/v1/integrations/gmail/oauth-callback
GMAIL_SCOPE=https://www.googleapis.com/auth/gmail.readonly https://www.googleapis.com/auth/gmail.modify
```

### Setup Steps
1. Go to Google Cloud Console
2. Create OAuth 2.0 credentials (Web application)
3. Add redirect URI: https://yourdomain.com/api/v1/integrations/gmail/oauth-callback
4. Download credentials JSON
5. Store in environment variables

### Test Endpoint
```bash
curl -X POST http://localhost:8000/api/v1/integrations/gmail/oauth-callback?code=AUTH_CODE
```

---

## INTEGRATION 2: GITHUB SETUP

### Configuration
```env
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
GITHUB_CALLBACK_URL=https://yourdomain.com/api/v1/integrations/github/oauth-callback
GITHUB_WEBHOOK_SECRET=your_webhook_secret
GITHUB_REPO=romanchaa997/Bakhmach-Business-Hub
```

### Setup Steps
1. Go to GitHub Settings > Developer Settings > OAuth Apps
2. Create new OAuth App
3. Set Authorization callback URL
4. Create webhook with:
   - Payload URL: https://yourdomain.com/api/v1/webhooks/github
   - Content type: application/json
   - Events: push, pull_request, issues

### Events Handled
- Push events
- Pull request creation/update
- Issue creation/closing
- Repository events

---

## INTEGRATION 3: SLACK SETUP

### Configuration
```env
SLACK_CLIENT_ID=xoxp-xxxxxxxxxxxx
SLACK_CLIENT_SECRET=your_secret
SLACK_SIGNING_SECRET=your_signing_secret
SLACK_BOT_TOKEN=xoxb-xxxxxxxxxxxx
SLACK_CALLBACK_URL=https://yourdomain.com/api/v1/integrations/slack/oauth-callback
```

### Scopes Required
- chat:write
- chat:read
- users:read
- channels:manage
- groups:read

### Setup Steps
1. Create Slack App at api.slack.com
2. Configure OAuth & Permissions
3. Add redirect URL
4. Copy Bot Token
5. Set Event Subscriptions URL

---

## INTEGRATION 4: GOOGLE CALENDAR SETUP

### Configuration
```env
GOOGLE_CALENDAR_API_KEY=your_api_key
GOOGLE_CALENDAR_ID=primary
CALENDAR_WEBHOOK_URL=https://yourdomain.com/api/v1/webhooks/calendar
```

### Setup Steps
1. Enable Google Calendar API
2. Create Service Account
3. Grant Calendar permissions
4. Set up watch notifications

---

## INTEGRATION 5: ZAPIER SETUP

### Endpoints Required
```
POST /api/v1/zapier/trigger - Trigger events
POST /api/v1/zapier/action - Perform actions
GET /api/v1/zapier/fields - Get available fields
```

### Configuration
```env
ZAPIER_API_KEY=your_zapier_key
ZAPIER_WEBHOOK_SECRET=secret
```

---

## INTEGRATION 6: TELEGRAM BOT COMPLETE

### Configuration
```env
TELEGRAM_BOT_TOKEN=1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh
TELEGRAM_WEBHOOK_URL=https://yourdomain.com/api/v1/telegram/webhook
TELEGRAM_WEBHOOK_SECRET=your_secret
```

### Commands Implemented
- /start - Main menu
- /help - Help information
- /integrate - Integration options
- /status - Check integration status
- /transactions - Monobank transactions
- /settings - Bot settings

### Database Schema
```sql
CREATE TABLE telegram_users (
    id SERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE,
    username VARCHAR,
    first_name VARCHAR,
    last_name VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE telegram_integrations (
    id SERIAL PRIMARY KEY,
    telegram_user_id INTEGER REFERENCES telegram_users(id),
    service VARCHAR (gmail, github, slack, etc.),
    credentials JSONB,
    status VARCHAR (active, pending, disconnected),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE telegram_messages (
    id SERIAL PRIMARY KEY,
    telegram_user_id INTEGER REFERENCES telegram_users(id),
    message TEXT,
    message_type VARCHAR (command, callback, message),
    response TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Webhook Setup
```bash
# Set webhook
curl -X POST https://api.telegram.org/bot{TOKEN}/setWebhook \
  -F url=https://yourdomain.com/api/v1/telegram/webhook

# Verify webhook
curl https://api.telegram.org/bot{TOKEN}/getWebhookInfo
```

---

## INTEGRATION 7: MONOBANK SETUP

### Configuration
```env
MONOBANK_API_TOKEN=your_monobank_token
MONOBANK_WEBHOOK_URL=https://yourdomain.com/api/v1/monobank/webhook
MONOBANK_WEBHOOK_SECRET=your_secret
```

### API Endpoints
- GET /api/v1/monobank/accounts - List accounts
- GET /api/v1/monobank/transactions - Get transactions
- POST /api/v1/monobank/webhook - Webhook receiver

### Webhook Signature Validation
```python
import hmac
import hashlib

def validate_monobank_webhook(request_body, signature, secret):
    expected_signature = hmac.new(
        secret.encode(),
        request_body,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(signature, expected_signature)
```

---

## END-TO-END FEATURE TESTS

### Test Suite
```bash
pytest tests/test_integrations.py -v
pytest tests/test_telegram_bot.py -v
pytest tests/test_webhooks.py -v
pytest tests/test_api.py -v
```

### Core Features to Test
1. **Authentication** - OAuth2 flows for all services
2. **Integration Management** - Connect/disconnect services
3. **Data Sync** - Gmail sync, GitHub events, Slack messages
4. **Webhook Handling** - Receive and process events
5. **Telegram Commands** - All bot commands working
6. **Transaction Processing** - Monobank transactions sync
7. **Error Handling** - Graceful error responses
8. **Rate Limiting** - Respect API rate limits

---

## DEPLOYMENT CHECKLIST

### Pre-Deployment
- [ ] All environment variables set
- [ ] Database migrations applied
- [ ] Redis running and accessible
- [ ] SSL certificate installed
- [ ] Domain DNS configured
- [ ] All tests passing (100% coverage)
- [ ] Code review completed

### Deployment
- [ ] Build Docker image
- [ ] Push to registry
- [ ] Deploy to Kubernetes
- [ ] Verify health checks
- [ ] Check webhook connectivity
- [ ] Monitor logs for errors

### Post-Deployment
- [ ] Test all integrations in production
- [ ] Monitor error rates
- [ ] Check performance metrics
- [ ] Verify webhook deliveries
- [ ] Test Telegram bot commands
- [ ] Monitor transaction processing

---

## STATUS: READY FOR PRODUCTION ✅

All 7 integrations are fully documented and ready to deploy.

**Last Updated**: January 3, 2026, 7 AM EET
