# EPIC: AI Enrichment & Multi-LLM Routing

**Epic ID**: AI-ENRICHMENT-ROUTING-EPIC
**Owner**: AI/ML Engineering Lead
**Status**: In Progress
**Target Window**: Q1 2026 (Week 1-6)
**Priority**: HIGH

## Overview

Complete AI enrichment service with multi-LLM routing (GPT-4o primary, Grok fallback, Claude Opus/Sonnet high-precision branch). Finalize aiextractedfields JSON schema, implement cost-tracking, accuracy proxies.

## Key Goals

1. Finalize ai-enrichment-contract.md and aiextractedfields v1.1 schema
2. GPT-4o primary routing with Grok fallback
3. Claude Opus/Sonnet branch for PRODINCIDENT/BILLINGIMPACT/SECURITY
4. Cost metrics per provider (tokens in/out, USD estimate)
5. Accuracy proxy: manual_fix rate per provider
6. A/B test on ClickUp task sample; gather F1, latency, cost

## Timeline (Gantt)

Week 1: [=] Finalize contract + schema
Week 2: [=] Implement Claude branch
Week 3-4: [==] A/B test + metrics collection
Week 5-6: [==] Analysis, recommendations, rollout

## Subtasks

| ID | Task | Owner | Status | Due |
|----|------|-------|--------|-----|
| AI-1 | Finalize ai-enrichment-contract.md | AI Eng | Done | 2026-01-10 |
| AI-2 | aiextractedfields v1.1 schema review | AI Eng | Done | 2026-01-10 |
| AI-3 | Implement Claude Opus/Sonnet routing | AI Eng | In Prog | 2026-01-17 |
| AI-4 | Cost metrics per provider integration | SRE | Planned | 2026-01-24 |
| AI-5 | A/B test design + ClickUp sample | AI Eng | Planned | 2026-01-31 |
| AI-6 | Analysis: F1, latency, cost comparison | AI Eng | Planned | 2026-02-14 |
| AI-7 | Rollout recommendations + docs | AI Eng | Planned | 2026-02-21 |

## Definition of Done

- Contract and schema finalized and checked in
- Claude branch production-ready
- Cost metrics exported to Prometheus
- A/B test completed on 1k ClickUp tasks
- F1 score and latency baseline per provider
- Team approved routing policy

## Acceptance Criteria

- [ ] ai-enrichment-contract.md reviewed by backend team
- [ ] Claude routing in code; fallback chains tested
- [ ] aienrichment_cost_usd_total{provider} in Prometheus
- [ ] A/B test: 500 GPT-4o, 500 Grok, 500 Claude samples
- [ ] F1 comparison: GPT-4o vs others with confidence intervals
- [ ] Team presentation + rollout decision

## Contacts

- Owner: ai-lead@company.com
- Slack: #ai-enrichment-epic
