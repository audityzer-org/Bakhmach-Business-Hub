# EPIC: SAAS Layer & Multitenant

**Epic ID**: SAAS-MULTITENANT-EPIC
**Owner**: Backend Lead
**Status**: Planned
**Target Window**: Q2 2026 (Week 9-16)
**Priority**: MEDIUM (Phase 2 enabler)

## Overview

Implement multitenant SaaS layer: JWT/OAuth auth, Stripe billing (subscriptions + usage-based), tenant-aware metrics/logs, admin dashboard for tenants and AI usage.

## Key Goals

1. JWT/OAuth middleware, tenant_id in all payloads/logs
2. Stripe subscriptions + usage-based billing for AI tokens
3. Tenant isolation in metrics (labels: tenant_id)
4. Admin dashboard: tenants, usage, SLO, queue depth
5. ClickUp sync with tenant context

## Timeline

Week 9-10: [==] JWT/OAuth + tenant routing
Week 11-12: [==] Stripe integration
Week 13-14: [==] Metrics + dashboards
Week 15-16: [==] Admin UI

## Subtasks

| ID | Task | Owner | Status | Due |
|----|------|-------|--------|-----|
| SAAS-1 | JWT/OAuth middleware | Backend Eng | Planned | 2026-03-21 |
| SAAS-2 | Tenant routing + isolation | Backend Eng | Planned | 2026-03-28 |
| SAAS-3 | Stripe billing integration | Backend Eng | Planned | 2026-04-04 |
| SAAS-4 | Tenant-aware metrics | SRE | Planned | 2026-04-11 |
| SAAS-5 | Admin React dashboard | Frontend Eng | Planned | 2026-04-25 |
| SAAS-6 | ClickUp multitenant sync | Platform Eng | Planned | 2026-05-02 |

## Definition of Done

- All Backend APIs require JWT token
- tenant_id in 100% of logs and metrics
- Stripe charges per tenant usage
- Admin dashboard fully functional
- Team understands tenant isolation model

## Contacts

- Owner: backend-lead@company.com
- Slack: #saas-epic
