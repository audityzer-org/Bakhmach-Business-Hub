# Security Hardening & Compliance

## Encryption

### Data at Rest
- Database encryption: AWS RDS with KMS
- S3 buckets: Default AES-256 encryption
- Backup encryption: AWS managed keys (CMK)
- Disk encryption: Linux LUKS on all servers

### Data in Transit
- TLS 1.2+ for all connections
- HTTPS only (HTTP → 301 redirect)
- mTLS for service-to-service
- VPC endpoints for AWS services

## Authentication & Authorization

### OAuth 2.0 / OpenID Connect
```typescript
// Enable multi-provider auth
Providers: Google, Microsoft, GitHub
Scopes: email, profile, optional MFA
Token Expiry: 1 hour access, 30 days refresh
```

### RBAC Implementation
- Admin: Full system access
- Developer: Code push, test access
- User: Read/write own data
- Guest: Read-only public content

### API Security
- API Keys with rate limiting (100 req/min)
- JWT tokens (HS256/RS256)
- CORS policy: Strict origin checking
- CSRF tokens on state-changing operations

## Secrets Management

```bash
# AWS Secrets Manager
aws secretsmanager create-secret --name bakhmach/db-password

# Rotate every 30 days
aws secretsmanager rotate-secret --secret-id bakhmach/db-password
```

## Network Security

### VPC Configuration
- Public subnets: NAT gateway, ALB only
- Private subnets: Application tier
- Database tier: No internet access
- Security groups: Least privilege

### DDoS Protection
- AWS Shield Standard (built-in)
- AWS WAF for application layer
- Rate limiting: 10,000 req/sec per IP
- Geo-blocking if needed

## Compliance

### Standards
- OWASP Top 10 mitigation
- GDPR for EU users
- PCI DSS for payment data
- SOC 2 audit ready

### Audit Logging
```yaml
Logged Events:
  - Authentication attempts
  - Data access (queries)
  - Configuration changes
  - Failed security checks
Retention: 90 days
```

## Vulnerability Management

- Dependency scanning: Weekly
- Container scanning: On push
- Infrastructure scanning: Monthly
- Penetration testing: Quarterly

## Security Headers

```
Strict-Transport-Security: max-age=31536000
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Content-Security-Policy: strict
X-XSS-Protection: 1; mode=block
```
