# Bakhmach Business Hub - API Reference

## Base URL
```
https://api.bakhmach.dev/v1
Alternative: https://api-staging.bakhmach.dev/v1
```

## Authentication

All API endpoints require authentication via Bearer token in the Authorization header:

```
Authorization: Bearer YOUR_API_TOKEN
Content-Type: application/json
```

### Obtaining API Token
```bash
curl -X POST https://api.bakhmach.dev/v1/auth/token \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password"}'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

## API Endpoints

### 1. Projects

#### List All Projects
```
GET /projects
```

Response:
```json
{
  "data": [
    {
      "id": "proj_123",
      "name": "Q4 Marketing Campaign",
      "status": "active",
      "created_at": "2026-01-01T00:00:00Z",
      "updated_at": "2026-01-09T15:30:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 45
  }
}
```

#### Create Project
```
POST /projects
```

Request Body:
```json
{
  "name": "New Business Initiative",
  "description": "Quarterly business expansion plan",
  "budget": 100000,
  "start_date": "2026-01-15",
  "end_date": "2026-04-15",
  "owner_id": "user_456"
}
```

#### Get Project Details
```
GET /projects/{project_id}
```

#### Update Project
```
PUT /projects/{project_id}
```

#### Delete Project
```
DELETE /projects/{project_id}
```

### 2. Tasks

#### List Project Tasks
```
GET /projects/{project_id}/tasks
```

Query Parameters:
- `status`: (active, completed, archived)
- `priority`: (high, medium, low)
- `assigned_to`: User ID

#### Create Task
```
POST /projects/{project_id}/tasks
```

Request Body:
```json
{
  "title": "Complete market research",
  "description": "Analyze competitor strategies",
  "priority": "high",
  "status": "active",
  "assigned_to": "user_789",
  "due_date": "2026-01-20",
  "tags": ["research", "q4"]
}
```

#### Update Task
```
PUT /projects/{project_id}/tasks/{task_id}
```

#### Delete Task
```
DELETE /projects/{project_id}/tasks/{task_id}
```

### 3. Team Members

#### List Team Members
```
GET /team
```

#### Add Team Member
```
POST /team
```

Request Body:
```json
{
  "email": "newmember@bakhmach.dev",
  "role": "developer",
  "department": "engineering"
}
```

#### Update Member Role
```
PUT /team/{user_id}
```

#### Remove Team Member
```
DELETE /team/{user_id}
```

### 4. Metrics & Analytics

#### Get Project Metrics
```
GET /projects/{project_id}/metrics
```

Response:
```json
{
  "completion_rate": 75,
  "budget_utilization": 62.5,
  "timeline_adherence": 88,
  "team_productivity": 92,
  "quality_score": 8.5
}
```

#### Get Team Productivity
```
GET /analytics/productivity
```

Query Parameters:
- `start_date`: (YYYY-MM-DD)
- `end_date`: (YYYY-MM-DD)
- `granularity`: (daily, weekly, monthly)

#### Get Financial Reports
```
GET /analytics/financial
```

### 5. Notifications

#### Get Notifications
```
GET /notifications
```

#### Mark as Read
```
POST /notifications/{notification_id}/read
```

#### Delete Notification
```
DELETE /notifications/{notification_id}
```

### 6. Files & Attachments

#### Upload File
```
POST /uploads
Content-Type: multipart/form-data
```

#### Download File
```
GET /files/{file_id}/download
```

#### Delete File
```
DELETE /files/{file_id}
```

## Error Handling

All errors follow standard HTTP status codes:

- `200 OK`: Successful request
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Missing or invalid authentication
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

### Error Response Format
```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Invalid project ID format",
    "details": {
      "field": "project_id",
      "reason": "must be alphanumeric"
    }
  }
}
```

## Rate Limiting

- **Standard**: 100 requests per minute
- **Premium**: 1000 requests per minute
- **Enterprise**: Unlimited

Headers returned with rate limit info:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1610000000
```

## Pagination

### Request
```bash
GET /projects?page=2&limit=25
```

### Response
```json
{
  "data": [...],
  "pagination": {
    "page": 2,
    "limit": 25,
    "total": 150,
    "pages": 6
  }
}
```

## Webhooks

### Register Webhook
```
POST /webhooks
```

Request Body:
```json
{
  "url": "https://your-domain.com/webhook",
  "events": ["project.created", "task.completed"],
  "active": true
}
```

### Webhook Events
- `project.created`
- `project.updated`
- `project.deleted`
- `task.created`
- `task.completed`
- `team.member.added`

## SDK Examples

### JavaScript/Node.js
```javascript
const bakhmach = require('@bakhmach/sdk');
const client = new bakhmach.Client({
  apiToken: 'your-api-token'
});

const projects = await client.projects.list();
const newTask = await client.tasks.create(projectId, {
  title: 'New task',
  priority: 'high'
});
```

### Python
```python
import bakhmach
client = bakhmach.Client(api_token='your-api-token')
projects = client.projects.list()
print(projects)
```

## Support

- **Documentation**: https://docs.bakhmach.dev
- **Status Page**: https://status.bakhmach.dev
- **Support Email**: api-support@bakhmach.dev
- **GitHub Issues**: https://github.com/romanchaa997/Bakhmach-Business-Hub/issues

---
**API Version**: 1.0.0
**Last Updated**: January 2026
**Status**: Production Ready ✅
