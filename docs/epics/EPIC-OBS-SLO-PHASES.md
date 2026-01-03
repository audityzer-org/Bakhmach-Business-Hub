# EPIC: Observability & SLO/Phase Automation

**Epic ID**: OBS-SLO-PHASES-EPIC
**Owner**: SRE Lead
**Status**: Planned
**Target Window**: Q1 2026 (Week 3-8)
**Priority**: HIGH

## Overview

Formalize SLO/SLA metrics for AI Enrichment and implement RED/YELLOW/GREEN/BLUE phase automation via Prometheus recording rules and alert thresholds.

## Key Goals

1. Define SLO: P95 latency <5s, success rate >=99.5%, queue depth <5000
2. Recording rules: aienrichment_phase_state{phase=RED|YELLOW|GREEN|BLUE}
3. Alert rules: thresholds for RED/YELLOW, auto-actions in Slack
4. Playbook: RED=throttle+scale, YELLOW=fallback-only, GREEN=normal, BLUE=cooldown
5. Grafana/Datadog dashboards: phase indicator + trending metrics

## Timeline

Week 3: [=] SLO definition + baseline collection
Week 4-5: [==] Recording rules + alerts
Week 6-7: [==] Playbook + runbook
Week 8: [=] Team training + deploy

## Subtasks

| ID | Task | Owner | Status | Due |
|----|------|-------|--------|-----|
| OBS-1 | Define SLO/SLA per service | SRE | Planned | 2026-02-07 |
| OBS-2 | Recording rules for phases | SRE | Planned | 2026-02-14 |
| OBS-3 | Alert rules + Slack webhooks | SRE | Planned | 2026-02-21 |
| OBS-4 | Grafana dashboards + phase widget | SRE | Planned | 2026-02-28 |
| OBS-5 | Incident playbook + runbook | SRE | Planned | 2026-03-07 |
| OBS-6 | Team training session | SRE | Planned | 2026-03-14 |

## Definition of Done

- SLO/SLA documented in METRICS-AND-KPIs.md
- aienrichment_phase_state in Prometheus
- Alerts fire within 2 min of RED
- Grafana dashboard shows phase history
- Team understands runbook for each phase

## Contacts

- Owner: sre-lead@company.com
- Slack: #observability-epic
