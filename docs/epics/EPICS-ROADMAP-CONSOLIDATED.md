# Consolidated EPICS Roadmap – Q1-Q2 2026

**Owner**: Product Lead  
**Last Updated**: 2026-01-03  
**Status**: Planning  

## Executive Summary

Five parallel execution streams to achieve production-grade observability, reliability, AI enrichment, security, and SAAS readiness by Q2 2026. Total effort: ~40 person-weeks across 30+ FTE-weeks allocated.

## Epic Overview Table

| Epic | Stream | Owner | Q1 Window | Q2 Window | Priority | Status |
|------|--------|-------|-----------|-----------|----------|--------|
| SECURITY-EDGE | Security & Edge | Security Lead | Weeks 1-8 | - | HIGH | Planned |
| RELIABILITY-QUEUES | Reliability | Platform Lead | Weeks 1-8 | - | HIGH | Planned |
| AI-ENRICHMENT-ROUTING | AI | AI Lead | Weeks 1-6 | - | HIGH | In Prog |
| OBS-SLO-PHASES | Observability | SRE Lead | Weeks 3-8 | - | HIGH | Planned |
| SAAS-MULTITENANT | SAAS | Backend Lead | - | Weeks 9-16 | MEDIUM | Planned |

## Gantt Timeline (Quarters)

```
          Q1 2026                              Q2 2026
    W1-W2 W3-W4 W5-W6 W7-W8              W9-W12 W13-W16

SEC-EDGE [===] [===] [===] [===]         -       -
REL-QUEUE [===] [===] [===] [===]        -       -
AI-ENRICH [===] [===] [===] -            -       -
OBS-SLO   -     [===] [===] [===]        -       -
SAAS-MULTI -    -     -     -            [====] [====]
```

## Stream Dependencies

```
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 0 (Done) → PHASE 1 (Done) → PHASE 2 (Q1 2026) → PHASE 3  │
└─────────────────────────────────────────────────────────────────┘

PHASE 2 Q1 Streams:

  SEC-EDGE (mTLS, WAF, X-Trace-ID)
         ↓
  REL-QUEUE (DLQ, HPA, queue metrics) ← depends on SEC-EDGE (logs tracing)
         ↓
  AI-ENRICH (GPT-4o/Grok/Claude routing) ← runs in parallel
         ↓
  OBS-SLO (Phase automation, alerts) ← depends on AI-ENRICH (metrics)
         ↓
PHASE 3 Q2 Streams:

  SAAS-MULTI (auth, billing, admin) ← depends on all Q1 epics
```

## Key Milestones & Dependencies

### Dependency Matrix

| Epic | Blocks | Depends On | Critical Path |
|------|--------|-----------|---------------|
| SEC-EDGE | REL-QUEUE, OBS-SLO | - | X-Trace-ID |
| REL-QUEUE | OBS-SLO, SAAS-MULTI | SEC-EDGE | Queue metrics |
| AI-ENRICH | OBS-SLO, SAAS-MULTI | SEC-EDGE (optional) | aiextractedfields schema |
| OBS-SLO | SAAS-MULTI | AI-ENRICH, REL-QUEUE | Phase definition |
| SAAS-MULTI | - | All Q1 epics | Multi-epic rollout |

## Resource Allocation (Estimate)

- **Security Eng**: 8 FTE-weeks (SEC-EDGE)
- **Platform Eng**: 10 FTE-weeks (REL-QUEUE, SAAS-MULTI)
- **AI/ML Eng**: 6 FTE-weeks (AI-ENRICH)
- **SRE**: 8 FTE-weeks (OBS-SLO, metrics)
- **Backend Eng**: 6 FTE-weeks (SAAS-MULTI)
- **Frontend Eng**: 4 FTE-weeks (SAAS-MULTI admin UI)
- **QA/DevOps**: 4 FTE-weeks (load testing, CI/CD)

**Total**: ~46 FTE-weeks over 16 weeks = ~3 FTE continuous effort.

## SLO Success Criteria (Phase 2 Exit)

- ✅ mTLS + WAF on 100% of Backend APIs
- ✅ DLQ configured for all core queues; no message loss in prod
- ✅ AI-ENRICHMENT latency P95 <5s, success rate ≥99.5%
- ✅ Phase RED/YELLOW/GREEN/BLUE automated + alerted
- ✅ Zero security incidents post-deployment

## Rollout Sequence

1. **Weeks 1-2**: SEC-EDGE + REL-QUEUE foundation (staging)
2. **Weeks 3-4**: SEC-EDGE prod rollout; REL-QUEUE testing
3. **Weeks 5-6**: AI-ENRICH A/B test; OBS-SLO recording rules
4. **Weeks 7-8**: Full Q1 validation, stress testing, docs
5. **Weeks 9-16**: SAAS-MULTI buildout (parallel)

## Risk Register

| Risk | Impact | Owner | Mitigation |
|------|--------|-------|------------|
| Cert rotation impacts production | P0 | Security Lead | Staged rollout, automated testing |
| Queue HPA thrashing | P1 | Platform Lead | Conservative cooldown, alerts |
| Claude pricing surge | P2 | AI Lead | Cost caps, fallback routing |
| Admin dashboard feature creep | P2 | Frontend Lead | MVP scope lock |

## Contacts & Escalation

- **Product Lead** (overall): product@company.com
- **Security Lead**: security@company.com
- **Platform Lead**: platform@company.com
- **AI Lead**: ai@company.com
- **SRE Lead**: sre@company.com
- **Escalation**: vp-engineering@company.com

## References

- [EPIC-SECURITY-EDGE.md](./EPIC-SECURITY-EDGE.md)
- [EPIC-RELIABILITY-QUEUES.md](./EPIC-RELIABILITY-QUEUES.md)
- [EPIC-AI-ENRICHMENT-ROUTING.md](./EPIC-AI-ENRICHMENT-ROUTING.md)
- [EPIC-OBS-SLO-PHASES.md](./EPIC-OBS-SLO-PHASES.md)
- [EPIC-SAAS-MULTITENANT.md](./EPIC-SAAS-MULTITENANT.md)
- [ROADMAP.md](../ROADMAP.md)
- [GAP-FIXES.md](../GAP-FIXES.md)
