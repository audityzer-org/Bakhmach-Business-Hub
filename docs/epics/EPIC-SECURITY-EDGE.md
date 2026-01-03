# EPIC: Security & Edge (Cloudflare / mTLS / WAF)

**Epic ID**: SECURITY-EDGE-EPIC
**Owner**: Security Engineering Lead
**Status**: Planned
**Target Window**: Q1 2026 (Week 1-8)
**Priority**: HIGH

## Overview

Harden Cloudflare edge security with full mTLS, WAF rules, rate limiting, and X-Trace-ID propagation.

## Key Goals

1. Enable mTLS for all Backend connections
2. Deploy WAF managed rulesets for /api/* endpoints
3. Implement rate limiting: 100 req / 10s per IP
4. Propagate X-Trace-ID through all logs and metrics
5. Structured logging to SIEM

## Timeline (Gantt)

Week 1-2: [===] Cert provisioning + mTLS pilot
Week 3-4: [===] mTLS prod rollout + WAF rules
Week 5-6: [===] Rate limiting + X-Trace-ID
Week 7-8: [===] E2E testing, docs, hardening

## Subtasks

| ID | Task | Owner | Status | Due |
|----|------|-------|--------|-----|
| SEC-1 | Issue/rotate client certs | Security Eng | Planned | 2026-01-17 |
| SEC-2 | Configure mTLS rules | Security Eng | Planned | 2026-01-24 |
| SEC-3 | Build WAF rulesets | Security Eng | Planned | 2026-01-31 |
| SEC-4 | Implement Worker + X-Trace-ID | Platform Eng | In Prog | 2026-02-07 |
| SEC-5 | Logpush to S3/Datadog | SRE | Planned | 2026-02-14 |
| SEC-6 | E2E testing | QA | Planned | 2026-02-21 |
| SEC-7 | Documentation | Tech Writer | Planned | 2026-02-28 |

## Definition of Done

- All backend ingress protected by mTLS
- X-Trace-ID in 100% of logs
- WAF blocks attacks with <1% false positives
- Rate limiting enforced: 100 req/10s per IP
- Cert rotation automated (30-day renewal)
- Zero security incidents in 30 days post-launch

## Dependencies

None (can run in parallel)

## Risks

| Risk | Mitigation |
|------|------------|
| Cert rotation breaks auth | Automated ACME + staging rollout |
| WAF false positives | A/B test on <5% traffic |
| X-Trace-ID latency | Batch tracing, 10% sampling |

## Rollback Plan

1. Disable mTLS in Cloudflare
2. Revert WAF rules
3. Clear rate-limit rules
4. Redeploy old Worker code
5. RTO: <5 minutes

## Acceptance Criteria

- [ ] mTLS on /api/*; handshake <50ms
- [ ] X-Trace-ID in 100% of logs
- [ ] WAF blocks OWASP top-10 with <1% FP
- [ ] Rate-limit 429s logged in Prometheus
- [ ] Cert rotation tested; auto-rotation enabled
- [ ] Incident response playbook documented
- [ ] Team trained on WAF/mTLS flow

## Contacts

- Owner: security-lead@company.com
- Slack: #security-epic
- Escalation: cto@company.com
