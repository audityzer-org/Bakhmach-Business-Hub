# EPIC: Reliability & Queues (RabbitMQ + HPA)

**Epic ID**: RELIABILITY-QUEUES-EPIC
**Owner**: Platform Engineering Lead
**Status**: Planned
**Target Window**: Q1 2026 (Week 1-8)
**Priority**: HIGH

## Overview

Implement DLQ (Dead Letter Queue) infrastructure for all core RabbitMQ queues, exponential backoff retry strategies, and queue-based HPA (Horizontal Pod Autoscaler) to prevent RED phase incidents.

## Key Goals

1. DLQ for rawevents, normalizedevents, resultqueue, enrichqueue
2. Exponential backoff retry logic (1s -> 2s -> 4s -> 8s...)
3. RabbitMQ Prometheus exporter + custom queue depth metric
4. HPA scaling by queue depth (threshold 5000 messages)
5. Nightly DLQ cleanup and alerting
6. Load test: 10k events, verify no RED phase

## Timeline (Gantt)

Week 1-2: [===] DLQ setup + backoff logic
Week 3-4: [===] RabbitMQ exporter + Prometheus rules
Week 5-6: [===] HPA configuration + testing
Week 7-8: [===] Load testing, validation, docs

## Subtasks

| ID | Task | Owner | Status | Due |
|----|------|-------|--------|-----|
| REL-1 | DLQ infrastructure setup | Platform Eng | Planned | 2026-01-17 |
| REL-2 | Exponential backoff retry logic | Platform Eng | Planned | 2026-01-24 |
| REL-3 | RabbitMQ exporter deployment | SRE | Planned | 2026-01-31 |
| REL-4 | Configure HPA by queue depth | SRE | Planned | 2026-02-07 |
| REL-5 | DLQ monitoring + alerting | SRE | Planned | 2026-02-14 |
| REL-6 | Load test 10k events | QA | Planned | 2026-02-21 |
| REL-7 | Documentation + runbooks | Tech Writer | Planned | 2026-02-28 |

## Definition of Done

- All core queues have DLQ configured
- Retry backoff: 1s, 2s, 4s, 8s, 16s max
- aiprocessingqueuedepth metric exported by RabbitMQ
- HPA scales pods when queue > 5000 messages
- No RED phase lasting >5 min in production
- Zero message loss in load test (10k events)
- DLQ alerting: topic:rabbitmq.dlq.depth

## Dependencies

- None (can run in parallel with Security)

## Risks

| Risk | Mitigation |
|------|------------|
| DLQ not drained properly | Cron job cleanup, alerts on DLQ depth ||
| HPA thrashing | Min replicas=2, cooldown period 5 min |
| Backoff too aggressive | Start with 1s, monitor latency impact |

## Rollback Plan

1. Disable HPA (manual replicas)
2. Clear DLQ settings from RabbitMQ config
3. Redeploy old queue definitions
4. RTO: 10 minutes

## Acceptance Criteria

- [ ] DLQ visible in RabbitMQ UI
- [ ] aiprocessingqueuedepth in Prometheus
- [ ] HPA scales 2->10 pods as queue grows
- [ ] Backoff tested: max retry 5 attempts
- [ ] Load test: 10k events processed, <5% DLQ
- [ ] SLO met: P95 latency < 8s, 99.5% success
- [ ] Team trained on DLQ/retry flow

## Contacts

- Owner: platform-lead@company.com
- Slack: #reliability-epic
- Escalation: vp-engineering@company.com
